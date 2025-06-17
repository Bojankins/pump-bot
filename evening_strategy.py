"""
Evening Trading Strategy Tool - Optimized for tonight's session
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class EveningTradingStrategy:
    """Specialized trading strategy for evening sessions"""
    
    def __init__(self):
        self.session_config = {
            'risk_per_trade': 0.02,  # 2% per trade (conservative for evening)
            'max_trades': 3,         # Limit exposure
            'stop_loss': -0.15,      # 15% stop loss
            'take_profit_1': 0.25,   # 25% first target
            'take_profit_2': 0.50,   # 50% second target
            'moon_bag': 0.20,        # 20% for potential 5-10x
            'session_duration': 4    # 4 hour session
        }
        
        self.active_positions = {}
        self.session_stats = {
            'trades_executed': 0,
            'successful_trades': 0,
            'total_pnl': 0.0,
            'session_start': None
        }
    
    def start_evening_session(self, account_balance: float, risk_tolerance: str = 'moderate'):
        """Start evening trading session"""
        try:
            self.session_stats['session_start'] = datetime.utcnow()
            
            # Adjust config based on risk tolerance
            if risk_tolerance == 'conservative':
                self.session_config['risk_per_trade'] = 0.015  # 1.5%
                self.session_config['max_trades'] = 2
                self.session_config['stop_loss'] = -0.10  # 10%
            elif risk_tolerance == 'aggressive':
                self.session_config['risk_per_trade'] = 0.03  # 3%
                self.session_config['max_trades'] = 5
                self.session_config['stop_loss'] = -0.20  # 20%
            
            # Calculate position sizes
            self.position_size = account_balance * self.session_config['risk_per_trade']
            
            logger.info(f"Evening session started - Risk: {risk_tolerance}, Position size: {self.position_size:.2f} SOL")
            
            return {
                'session_id': f"evening_{int(datetime.utcnow().timestamp())}",
                'config': self.session_config,
                'position_size': self.position_size,
                'max_exposure': self.position_size * self.session_config['max_trades']
            }
            
        except Exception as e:
            logger.error(f"Error starting evening session: {str(e)}")
            return None
    
    def evaluate_entry_opportunity(self, opportunity_signal) -> Dict[str, Any]:
        """Evaluate if we should enter a position"""
        try:
            # Check if we can take more positions
            if len(self.active_positions) >= self.session_config['max_trades']:
                return {
                    'should_enter': False,
                    'reason': 'Maximum positions reached'
                }
            
            # Check opportunity quality
            if opportunity_signal.overall_score < 7.5:
                return {
                    'should_enter': False,
                    'reason': 'Score below threshold'
                }
            
            # Check risk level
            if opportunity_signal.risk_level in ['high', 'very_high']:
                return {
                    'should_enter': False,
                    'reason': 'Risk level too high for evening session'
                }
            
            # Check time sensitivity
            if opportunity_signal.time_sensitivity == 'very_high':
                # High urgency - reduce position size
                position_size = self.position_size * 0.7
            else:
                position_size = self.position_size
            
            # Calculate stop loss and take profit levels
            entry_price = 0.001  # Placeholder - would get from market data
            stop_loss_price = entry_price * (1 + self.session_config['stop_loss'])
            take_profit_1_price = entry_price * (1 + self.session_config['take_profit_1'])
            take_profit_2_price = entry_price * (1 + self.session_config['take_profit_2'])
            
            return {
                'should_enter': True,
                'position_size': position_size,
                'entry_price': entry_price,
                'stop_loss': stop_loss_price,
                'take_profit_1': take_profit_1_price,
                'take_profit_2': take_profit_2_price,
                'confidence': opportunity_signal.confidence_level,
                'expected_return': opportunity_signal.potential_return
            }
            
        except Exception as e:
            logger.error(f"Error evaluating entry opportunity: {str(e)}")
            return {'should_enter': False, 'reason': 'Evaluation error'}
    
    def manage_position(self, mint_address: str, current_price: float) -> Dict[str, Any]:
        """Manage existing position"""
        try:
            if mint_address not in self.active_positions:
                return {'action': 'none', 'reason': 'Position not found'}
            
            position = self.active_positions[mint_address]
            entry_price = position['entry_price']
            current_pnl_percent = (current_price - entry_price) / entry_price
            
            # Check stop loss
            if current_price <= position['stop_loss']:
                return {
                    'action': 'close_all',
                    'reason': 'Stop loss triggered',
                    'pnl_percent': current_pnl_percent
                }
            
            # Check take profit levels
            if current_price >= position['take_profit_2'] and position['size'] > 0.2:
                # Take profit at second level - sell 60% more
                return {
                    'action': 'partial_close',
                    'close_percent': 0.6,
                    'reason': 'Take profit 2 reached',
                    'pnl_percent': current_pnl_percent
                }
            elif current_price >= position['take_profit_1'] and position['size'] > 0.5:
                # Take profit at first level - sell 50%
                return {
                    'action': 'partial_close',
                    'close_percent': 0.5,
                    'reason': 'Take profit 1 reached',
                    'pnl_percent': current_pnl_percent
                }
            
            # Check for trailing stop (if in profit)
            if current_pnl_percent > 0.1:  # 10% profit
                # Implement trailing stop
                trailing_stop = current_price * 0.9  # 10% trailing stop
                if trailing_stop > position['stop_loss']:
                    position['stop_loss'] = trailing_stop
                    return {
                        'action': 'update_stop',
                        'new_stop': trailing_stop,
                        'reason': 'Trailing stop updated'
                    }
            
            return {
                'action': 'hold',
                'current_pnl_percent': current_pnl_percent,
                'unrealized_pnl': position['size'] * current_pnl_percent
            }
            
        except Exception as e:
            logger.error(f"Error managing position: {str(e)}")
            return {'action': 'none', 'reason': 'Management error'}
    
    def get_evening_strategy_tips(self) -> List[str]:
        """Get strategy tips for evening trading"""
        return [
            "🕐 Prime Hours: 6-11 PM EST for highest activity",
            "💰 Position Size: 2% risk per trade maximum",
            "🛑 Stop Losses: Tight 15% stops for evening volatility",
            "🎯 Take Profits: 25% and 50% targets, keep 20% moon bag",
            "📊 Quality Focus: Only trade 7.5+ score opportunities",
            "⚠️ Risk Management: Max 3 positions simultaneously",
            "🐋 Watch Whales: Follow smart money movements",
            "⏰ Time Limits: 4-hour session maximum",
            "📱 Stay Alert: Evening can be volatile",
            "💎 Moon Bags: Let 20% ride for potential 5-10x"
        ]
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get current session summary"""
        try:
            if not self.session_stats['session_start']:
                return {'status': 'No active session'}
            
            session_duration = datetime.utcnow() - self.session_stats['session_start']
            
            # Calculate win rate
            win_rate = 0.0
            if self.session_stats['trades_executed'] > 0:
                win_rate = self.session_stats['successful_trades'] / self.session_stats['trades_executed'] * 100
            
            return {
                'session_duration_minutes': session_duration.total_seconds() / 60,
                'trades_executed': self.session_stats['trades_executed'],
                'successful_trades': self.session_stats['successful_trades'],
                'win_rate_percent': win_rate,
                'total_pnl': self.session_stats['total_pnl'],
                'active_positions': len(self.active_positions),
                'remaining_capacity': self.session_config['max_trades'] - len(self.active_positions),
                'session_config': self.session_config
            }
            
        except Exception as e:
            logger.error(f"Error getting session summary: {str(e)}")
            return {'error': str(e)}

