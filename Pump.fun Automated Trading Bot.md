# Pump.fun Automated Trading Bot

A sophisticated automated trading bot for the pump.fun platform on Solana, designed to maximize gains through intelligent new coin sniping and strategic long-term investment approaches.

## Features

### Core Trading Strategies
- **New Coin Sniping**: Automated detection and rapid execution on newly launched tokens
- **Long-term Investment**: Strategic positioning in tokens with strong fundamentals
- **Multi-wallet Management**: Reputation preservation and risk distribution
- **Advanced Risk Controls**: Stop losses, take profits, and position sizing

### Technical Capabilities
- **Real-time Data Processing**: WebSocket integration with PumpPortal and Bitquery APIs
- **Intelligent Signal Generation**: ML-enhanced analysis of token quality and market conditions
- **Comprehensive Monitoring**: Performance tracking, health checks, and alerting
- **Scalable Architecture**: Modular design supporting multiple trading strategies

## Quick Start

### Prerequisites
- Python 3.11+
- Solana CLI tools
- API keys for PumpPortal and Bitquery
- Solana wallet private keys

### Installation

1. Clone and setup:
```bash
git clone <repository-url>
cd pump_fun_bot
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys and wallet private keys
```

3. Run the bot:
```bash
python -m src.main
```

## Configuration

### Required Environment Variables

```bash
# API Keys
PUMPPORTAL_API_KEY=your_pumpportal_api_key
BITQUERY_API_KEY=your_bitquery_api_key

# Wallet Private Keys (keep secure!)
SNIPING_WALLET_PRIVATE_KEY=your_sniping_wallet_key
LONGTERM_WALLET_PRIVATE_KEY=your_longterm_wallet_key

# Trading Parameters
MIN_BUY_AMOUNT=0.015
MAX_BUY_AMOUNT=0.05
STOP_LOSS_PERCENTAGE=10
TAKE_PROFIT_1=25
TAKE_PROFIT_2=50
```

### Trading Strategy Configuration

The bot supports multiple trading strategies that can be enabled/disabled:

- **Sniping Strategy**: Targets newly launched tokens within first 2 minutes
- **Long-term Strategy**: Identifies tokens with sustainable growth potential
- **Copy Trading**: Follows successful trader wallets (optional)
- **Arbitrage**: Cross-platform price differences (optional)

## Architecture

### Core Components

1. **Data Layer** (`src/data/`)
   - PumpPortal API client for real-time data and trading
   - Bitquery client for comprehensive analytics
   - Data processor for market analysis

2. **Trading Engine** (`src/trading/`)
   - Strategy engine for signal generation
   - Execution engine for trade management
   - Risk manager for position controls

3. **Wallet Management** (`src/wallets/`)
   - Multi-wallet coordination
   - Reputation management
   - Security protocols

4. **Monitoring** (`src/monitoring/`)
   - Comprehensive logging
   - Performance metrics
   - Health monitoring

### Data Flow

```
WebSocket Events → Data Processor → Strategy Engine → Execution Engine → Trade Execution
                                        ↓
                                 Risk Manager → Position Monitoring
```

## Trading Strategies

### New Coin Sniping

**Objective**: Capture early price movements in newly launched tokens

**Process**:
1. Monitor WebSocket for new token creation events
2. Analyze token quality using multiple factors:
   - Creator wallet reputation
   - Token metadata quality
   - Initial liquidity setup
3. Generate trading signals with confidence scores
4. Execute trades within 30 seconds to 2 minutes of launch

**Risk Management**:
- Position size: 0.015-0.05 SOL per trade
- Stop loss: 10-15% maximum loss
- Take profit: 25% first level, 50% second level
- Bonding curve exit: 15% progress threshold

### Long-term Investment

**Objective**: Identify tokens with sustainable growth potential

**Analysis Factors**:
- Community growth and engagement
- Developer activity and transparency
- Trading volume and holder distribution
- Market position and competitive advantages

**Position Management**:
- Larger position sizes (up to 2x sniping amounts)
- Higher stop losses (25%) for volatility tolerance
- Multiple take profit levels (100%, 300%, 500%, 1000%)
- Hold duration: 1-30 days depending on performance

### Multi-wallet Strategy

**Wallet Types**:
- **Sniping Wallets**: High-frequency trading, minimal balances
- **Long-term Wallets**: Conservative patterns, reputation building
- **Utility Wallets**: Specialized functions, arbitrage

**Reputation Management**:
- Separate transaction patterns to avoid detection
- Organic-looking trading behavior for long-term wallets
- Community participation and ecosystem engagement

## Risk Management

### Position-Level Controls
- Dynamic position sizing based on market conditions
- Multiple stop-loss mechanisms (hard, trailing, time-based)
- Intelligent take-profit optimization

### Portfolio-Level Controls
- Maximum concentration limits per token
- Correlation analysis for true diversification
- Drawdown protection and circuit breakers

### Operational Controls
- API reliability monitoring and failover
- Security protocols and encrypted key storage
- Compliance monitoring and audit trails

## Monitoring and Alerts

### Performance Tracking
- Real-time P&L monitoring
- Strategy-specific performance metrics
- Win rate and average profit analysis

### System Health
- API connection status
- WebSocket connectivity
- Database and cache performance

### Alerting
- Discord/Slack webhook integration
- Email notifications for critical events
- SMS alerts for emergency situations

## Security Considerations

### Private Key Management
- Environment variable storage only
- No hardcoded keys in source code
- Separate keys for different wallet types

### API Security
- Rate limiting and retry logic
- Secure communication channels
- API key rotation capabilities

### Operational Security
- Comprehensive audit logging
- Access control and authentication
- Regular security assessments

## Performance Optimization

### Execution Speed
- WebSocket connections for real-time data
- Optimized transaction routing
- Priority fee management

### Resource Efficiency
- Connection pooling and reuse
- Intelligent caching strategies
- Asynchronous processing

### Scalability
- Modular architecture for easy expansion
- Database optimization for high throughput
- Load balancing for multiple instances

## Disclaimer

**Important Risk Warning**: This trading bot is designed for educational and research purposes. Cryptocurrency trading involves substantial risk and can result in significant financial losses. Users should:

- Never invest more than they can afford to lose
- Thoroughly test the bot with small amounts before scaling
- Understand that past performance does not guarantee future results
- Comply with all applicable laws and regulations
- Use appropriate risk management settings

The developers are not responsible for any financial losses incurred through the use of this software.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Join our Discord community
- Review the documentation wiki

## Roadmap

### Phase 1 (Current)
- ✅ Core trading engine implementation
- ✅ PumpPortal and Bitquery API integration
- ✅ Basic sniping and long-term strategies
- ✅ Multi-wallet management framework

### Phase 2 (Next)
- [ ] Advanced execution engine with Solana integration
- [ ] Machine learning enhanced signal generation
- [ ] Copy trading implementation
- [ ] Web dashboard for monitoring and control

### Phase 3 (Future)
- [ ] Cross-platform arbitrage strategies
- [ ] Advanced social sentiment analysis
- [ ] Mobile app for remote monitoring
- [ ] Community features and signal sharing

