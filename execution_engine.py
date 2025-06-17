"""
Execution Engine - Handles trade execution with risk controls and multi-wallet support
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid

from ..data.pumpportal_client import PumpPortalClient
from ..wallets.wallet_manager import WalletManager, SolanaWallet
from ..trading.strategy_engine import TradingSignal, StrategyType
from ..trading.risk_manager import RiskManager, Position, RiskLevel
from ..config.settings import settings

logger = logging.getLogger(__name__)

class ExecutionStatus(Enum):
    """Execution status for trades"""
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

class OrderType(Enum):
    """Types of orders"""
    MARKET_BUY = "market_buy"
    MARKET_SELL = "market_sell"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"

class TradeExecution:
    """Represents a trade execution"""
    
    def __init__(self, 
                 execution_id: str,
                 signal: TradingSignal,
                 wallet: SolanaWallet,
                 order_type: OrderType,
                 amount: float,
                 expected_price: float = 0.0):
        self.execution_id = execution_id
        self.signal = signal
        self.wallet = wallet
        self.order_type = order_type
        self.amount = amount
        self.expected_price = expected_price
        self.status = ExecutionStatus.PENDING
        self.created_at = datetime.utcnow()
        self.executed_at = None
        self.actual_price = 0.0
        self.actual_amount = 0.0
        self.transaction_signature = None
        self.gas_fee = 0.0
        self.slippage = 0.0
        self.error_message = None
        self.retry_count = 0
        self.max_retries = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert execution to dictionary"""
        return {
            'execution_id': self.execution_id,
            'signal_id': self.signal.signal_id,
            'wallet_id': self.wallet.wallet_id,
            'order_type': self.order_type.value,
            'amount': self.amount,
            'expected_price': self.expected_price,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'executed_at': self.executed_at.isoformat() if self.executed_at else None,
            'actual_price': self.actual_price,
            'actual_amount': self.actual_amount,
            'transaction_signature': self.transaction_signature,
            'gas_fee': self.gas_fee,
            'slippage': self.slippage,
            'error_message': self.error_message,
            'retry_count': self.retry_count
        }