def print_evening_trading_guide():
    """Print comprehensive evening trading guide"""
    print("🌙 EVENING TRADING STRATEGY GUIDE")
    print("=" * 50)
    print()
    
    print("⏰ OPTIMAL TIMING:")
    print("• 6:00-7:00 PM: Setup and scanning phase")
    print("• 7:00-9:00 PM: Prime retail activity window")
    print("• 9:00-11:00 PM: Whale activity increases")
    print("• 11:00 PM+: Late night pumps (higher risk)")
    print()
    
    print("💰 POSITION SIZING:")
    print("• Conservative: 1.5% per trade, max 2 positions")
    print("• Moderate: 2% per trade, max 3 positions")
    print("• Aggressive: 3% per trade, max 5 positions")
    print()
    
    print("🎯 ENTRY CRITERIA:")
    print("• Overall score: 7.5+ out of 10")
    print("• Risk level: Low to Medium only")
    print("• Developer risk: Below 3.0")
    print("• Liquidity quality: Good or Excellent")
    print("• Whale sentiment: Neutral to Bullish")
    print()
    
    print("🛑 EXIT STRATEGY:")
    print("• Stop Loss: 15% (tight for evening volatility)")
    print("• Take Profit 1: 25% (sell 50% of position)")
    print("• Take Profit 2: 50% (sell additional 30%)")
    print("• Moon Bag: Keep 20% for potential 5-10x")
    print()
    
    print("⚠️ RISK MANAGEMENT:")
    print("• Maximum 3 simultaneous positions")
    print("• Session limit: 4 hours maximum")
    print("• Daily loss limit: 6% of account")
    print("• Trailing stops: 10% when in 10%+ profit")
    print()
    
    print("🔍 WHAT TO LOOK FOR TONIGHT:")
    print("• New tokens with strong fundamentals")
    print("• Bonding curve progress: 10-70%")
    print("• Active developer engagement")
    print("• Growing community metrics")
    print("• Whale accumulation patterns")
    print()
    
    print("🚫 RED FLAGS TO AVOID:")
    print("• Copy-paste projects")
    print("• Anonymous developers")
    print("• Suspicious funding patterns")
    print("• Poor liquidity conditions")
    print("• Late-stage bonding curve (>90%)")
    print()
    
    print("📊 SUCCESS METRICS:")
    print("• Win rate target: 60%+")
    print("• Average return per trade: 30%+")
    print("• Maximum drawdown: <10%")
    print("• Risk-adjusted returns: Positive Sharpe ratio")
    print()
    
    print("💡 PRO TIPS:")
    print("• Start small to test the enhanced system")
    print("• Use the opportunity scanner for real-time alerts")
    print("• Follow whale wallets for early signals")
    print("• Take profits systematically - don't get greedy")
    print("• Keep detailed records for continuous improvement")
    print()
    
    print("⚠️ DISCLAIMER: This is educational content only.")
    print("Always do your own research and never invest more than you can afford to lose!")

# Example usage
if __name__ == "__main__":
    print_evening_trading_guide()
    print()
    
    # Example session
    strategy = EveningTradingStrategy()
    session = strategy.start_evening_session(100.0, 'moderate')  # 100 SOL account
    
    print("🎮 EXAMPLE EVENING SESSION:")
    print(f"Position Size: {session['position_size']:.2f} SOL")
    print(f"Max Exposure: {session['max_exposure']:.2f} SOL")
    print(f"Max Trades: {session['config']['max_trades']}")
    print()
    
    tips = strategy.get_evening_strategy_tips()
    print("💡 EVENING STRATEGY TIPS:")
    for tip in tips:
        print(f"  {tip}")

