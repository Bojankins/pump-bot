"""
Updated main application with enhanced components integration
"""
import asyncio
import logging
import signal
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

from src.config.settings import settings
from src.data.pumpportal_client import PumpPortalClient
from src.data.bitquery_client import BitqueryClient
from src.data.data_processor import DataProcessor
from src.trading.strategy_engine import StrategyEngine
from src.trading.advanced_sniping_strategy import AdvancedSnipingStrategy
from src.trading.long_term_strategy import LongTermStrategy
from src.trading.enhanced_execution_engine import EnhancedExecutionEngine
from src.trading.mev_protection import MEVProtectionModule
from src.trading.market_microstructure import MarketMicrostructureAnalyzer
from src.trading.pumpfun_optimizer import PumpFunOptimizer
from src.trading.risk_manager import RiskManager
from src.wallets.wallet_manager import WalletManager
from src.wallets.reputation_manager import ReputationManager
from src.monitoring.performance_monitor import PerformanceMonitor
from src.monitoring.alert_system import AlertSystem
from src.monitoring.safety_circuit import SafetyCircuit
from src.monitoring.logger import setup_logging

logger = logging.getLogger(__name__)

class EnhancedPumpFunTradingBot:
    """Enhanced Pump.fun Trading Bot with advanced features"""
    
    def __init__(self):
        self.running = False
        self.shutdown_event = asyncio.Event()
        
        # Core components
        self.data_processor = None
        self.strategy_engine = None
        self.wallet_manager = None
        self.risk_manager = None
        self.reputation_manager = None
        
        # Enhanced components
        self.mev_protection = None
        self.market_analyzer = None
        self.pumpfun_optimizer = None
        self.enhanced_execution_engine = None
        
        # Strategies
        self.sniping_strategy = None
        self.long_term_strategy = None
        
        # Monitoring
        self.performance_monitor = None
        self.alert_system = None
        self.safety_circuit = None
        
        # API clients
        self.pumpportal_client = None
        self.bitquery_client = None
        
    async def initialize(self):
        """Initialize all bot components"""
        try:
            logger.info("Initializing Enhanced Pump.fun Trading Bot...")
            
            # Initialize API clients
            self.pumpportal_client = PumpPortalClient()
            self.bitquery_client = BitqueryClient()
            
            # Initialize core components
            self.data_processor = DataProcessor(self.pumpportal_client, self.bitquery_client)
            self.wallet_manager = WalletManager()
            self.reputation_manager = ReputationManager()
            self.risk_manager = RiskManager()
            
            # Initialize enhanced components
            self.mev_protection = MEVProtectionModule()
            self.market_analyzer = MarketMicrostructureAnalyzer()
            self.pumpfun_optimizer = PumpFunOptimizer()
            
            # Initialize execution engine with enhanced features
            self.enhanced_execution_engine = EnhancedExecutionEngine(
                self.wallet_manager, 
                self.risk_manager
            )
            
            # Initialize strategies
            self.sniping_strategy = AdvancedSnipingStrategy(self.data_processor)
            self.long_term_strategy = LongTermStrategy(self.data_processor)
            
            # Initialize strategy engine
            self.strategy_engine = StrategyEngine(
                self.sniping_strategy,
                self.long_term_strategy,
                self.enhanced_execution_engine,
                self.risk_manager
            )
            
            # Initialize monitoring
            self.performance_monitor = PerformanceMonitor()
            self.alert_system = AlertSystem()
            self.safety_circuit = SafetyCircuit(
                self.risk_manager,
                self.performance_monitor,
                self.alert_system
            )
            
            # Initialize all components
            await self._initialize_components()
            
            logger.info("Enhanced Pump.fun Trading Bot initialized successfully!")
            
        except Exception as e:
            logger.error(f"Failed to initialize bot: {str(e)}")
            raise
    
    async def _initialize_components(self):
        """Initialize all components in correct order"""
        try:
            # Core components
            await self.data_processor.initialize()
            await self.wallet_manager.initialize()
            await self.reputation_manager.initialize()
            await self.risk_manager.initialize()
            
            # Enhanced components
            await self.mev_protection.initialize()
            await self.market_analyzer.initialize()
            await self.pumpfun_optimizer.initialize()
            await self.enhanced_execution_engine.initialize()
            
            # Strategies
            await self.sniping_strategy.initialize()
            await self.long_term_strategy.initialize()
            await self.strategy_engine.initialize()
            
            # Monitoring
            await self.performance_monitor.initialize()
            await self.alert_system.initialize()
            await self.safety_circuit.initialize()
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            raise
    
    async def start(self):
        """Start the enhanced trading bot"""
        try:
            if self.running:
                logger.warning("Bot is already running")
                return
            
            self.running = True
            logger.info("Starting Enhanced Pump.fun Trading Bot...")
            
            # Start main trading loop
            trading_task = asyncio.create_task(self._main_trading_loop())
            
            # Start monitoring tasks
            monitoring_task = asyncio.create_task(self._monitoring_loop())
            
            # Start safety monitoring
            safety_task = asyncio.create_task(self._safety_monitoring_loop())
            
            # Wait for shutdown signal
            await self.shutdown_event.wait()
            
            # Cancel tasks
            trading_task.cancel()
            monitoring_task.cancel()
            safety_task.cancel()
            
            # Wait for tasks to complete
            await asyncio.gather(trading_task, monitoring_task, safety_task, return_exceptions=True)
            
            logger.info("Enhanced Pump.fun Trading Bot stopped")
            
        except Exception as e:
            logger.error(f"Error in bot main loop: {str(e)}")
            raise
        finally:
            self.running = False
    
    async def _main_trading_loop(self):
        """Enhanced main trading loop"""
        try:
            logger.info("Starting enhanced main trading loop...")
            
            while self.running:
                try:
                    # Check safety circuit
                    safety_status = await self.safety_circuit.get_safety_status()
                    if safety_status['level'] in ['danger', 'emergency']:
                        logger.warning(f"Trading halted due to safety level: {safety_status['level']}")
                        await asyncio.sleep(60)  # Wait before checking again
                        continue
                    
                    # Process new tokens with enhanced analysis
                    await self._process_new_tokens_enhanced()
                    
                    # Process long-term opportunities
                    await self._process_long_term_opportunities()
                    
                    # Update performance metrics
                    await self._update_performance_metrics()
                    
                    # Brief pause before next iteration
                    await asyncio.sleep(1)
                    
                except asyncio.CancelledError:
                    logger.info("Main trading loop cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in main trading loop iteration: {str(e)}")
                    await self.alert_system.send_alert(
                        "high",
                        "trading",
                        f"Main trading loop error: {str(e)}"
                    )
                    await asyncio.sleep(5)  # Brief pause before retry
                    
        except Exception as e:
            logger.error(f"Fatal error in main trading loop: {str(e)}")
            await self.safety_circuit.trigger_emergency_stop("Main trading loop fatal error")
    
    async def _process_new_tokens_enhanced(self):
        """Process new tokens with enhanced analysis"""
        try:
            # Get new tokens from data processor
            new_tokens = await self.data_processor.get_new_tokens()
            
            for token_data in new_tokens:
                try:
                    # Enhanced sniping analysis
                    sniping_analysis = await self.sniping_strategy.analyze_new_token(token_data)
                    
                    if sniping_analysis.recommendation not in ["avoid", "skip"]:
                        # Generate trading signal
                        signal = await self.sniping_strategy.generate_trading_signal(sniping_analysis)
                        
                        if signal:
                            # Execute with enhanced engine
                            execution_result = await self.enhanced_execution_engine.execute_signal_enhanced(
                                signal, token_data
                            )
                            
                            # Log execution result
                            if execution_result.success:
                                logger.info(
                                    f"Enhanced execution successful: {execution_result.execution_id}, "
                                    f"Price: {execution_result.executed_price:.6f}, "
                                    f"Slippage: {execution_result.slippage:.3f}, "
                                    f"MEV Protected: {execution_result.mev_protection_applied}"
                                )
                            else:
                                logger.warning(
                                    f"Enhanced execution failed: {execution_result.execution_id}, "
                                    f"Error: {execution_result.error_message}"
                                )
                            
                            # Update performance tracking
                            await self.performance_monitor.record_trade_execution(execution_result)
                    
                except Exception as e:
                    logger.error(f"Error processing token {token_data.get('mint', 'unknown')}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in enhanced new token processing: {str(e)}")
    
    async def _process_long_term_opportunities(self):
        """Process long-term investment opportunities"""
        try:
            # Get potential long-term investments
            opportunities = await self.data_processor.get_long_term_opportunities()
            
            for opportunity in opportunities:
                try:
                    # Long-term analysis
                    analysis = await self.long_term_strategy.analyze_investment_opportunity(opportunity)
                    
                    if analysis.investment_grade in ["A+", "A", "A-", "B+"]:
                        # Generate investment signal
                        signal = await self.long_term_strategy.generate_investment_signal(analysis)
                        
                        if signal:
                            # Execute with enhanced engine
                            execution_result = await self.enhanced_execution_engine.execute_signal_enhanced(
                                signal, opportunity
                            )
                            
                            # Update performance tracking
                            await self.performance_monitor.record_trade_execution(execution_result)
                    
                except Exception as e:
                    logger.error(f"Error processing long-term opportunity: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in long-term opportunity processing: {str(e)}")
    
    async def _update_performance_metrics(self):
        """Update performance metrics"""
        try:
            # Update strategy performance
            await self.performance_monitor.update_strategy_performance()
            
            # Update wallet performance
            await self.performance_monitor.update_wallet_performance()
            
            # Update overall performance
            await self.performance_monitor.calculate_overall_performance()
            
        except Exception as e:
            logger.error(f"Error updating performance metrics: {str(e)}")
    
    async def _monitoring_loop(self):
        """Enhanced monitoring loop"""
        try:
            logger.info("Starting enhanced monitoring loop...")
            
            while self.running:
                try:
                    # Generate performance reports
                    await self._generate_performance_reports()
                    
                    # Check for alerts
                    await self._check_system_alerts()
                    
                    # Update reputation scores
                    await self._update_reputation_scores()
                    
                    # Monitor enhanced components
                    await self._monitor_enhanced_components()
                    
                    await asyncio.sleep(60)  # Monitor every minute
                    
                except asyncio.CancelledError:
                    logger.info("Monitoring loop cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in monitoring loop: {str(e)}")
                    await asyncio.sleep(30)  # Brief pause before retry
                    
        except Exception as e:
            logger.error(f"Fatal error in monitoring loop: {str(e)}")
    
    async def _safety_monitoring_loop(self):
        """Enhanced safety monitoring loop"""
        try:
            logger.info("Starting enhanced safety monitoring loop...")
            
            while self.running:
                try:
                    # Check safety circuit
                    await self.safety_circuit.check_safety_conditions()
                    
                    # Monitor risk levels
                    await self._monitor_risk_levels()
                    
                    # Check for emergency conditions
                    await self._check_emergency_conditions()
                    
                    await asyncio.sleep(30)  # Check every 30 seconds
                    
                except asyncio.CancelledError:
                    logger.info("Safety monitoring loop cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in safety monitoring: {str(e)}")
                    await asyncio.sleep(15)  # Brief pause before retry
                    
        except Exception as e:
            logger.error(f"Fatal error in safety monitoring: {str(e)}")
    
    async def _generate_performance_reports(self):
        """Generate enhanced performance reports"""
        try:
            # Get comprehensive performance data
            performance_data = await self.performance_monitor.get_comprehensive_performance()
            
            # Get execution engine performance
            execution_summary = self.enhanced_execution_engine.get_execution_summary()
            
            # Get MEV protection stats
            mev_stats = self.mev_protection.get_protection_stats()
            
            # Log enhanced performance summary
            logger.info(
                f"Enhanced Performance Summary - "
                f"Total Return: {performance_data.get('total_return_percent', 0):.2f}%, "
                f"Success Rate: {execution_summary.get('success_rate', 0):.1f}%, "
                f"MEV Protection: {mev_stats.get('mev_attacks_prevented', 0)} attacks prevented, "
                f"Avg Slippage: {execution_summary.get('average_slippage', 0):.3f}"
            )
            
        except Exception as e:
            logger.error(f"Error generating performance reports: {str(e)}")
    
    async def _check_system_alerts(self):
        """Check for system alerts"""
        try:
            # Check for pending alerts
            pending_alerts = await self.alert_system.get_pending_alerts()
            
            for alert in pending_alerts:
                logger.warning(f"System Alert: {alert['severity']} - {alert['message']}")
                
        except Exception as e:
            logger.error(f"Error checking system alerts: {str(e)}")
    
    async def _update_reputation_scores(self):
        """Update wallet reputation scores"""
        try:
            await self.reputation_manager.update_all_reputation_scores()
            
        except Exception as e:
            logger.error(f"Error updating reputation scores: {str(e)}")
    
    async def _monitor_enhanced_components(self):
        """Monitor enhanced component performance"""
        try:
            # Monitor MEV protection effectiveness
            mev_stats = self.mev_protection.get_protection_stats()
            if mev_stats.get('total_protected_transactions', 0) > 0:
                protection_rate = mev_stats.get('mev_attacks_prevented', 0) / mev_stats['total_protected_transactions']
                if protection_rate < 0.8:  # Less than 80% protection rate
                    await self.alert_system.send_alert(
                        "medium",
                        "system",
                        f"MEV protection rate below threshold: {protection_rate:.1%}"
                    )
            
            # Monitor market analyzer performance
            # (Additional monitoring logic would go here)
            
        except Exception as e:
            logger.error(f"Error monitoring enhanced components: {str(e)}")
    
    async def _monitor_risk_levels(self):
        """Monitor risk levels"""
        try:
            current_risk = await self.risk_manager.get_current_risk_level()
            
            if current_risk['level'] == 'high':
                await self.alert_system.send_alert(
                    "high",
                    "risk",
                    f"High risk level detected: {current_risk['reason']}"
                )
                
        except Exception as e:
            logger.error(f"Error monitoring risk levels: {str(e)}")
    
    async def _check_emergency_conditions(self):
        """Check for emergency conditions"""
        try:
            # Check for emergency triggers
            emergency_status = await self.safety_circuit.check_emergency_conditions()
            
            if emergency_status['emergency_triggered']:
                logger.critical(f"Emergency condition detected: {emergency_status['reason']}")
                await self.safety_circuit.trigger_emergency_stop(emergency_status['reason'])
                
        except Exception as e:
            logger.error(f"Error checking emergency conditions: {str(e)}")
    
    async def stop(self):
        """Stop the enhanced trading bot"""
        try:
            logger.info("Stopping Enhanced Pump.fun Trading Bot...")
            
            self.running = False
            self.shutdown_event.set()
            
            # Cleanup components
            await self._cleanup_components()
            
            logger.info("Enhanced Pump.fun Trading Bot stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping bot: {str(e)}")
    
    async def _cleanup_components(self):
        """Cleanup all components"""
        try:
            # Cleanup in reverse order of initialization
            if self.safety_circuit:
                await self.safety_circuit.cleanup()
            
            if self.alert_system:
                await self.alert_system.cleanup()
            
            if self.performance_monitor:
                await self.performance_monitor.cleanup()
            
            if self.strategy_engine:
                await self.strategy_engine.cleanup()
            
            if self.long_term_strategy:
                await self.long_term_strategy.cleanup()
            
            if self.sniping_strategy:
                await self.sniping_strategy.cleanup()
            
            if self.enhanced_execution_engine:
                await self.enhanced_execution_engine.cleanup()
            
            if self.pumpfun_optimizer:
                await self.pumpfun_optimizer.cleanup()
            
            if self.market_analyzer:
                await self.market_analyzer.cleanup()
            
            if self.mev_protection:
                await self.mev_protection.cleanup()
            
            if self.risk_manager:
                await self.risk_manager.cleanup()
            
            if self.reputation_manager:
                await self.reputation_manager.cleanup()
            
            if self.wallet_manager:
                await self.wallet_manager.cleanup()
            
            if self.data_processor:
                await self.data_processor.cleanup()
            
            logger.info("All components cleaned up successfully")
            
        except Exception as e:
            logger.error(f"Error during component cleanup: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get enhanced bot status"""
        try:
            status = {
                'running': self.running,
                'timestamp': datetime.utcnow().isoformat(),
                'components': {
                    'data_processor': bool(self.data_processor),
                    'strategy_engine': bool(self.strategy_engine),
                    'enhanced_execution_engine': bool(self.enhanced_execution_engine),
                    'mev_protection': bool(self.mev_protection),
                    'market_analyzer': bool(self.market_analyzer),
                    'pumpfun_optimizer': bool(self.pumpfun_optimizer),
                    'safety_circuit': bool(self.safety_circuit)
                }
            }
            
            if self.performance_monitor:
                status['performance'] = asyncio.create_task(
                    self.performance_monitor.get_current_performance()
                )
            
            if self.enhanced_execution_engine:
                status['execution_summary'] = self.enhanced_execution_engine.get_execution_summary()
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting bot status: {str(e)}")
            return {'running': self.running, 'error': str(e)}

def signal_handler(bot):
    """Handle shutdown signals"""
    def handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating shutdown...")
        asyncio.create_task(bot.stop())
    return handler

async def main():
    """Enhanced main function"""
    try:
        # Setup logging
        setup_logging()
        
        logger.info("Starting Enhanced Pump.fun Trading Bot...")
        
        # Create and initialize bot
        bot = EnhancedPumpFunTradingBot()
        await bot.initialize()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, signal_handler(bot))
        signal.signal(signal.SIGTERM, signal_handler(bot))
        
        # Start bot
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

