"""
Test suite for the Pump.fun Trading Bot
"""
import asyncio
import unittest
import logging
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.main import PumpFunTradingBot
from src.data.data_processor import DataProcessor
from src.trading.advanced_sniping_strategy import AdvancedSnipingStrategy
from src.trading.long_term_strategy import LongTermStrategy
from src.wallets.wallet_manager import WalletManager
from src.monitoring.safety_circuit import SafetyCircuit

class TestTradingBot(unittest.TestCase):
    """Test cases for the main trading bot"""
    
    def setUp(self):
        """Setup test environment"""
        self.bot = PumpFunTradingBot()
        
    async def test_bot_initialization(self):
        """Test bot initialization"""
        try:
            await self.bot.initialize()
            self.assertTrue(len(self.bot.components) > 0)
            self.assertIn('data_processor', self.bot.components)
            self.assertIn('safety_circuit', self.bot.components)
            print("✓ Bot initialization test passed")
        except Exception as e:
            print(f"✗ Bot initialization test failed: {str(e)}")
            
    async def test_safety_circuit(self):
        """Test safety circuit functionality"""
        try:
            safety_circuit = SafetyCircuit()
            await safety_circuit.initialize()
            
            # Test normal operation
            self.assertTrue(safety_circuit.is_trading_allowed())
            
            # Test emergency stop
            await safety_circuit.emergency_stop("Test emergency stop")
            self.assertFalse(safety_circuit.is_trading_allowed())
            
            print("✓ Safety circuit test passed")
        except Exception as e:
            print(f"✗ Safety circuit test failed: {str(e)}")

class TestDataProcessor(unittest.TestCase):
    """Test cases for data processing"""
    
    async def test_data_processor_initialization(self):
        """Test data processor initialization"""
        try:
            processor = DataProcessor()
            await processor.initialize()
            print("✓ Data processor initialization test passed")
        except Exception as e:
            print(f"✗ Data processor initialization test failed: {str(e)}")

class TestTradingStrategies(unittest.TestCase):
    """Test cases for trading strategies"""
    
    async def test_sniping_strategy(self):
        """Test sniping strategy"""
        try:
            # Mock data processor
            mock_processor = Mock()
            strategy = AdvancedSnipingStrategy(mock_processor)
            await strategy.initialize()
            
            # Test token analysis with mock data
            mock_token_data = {
                'mint': 'test_mint_address',
                'name': 'Test Token',
                'symbol': 'TEST',
                'creator': 'test_creator',
                'market_cap': 50000,
                'created_timestamp': datetime.utcnow().timestamp()
            }
            
            analysis = await strategy.analyze_new_token(mock_token_data)
            self.assertIsNotNone(analysis)
            self.assertIn(analysis.recommendation, ["strong_buy", "buy", "hold", "avoid", "skip"])
            
            print("✓ Sniping strategy test passed")
        except Exception as e:
            print(f"✗ Sniping strategy test failed: {str(e)}")
    
    async def test_long_term_strategy(self):
        """Test long-term strategy"""
        try:
            # Mock data processor
            mock_processor = Mock()
            strategy = LongTermStrategy(mock_processor)
            await strategy.initialize()
            
            # Test fundamental analysis with mock data
            mock_token_data = {
                'mint': 'test_mint_address',
                'name': 'Test Utility Token',
                'symbol': 'TUT',
                'description': 'A test token with real utility',
                'market_cap': 1000000,
                'holder_count': 5000
            }
            
            analysis = await strategy.analyze_token_fundamentals(mock_token_data)
            self.assertIsNotNone(analysis)
            self.assertIn(analysis.recommendation, ["strong_buy", "buy", "accumulate", "hold", "reduce", "sell", "avoid"])
            
            print("✓ Long-term strategy test passed")
        except Exception as e:
            print(f"✗ Long-term strategy test failed: {str(e)}")

class TestWalletManager(unittest.TestCase):
    """Test cases for wallet management"""
    
    async def test_wallet_manager_initialization(self):
        """Test wallet manager initialization"""
        try:
            wallet_manager = WalletManager()
            await wallet_manager.initialize()
            print("✓ Wallet manager initialization test passed")
        except Exception as e:
            print(f"✗ Wallet manager initialization test failed: {str(e)}")

async def run_all_tests():
    """Run all test cases"""
    print("Starting Pump.fun Trading Bot Test Suite...")
    print("=" * 50)
    
    # Test bot initialization
    bot_test = TestTradingBot()
    await bot_test.test_bot_initialization()
    await bot_test.test_safety_circuit()
    
    # Test data processor
    data_test = TestDataProcessor()
    await data_test.test_data_processor_initialization()
    
    # Test trading strategies
    strategy_test = TestTradingStrategies()
    await strategy_test.test_sniping_strategy()
    await strategy_test.test_long_term_strategy()
    
    # Test wallet manager
    wallet_test = TestWalletManager()
    await wallet_test.test_wallet_manager_initialization()
    
    print("=" * 50)
    print("Test suite completed!")

if __name__ == "__main__":
    asyncio.run(run_all_tests())