class ExecutionEngine:
    """Handles trade execution with risk controls"""
    
    def __init__(self, wallet_manager: WalletManager, risk_manager: RiskManager):
        self.wallet_manager = wallet_manager
        self.risk_manager = risk_manager
        self.pumpportal_client = None
        self.pending_executions: Dict[str, TradeExecution] = {}
        self.completed_executions: List[TradeExecution] = []
        self.execution_queue = asyncio.Queue()
        self.is_running = False
        
    async def initialize(self):
        """Initialize execution engine"""
        try:
            logger.info("Initializing execution engine...")
            
            # Initialize PumpPortal client
            self.pumpportal_client = PumpPortalClient()
            await self.pumpportal_client.__aenter__()
            
            # Start execution worker
            self.is_running = True
            asyncio.create_task(self._execution_worker())
            asyncio.create_task(self._monitoring_worker())
            
            logger.info("Execution engine initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize execution engine: {str(e)}")
            raise
    
    async def execute_signal(self, signal: TradingSignal) -> Optional[str]:
        """
        Execute a trading signal
        
        Args:
            signal: Trading signal to execute
        
        Returns:
            Execution ID if successful, None otherwise
        """
        try:
            logger.info(f"Executing signal: {signal.signal_id}")
            
            # Get appropriate wallet
            wallet = await self.wallet_manager.get_wallet_for_strategy(
                signal.strategy_type.value, 
                signal.recommended_amount
            )
            
            if not wallet:
                logger.error(f"No suitable wallet found for signal {signal.signal_id}")
                return None
            
            # Get wallet balance
            wallet_balance = await self.wallet_manager.get_wallet_balance(wallet.wallet_id)
            
            # Evaluate risk
            risk_evaluation = await self.risk_manager.evaluate_signal_risk(signal, wallet_balance)
            
            if not risk_evaluation['approved']:
                logger.warning(f"Signal {signal.signal_id} rejected by risk manager: {risk_evaluation['blocking_factors']}")
                return None
            
            # Use risk-adjusted amount
            execution_amount = risk_evaluation['recommended_amount']
            
            # Create execution
            execution_id = f"exec_{signal.signal_id}_{int(datetime.utcnow().timestamp())}"
            execution = TradeExecution(
                execution_id=execution_id,
                signal=signal,
                wallet=wallet,
                order_type=OrderType.MARKET_BUY,
                amount=execution_amount
            )
            
            # Add to pending executions
            self.pending_executions[execution_id] = execution
            
            # Queue for execution
            await self.execution_queue.put(execution)
            
            logger.info(f"Queued execution {execution_id} for signal {signal.signal_id}")
            return execution_id
            
        except Exception as e:
            logger.error(f"Error executing signal: {str(e)}")
            return None
    
    async def _execution_worker(self):
        """Background worker for processing executions"""
        try:
            while self.is_running:
                try:
                    # Get next execution from queue
                    execution = await asyncio.wait_for(self.execution_queue.get(), timeout=1.0)
                    
                    # Process the execution
                    await self._process_execution(execution)
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    logger.error(f"Error in execution worker: {str(e)}")
                    await asyncio.sleep(1)
                    
        except asyncio.CancelledError:
            logger.info("Execution worker cancelled")
        except Exception as e:
            logger.error(f"Fatal error in execution worker: {str(e)}")
    
    async def _process_execution(self, execution: TradeExecution):
        """Process a single trade execution"""
        try:
            execution.status = ExecutionStatus.EXECUTING
            logger.info(f"Processing execution {execution.execution_id}")
            
            if execution.order_type == OrderType.MARKET_BUY:
                success = await self._execute_market_buy(execution)
            elif execution.order_type == OrderType.MARKET_SELL:
                success = await self._execute_market_sell(execution)
            else:
                logger.error(f"Unsupported order type: {execution.order_type}")
                success = False
            
            if success:
                execution.status = ExecutionStatus.COMPLETED
                execution.executed_at = datetime.utcnow()
                
                # Create position for risk management
                if execution.order_type == OrderType.MARKET_BUY:
                    await self._create_position_from_execution(execution)
                
                # Update wallet usage
                execution.wallet.update_usage(execution.actual_amount * execution.actual_price)
                
                logger.info(f"Execution {execution.execution_id} completed successfully")
                
            else:
                # Handle failure
                execution.retry_count += 1
                
                if execution.retry_count < execution.max_retries:
                    logger.warning(f"Execution {execution.execution_id} failed, retrying ({execution.retry_count}/{execution.max_retries})")
                    execution.status = ExecutionStatus.PENDING
                    
                    # Add delay before retry
                    await asyncio.sleep(2 ** execution.retry_count)  # Exponential backoff
                    await self.execution_queue.put(execution)
                else:
                    execution.status = ExecutionStatus.FAILED
                    logger.error(f"Execution {execution.execution_id} failed after {execution.max_retries} retries")
            
            # Move to completed executions if done
            if execution.status in [ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.CANCELLED]:
                self.completed_executions.append(execution)
                if execution.execution_id in self.pending_executions:
                    del self.pending_executions[execution.execution_id]
            
        except Exception as e:
            logger.error(f"Error processing execution {execution.execution_id}: {str(e)}")
            execution.status = ExecutionStatus.FAILED
            execution.error_message = str(e)
    
    async def _execute_market_buy(self, execution: TradeExecution) -> bool:
        """Execute a market buy order"""
        try:
            # Prepare trade parameters
            trade_params = {
                "action": "buy",
                "mint": execution.signal.mint_address,
                "amount": execution.amount,
                "denominatedInSol": True,
                "slippage": 1.0,  # 1% slippage tolerance
                "priorityFee": 0.0001,  # Priority fee for faster execution
                "pool": "pump"
            }
            
            # Execute trade through PumpPortal
            result = await self.pumpportal_client.execute_trade(trade_params)
            
            if result['success']:
                # Parse execution results
                execution.transaction_signature = result['data'].get('signature', '')
                execution.actual_price = result['data'].get('price', 0.0)
                execution.actual_amount = result['data'].get('amount', 0.0)
                execution.gas_fee = result['data'].get('fee', 0.0)
                
                # Calculate slippage
                if execution.expected_price > 0:
                    execution.slippage = abs(execution.actual_price - execution.expected_price) / execution.expected_price * 100
                
                logger.info(f"Market buy executed: {execution.actual_amount} tokens at {execution.actual_price}")
                return True
            else:
                execution.error_message = result.get('error', 'Unknown error')
                logger.error(f"Market buy failed: {execution.error_message}")
                return False
                
        except Exception as e:
            execution.error_message = str(e)
            logger.error(f"Error executing market buy: {str(e)}")
            return False
    
    async def _execute_market_sell(self, execution: TradeExecution) -> bool:
        """Execute a market sell order"""
        try:
            # Prepare trade parameters
            trade_params = {
                "action": "sell",
                "mint": execution.signal.mint_address,
                "amount": execution.amount,
                "denominatedInSol": False,  # Selling tokens, not SOL
                "slippage": 1.0,
                "priorityFee": 0.0001,
                "pool": "pump"
            }
            
            # Execute trade through PumpPortal
            result = await self.pumpportal_client.execute_trade(trade_params)
            
            if result['success']:
                # Parse execution results
                execution.transaction_signature = result['data'].get('signature', '')
                execution.actual_price = result['data'].get('price', 0.0)
                execution.actual_amount = result['data'].get('amount', 0.0)
                execution.gas_fee = result['data'].get('fee', 0.0)
                
                # Calculate slippage
                if execution.expected_price > 0:
                    execution.slippage = abs(execution.actual_price - execution.expected_price) / execution.expected_price * 100
                
                logger.info(f"Market sell executed: {execution.actual_amount} tokens at {execution.actual_price}")
                return True
            else:
                execution.error_message = result.get('error', 'Unknown error')
                logger.error(f"Market sell failed: {execution.error_message}")
                return False
                
        except Exception as e:
            execution.error_message = str(e)
            logger.error(f"Error executing market sell: {str(e)}")
            return False
    
    async def _create_position_from_execution(self, execution: TradeExecution):
        """Create a position in risk manager from successful execution"""
        try:
            position_id = f"pos_{execution.signal.mint_address}_{execution.wallet.wallet_id}_{int(datetime.utcnow().timestamp())}"
            
            position = Position(
                position_id=position_id,
                mint_address=execution.signal.mint_address,
                wallet_id=execution.wallet.wallet_id,
                strategy_type=execution.signal.strategy_type,
                entry_price=execution.actual_price,
                entry_amount=execution.actual_amount,
                current_amount=execution.actual_amount,
                entry_timestamp=execution.executed_at or datetime.utcnow(),
                stop_loss=execution.signal.stop_loss,
                take_profit_levels=execution.signal.take_profit_levels,
                current_price=execution.actual_price
            )
            
            await self.risk_manager.add_position(position)
            logger.info(f"Created position {position_id} from execution {execution.execution_id}")
            
        except Exception as e:
            logger.error(f"Error creating position from execution: {str(e)}")
    
    async def execute_stop_loss(self, position_id: str) -> bool:
        """Execute stop loss for a position"""
        try:
            # Get position from risk manager
            position = self.risk_manager.positions.get(position_id)
            if not position:
                logger.error(f"Position not found for stop loss: {position_id}")
                return False
            
            # Get wallet
            wallet = None
            for w in self.wallet_manager.wallets.values():
                if w.wallet_id == position.wallet_id:
                    wallet = w
                    break
            
            if not wallet:
                logger.error(f"Wallet not found for stop loss: {position.wallet_id}")
                return False
            
            # Create sell execution
            execution_id = f"sl_{position_id}_{int(datetime.utcnow().timestamp())}"
            
            # Create a dummy signal for the stop loss
            from ..trading.strategy_engine import TradingSignal, SignalStrength
            stop_loss_signal = TradingSignal(
                mint_address=position.mint_address,
                strategy_type=position.strategy_type,
                signal_strength=SignalStrength.STRONG_SELL,
                confidence=1.0,
                recommended_amount=position.current_amount,
                stop_loss=0.0,
                take_profit_levels=[],
                reasoning="Stop loss triggered"
            )
            
            execution = TradeExecution(
                execution_id=execution_id,
                signal=stop_loss_signal,
                wallet=wallet,
                order_type=OrderType.STOP_LOSS,
                amount=position.current_amount,
                expected_price=position.current_price
            )
            
            # Execute immediately (high priority)
            success = await self._execute_market_sell(execution)
            
            if success:
                # Close position in risk manager
                await self.risk_manager.close_position(
                    position_id, 
                    execution.actual_price, 
                    execution.actual_amount
                )
                
                logger.info(f"Stop loss executed for position {position_id}")
                return True
            else:
                logger.error(f"Stop loss execution failed for position {position_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing stop loss: {str(e)}")
            return False
    
    async def execute_take_profit(self, position_id: str, percentage: float = 0.5) -> bool:
        """Execute take profit for a position"""
        try:
            # Get position from risk manager
            position = self.risk_manager.positions.get(position_id)
            if not position:
                logger.error(f"Position not found for take profit: {position_id}")
                return False
            
            # Calculate amount to sell
            sell_amount = position.current_amount * percentage
            
            # Get wallet
            wallet = None
            for w in self.wallet_manager.wallets.values():
                if w.wallet_id == position.wallet_id:
                    wallet = w
                    break
            
            if not wallet:
                logger.error(f"Wallet not found for take profit: {position.wallet_id}")
                return False
            
            # Create sell execution
            execution_id = f"tp_{position_id}_{int(datetime.utcnow().timestamp())}"
            
            # Create a dummy signal for the take profit
            from ..trading.strategy_engine import TradingSignal, SignalStrength
            take_profit_signal = TradingSignal(
                mint_address=position.mint_address,
                strategy_type=position.strategy_type,
                signal_strength=SignalStrength.SELL,
                confidence=1.0,
                recommended_amount=sell_amount,
                stop_loss=0.0,
                take_profit_levels=[],
                reasoning=f"Take profit triggered ({percentage*100:.0f}%)"
            )
            
            execution = TradeExecution(
                execution_id=execution_id,
                signal=take_profit_signal,
                wallet=wallet,
                order_type=OrderType.TAKE_PROFIT,
                amount=sell_amount,
                expected_price=position.current_price
            )
            
            # Execute immediately (high priority)
            success = await self._execute_market_sell(execution)
            
            if success:
                # Partially close position in risk manager
                await self.risk_manager.close_position(
                    position_id, 
                    execution.actual_price, 
                    execution.actual_amount
                )
                
                logger.info(f"Take profit executed for position {position_id}: {percentage*100:.0f}%")
                return True
            else:
                logger.error(f"Take profit execution failed for position {position_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error executing take profit: {str(e)}")
            return False
    
    async def _monitoring_worker(self):
        """Background worker for monitoring positions and executing stop losses/take profits"""
        try:
            while self.is_running:
                try:
                    # Check all positions for stop loss and take profit triggers
                    for position_id, position in self.risk_manager.positions.items():
                        # Update position price (this would come from real-time data)
                        # For now, we'll skip this as it requires price feed integration
                        
                        # Check for risk alerts
                        alerts = await self.risk_manager.update_position_price(position_id, position.current_price)
                        
                        if alerts:
                            for alert in alerts:
                                if alert.alert_type.value == "position_stop_loss":
                                    logger.warning(f"Stop loss triggered for {position_id}")
                                    await self.execute_stop_loss(position_id)
                                elif alert.alert_type.value == "position_take_profit":
                                    logger.info(f"Take profit triggered for {position_id}")
                                    await self.execute_take_profit(position_id, 0.5)  # Sell 50%
                    
                    await asyncio.sleep(10)  # Check every 10 seconds
                    
                except Exception as e:
                    logger.error(f"Error in monitoring worker: {str(e)}")
                    await asyncio.sleep(5)
                    
        except asyncio.CancelledError:
            logger.info("Monitoring worker cancelled")
        except Exception as e:
            logger.error(f"Fatal error in monitoring worker: {str(e)}")
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific execution"""
        # Check pending executions
        if execution_id in self.pending_executions:
            return self.pending_executions[execution_id].to_dict()
        
        # Check completed executions
        for execution in self.completed_executions:
            if execution.execution_id == execution_id:
                return execution.to_dict()
        
        return None
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executions"""
        try:
            pending_count = len(self.pending_executions)
            completed_count = len(self.completed_executions)
            
            successful_executions = [
                ex for ex in self.completed_executions 
                if ex.status == ExecutionStatus.COMPLETED
            ]
            failed_executions = [
                ex for ex in self.completed_executions 
                if ex.status == ExecutionStatus.FAILED
            ]
            
            total_volume = sum(
                ex.actual_amount * ex.actual_price 
                for ex in successful_executions
            )
            
            average_slippage = sum(ex.slippage for ex in successful_executions) / len(successful_executions) if successful_executions else 0
            
            return {
                'pending_executions': pending_count,
                'completed_executions': completed_count,
                'successful_executions': len(successful_executions),
                'failed_executions': len(failed_executions),
                'success_rate': len(successful_executions) / completed_count * 100 if completed_count > 0 else 0,
                'total_volume': total_volume,
                'average_slippage': average_slippage,
                'queue_size': self.execution_queue.qsize()
            }
            
        except Exception as e:
            logger.error(f"Error generating execution summary: {str(e)}")
            return {}
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a pending execution"""
        try:
            if execution_id in self.pending_executions:
                execution = self.pending_executions[execution_id]
                if execution.status == ExecutionStatus.PENDING:
                    execution.status = ExecutionStatus.CANCELLED
                    logger.info(f"Execution {execution_id} cancelled")
                    return True
                else:
                    logger.warning(f"Cannot cancel execution {execution_id} with status {execution.status}")
                    return False
            else:
                logger.warning(f"Execution not found: {execution_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error cancelling execution: {str(e)}")
            return False
    
    async def cleanup(self):
        """Cleanup execution engine resources"""
        try:
            self.is_running = False
            
            if self.pumpportal_client:
                await self.pumpportal_client.__aexit__(None, None, None)
            
            logger.info("Execution engine cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during execution engine cleanup: {str(e)}")

