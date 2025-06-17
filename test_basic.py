"""
Simple test script for the Pump.fun Trading Bot
"""
import asyncio
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

async def test_imports():
    """Test that all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from src.config.settings import settings
        print("✓ Settings import successful")
    except Exception as e:
        print(f"✗ Settings import failed: {str(e)}")
    
    try:
        from src.data.data_processor import DataProcessor
        print("✓ DataProcessor import successful")
    except Exception as e:
        print(f"✗ DataProcessor import failed: {str(e)}")
    
    try:
        from src.trading.strategy_engine import StrategyEngine
        print("✓ StrategyEngine import successful")
    except Exception as e:
        print(f"✗ StrategyEngine import failed: {str(e)}")
    
    try:
        from src.wallets.wallet_manager import WalletManager
        print("✓ WalletManager import successful")
    except Exception as e:
        print(f"✗ WalletManager import failed: {str(e)}")
    
    try:
        from src.monitoring.safety_circuit import SafetyCircuit
        print("✓ SafetyCircuit import successful")
    except Exception as e:
        print(f"✗ SafetyCircuit import failed: {str(e)}")

async def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        from src.monitoring.safety_circuit import SafetyCircuit, SafetyLevel
        
        # Test safety circuit
        safety = SafetyCircuit()
        print(f"✓ SafetyCircuit created, initial state: {safety.safety_level}")
        
        # Test safety status
        status = safety.get_safety_status()
        print(f"✓ Safety status retrieved: {status.get('safety_level', 'unknown')}")
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {str(e)}")

async def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from src.config.settings import settings
        
        # Test that settings can be accessed
        api_key = getattr(settings, 'PUMPPORTAL_API_KEY', 'not_set')
        print(f"✓ Configuration loaded, API key status: {'set' if api_key != 'not_set' else 'not set'}")
        
    except Exception as e:
        print(f"✗ Configuration test failed: {str(e)}")

async def main():
    """Main test function"""
    print("Pump.fun Trading Bot - Basic Test Suite")
    print("=" * 50)
    
    await test_imports()
    await test_basic_functionality()
    await test_configuration()
    
    print("\n" + "=" * 50)
    print("Basic tests completed!")
    print("\nNote: For full functionality, you'll need to:")
    print("1. Copy .env.example to .env and configure API keys")
    print("2. Set up wallet private keys (securely)")
    print("3. Configure trading parameters")
    print("4. Test with small amounts first")

if __name__ == "__main__":
    asyncio.run(main())

