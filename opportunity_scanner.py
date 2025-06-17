"""
Opportunity Scanner - Real-time scanning tool for high-potential pump.fun opportunities
"""
import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import json
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OpportunitySignal:
    """Opportunity signal data structure"""
    mint_address: str
    token_name: str
    overall_score: float
    risk_level: str
    potential_return: float
    confidence_level: float
    time_sensitivity: str
    entry_recommendation: str
    key_factors: List[str]
    risk_factors: List[str]
    timestamp: datetime

class OpportunityScanner:
    """Real-time opportunity scanner for pump.fun"""
    
    def __init__(self, data_processor, sniping_strategy, pumpfun_optimizer, market_analyzer):
        self.data_processor = data_processor
        self.sniping_strategy = sniping_strategy
        self.pumpfun_optimizer = pumpfun_optimizer
        self.market_analyzer = market_analyzer
        
        # Scanning configuration
        self.min_score_threshold = 7.0
        self.max_rug_risk = 3.0
        self.min_confidence = 0.6
        self.scan_interval = 30  # seconds
        
        # Opportunity tracking
        self.active_opportunities = {}
        self.opportunity_history = []
        self.scanning_active = False
        
    async def start_scanning(self, config: Dict[str, Any] = None):
        """Start real-time opportunity scanning"""
        try:
            if config:
                self._update_config(config)
            
            self.scanning_active = True
            logger.info("Starting opportunity scanner...")
            
            # Start scanning loop
            asyncio.create_task(self._scanning_loop())
            
        except Exception as e:
            logger.error(f"Error starting opportunity scanner: {str(e)}")
            raise
    
    def _update_config(self, config: Dict[str, Any]):
        """Update scanner configuration"""
        self.min_score_threshold = config.get('min_score_threshold', 7.0)
        self.max_rug_risk = config.get('max_rug_risk', 3.0)
        self.min_confidence = config.get('min_confidence', 0.6)
        self.scan_interval = config.get('scan_interval', 30)
    
    async def _scanning_loop(self):
        """Main scanning loop"""
        try:
            while self.scanning_active:
                try:
                    # Scan for new opportunities
                    opportunities = await self._scan_for_opportunities()
                    
                    # Process and rank opportunities
                    ranked_opportunities = await self._rank_opportunities(opportunities)
                    
                    # Update active opportunities
                    await self._update_active_opportunities(ranked_opportunities)
                    
                    # Log top opportunities
                    await self._log_top_opportunities(ranked_opportunities)
                    
                    await asyncio.sleep(self.scan_interval)
                    
                except Exception as e:
                    logger.error(f"Error in scanning loop: {str(e)}")
                    await asyncio.sleep(10)  # Brief pause before retry
                    
        except asyncio.CancelledError:
            logger.info("Opportunity scanning cancelled")
        except Exception as e:
            logger.error(f"Fatal error in scanning loop: {str(e)}")
    
    async def _scan_for_opportunities(self) -> List[Dict[str, Any]]:
        """Scan for new opportunities"""
        try:
            # Get new tokens
            new_tokens = await self.data_processor.get_new_tokens()
            
            opportunities = []
            
            for token in new_tokens:
                try:
                    # Skip if already analyzed recently
                    if self._recently_analyzed(token.get('mint', '')):
                        continue
                    
                    # Perform comprehensive analysis
                    opportunity = await self._analyze_token_opportunity(token)
                    
                    if opportunity and self._meets_criteria(opportunity):
                        opportunities.append(opportunity)
                        
                except Exception as e:
                    logger.error(f"Error analyzing token {token.get('mint', 'unknown')}: {str(e)}")
                    continue
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error scanning for opportunities: {str(e)}")
            return []
    
    async def _analyze_token_opportunity(self, token_data: Dict[str, Any]) -> Optional[OpportunitySignal]:
        """Analyze a single token for opportunity potential"""
        try:
            mint_address = token_data.get('mint', '')
            
            # Enhanced sniping analysis
            sniping_analysis = await self.sniping_strategy.analyze_new_token(token_data)
            
            # Pump.fun specific metrics
            pump_metrics = await self.pumpfun_optimizer.get_pump_fun_metrics(token_data)
            
            # Developer analysis
            dev_analysis = await self.pumpfun_optimizer.analyze_dev_behavior(token_data)
            
            # Market conditions
            market_conditions = await self.market_analyzer.predict_price_movement(
                mint_address, 1.0  # 1 SOL trade size for analysis
            )
            
            # Calculate overall opportunity score
            opportunity_score = await self._calculate_opportunity_score(
                sniping_analysis, pump_metrics, dev_analysis, market_conditions
            )
            
            # Determine risk level
            risk_level = self._determine_risk_level(pump_metrics, dev_analysis)
            
            # Calculate potential return
            potential_return = await self._estimate_potential_return(
                token_data, sniping_analysis, pump_metrics
            )
            
            # Determine time sensitivity
            time_sensitivity = self._assess_time_sensitivity(
                sniping_analysis, pump_metrics, market_conditions
            )
            
            # Generate entry recommendation
            entry_recommendation = self._generate_entry_recommendation(
                opportunity_score, risk_level, market_conditions
            )
            
            # Identify key factors
            key_factors = self._identify_key_factors(
                sniping_analysis, pump_metrics, dev_analysis
            )
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(
                sniping_analysis, pump_metrics, dev_analysis
            )
            
            return OpportunitySignal(
                mint_address=mint_address,
                token_name=token_data.get('name', 'Unknown'),
                overall_score=opportunity_score,
                risk_level=risk_level,
                potential_return=potential_return,
                confidence_level=sniping_analysis.confidence_level,
                time_sensitivity=time_sensitivity,
                entry_recommendation=entry_recommendation,
                key_factors=key_factors,
                risk_factors=risk_factors,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error analyzing token opportunity: {str(e)}")
            return None
    
    async def _calculate_opportunity_score(self, sniping_analysis, pump_metrics, dev_analysis, market_conditions) -> float:
        """Calculate comprehensive opportunity score"""
        try:
            # Base score from sniping analysis
            base_score = sniping_analysis.overall_score
            
            # Adjust for pump.fun metrics
            if pump_metrics.migration_probability > 0.8:
                base_score += 0.5
            elif pump_metrics.migration_probability < 0.3:
                base_score -= 1.0
            
            # Adjust for developer risk
            dev_risk = dev_analysis.get('risk_score', 5.0)
            if dev_risk < 2.0:
                base_score += 0.5
            elif dev_risk > 7.0:
                base_score -= 2.0
            
            # Adjust for market conditions
            liquidity_quality = market_conditions.get('liquidity_quality', 'unknown')
            if liquidity_quality == 'excellent':
                base_score += 0.3
            elif liquidity_quality == 'poor':
                base_score -= 0.5
            
            # Adjust for whale sentiment
            whale_sentiment = market_conditions.get('whale_sentiment', 'neutral')
            if whale_sentiment == 'bullish':
                base_score += 0.3
            elif whale_sentiment == 'bearish':
                base_score -= 0.5
            
            return max(0.0, min(10.0, base_score))
            
        except Exception as e:
            logger.error(f"Error calculating opportunity score: {str(e)}")
            return 0.0
    
    def _determine_risk_level(self, pump_metrics, dev_analysis) -> str:
        """Determine overall risk level"""
        try:
            rug_risk = pump_metrics.rug_risk_score
            dev_risk_level = dev_analysis.get('risk_level', 'unknown')
            
            if rug_risk < 2.0 and dev_risk_level in ['very_low', 'low']:
                return 'low'
            elif rug_risk < 4.0 and dev_risk_level in ['very_low', 'low', 'medium']:
                return 'medium'
            elif rug_risk < 6.0:
                return 'high'
            else:
                return 'very_high'
                
        except Exception as e:
            logger.error(f"Error determining risk level: {str(e)}")
            return 'unknown'
    
    async def _estimate_potential_return(self, token_data, sniping_analysis, pump_metrics) -> float:
        """Estimate potential return percentage"""
        try:
            # Base potential from bonding curve progress
            bonding_progress = pump_metrics.bonding_curve_progress
            base_potential = (1.0 - bonding_progress) * 200  # Up to 200% to graduation
            
            # Adjust for token quality
            quality_multiplier = sniping_analysis.overall_score / 10.0
            
            # Adjust for migration probability
            migration_multiplier = pump_metrics.migration_probability
            
            # Calculate potential return
            potential_return = base_potential * quality_multiplier * migration_multiplier
            
            # Add post-graduation potential if high quality
            if sniping_analysis.overall_score > 8.0 and pump_metrics.migration_probability > 0.8:
                potential_return += 100  # Additional 100% post-graduation potential
            
            return min(potential_return, 1000)  # Cap at 1000%
            
        except Exception as e:
            logger.error(f"Error estimating potential return: {str(e)}")
            return 0.0
    
    def _assess_time_sensitivity(self, sniping_analysis, pump_metrics, market_conditions) -> str:
        """Assess time sensitivity of opportunity"""
        try:
            bonding_progress = pump_metrics.bonding_curve_progress
            whale_sentiment = market_conditions.get('whale_sentiment', 'neutral')
            
            if bonding_progress > 0.8:
                return 'very_high'  # Near graduation
            elif bonding_progress > 0.6 and whale_sentiment == 'bullish':
                return 'high'
            elif whale_sentiment == 'bullish':
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error assessing time sensitivity: {str(e)}")
            return 'unknown'
    
    def _generate_entry_recommendation(self, score, risk_level, market_conditions) -> str:
        """Generate entry recommendation"""
        try:
            exec_recommendation = market_conditions.get('execution_recommendation', 'execute_with_caution')
            
            if score >= 8.5 and risk_level in ['low', 'medium'] and exec_recommendation != 'wait_for_better_liquidity':
                return 'strong_buy'
            elif score >= 7.5 and risk_level in ['low', 'medium']:
                return 'buy'
            elif score >= 6.5 and risk_level == 'low':
                return 'consider'
            elif score >= 5.0:
                return 'monitor'
            else:
                return 'avoid'
                
        except Exception as e:
            logger.error(f"Error generating entry recommendation: {str(e)}")
            return 'monitor'
    
    def _identify_key_factors(self, sniping_analysis, pump_metrics, dev_analysis) -> List[str]:
        """Identify key positive factors"""
        factors = []
        
        try:
            if sniping_analysis.overall_score > 8.0:
                factors.append("High quality token analysis")
            
            if pump_metrics.migration_probability > 0.8:
                factors.append("High migration probability")
            
            if pump_metrics.rug_risk_score < 2.0:
                factors.append("Very low rug risk")
            
            if dev_analysis.get('risk_level') == 'very_low':
                factors.append("Trusted developer")
            
            if pump_metrics.community_engagement > 0.7:
                factors.append("Strong community engagement")
            
            if 0.1 < pump_metrics.bonding_curve_progress < 0.7:
                factors.append("Optimal bonding curve position")
            
        except Exception as e:
            logger.error(f"Error identifying key factors: {str(e)}")
        
        return factors
    
    def _identify_risk_factors(self, sniping_analysis, pump_metrics, dev_analysis) -> List[str]:
        """Identify key risk factors"""
        factors = []
        
        try:
            if pump_metrics.rug_risk_score > 6.0:
                factors.append("High rug pull risk")
            
            if dev_analysis.get('risk_level') in ['high', 'very_high']:
                factors.append("Risky developer profile")
            
            if pump_metrics.migration_probability < 0.3:
                factors.append("Low migration probability")
            
            if pump_metrics.bonding_curve_progress > 0.9:
                factors.append("Late stage entry risk")
            
            if sniping_analysis.confidence_level < 0.5:
                factors.append("Low analysis confidence")
            
            if len(sniping_analysis.red_flags) > 2:
                factors.append("Multiple red flags detected")
            
        except Exception as e:
            logger.error(f"Error identifying risk factors: {str(e)}")
        
        return factors
    
    def _meets_criteria(self, opportunity: OpportunitySignal) -> bool:
        """Check if opportunity meets scanning criteria"""
        try:
            return (
                opportunity.overall_score >= self.min_score_threshold and
                opportunity.confidence_level >= self.min_confidence and
                opportunity.risk_level != 'very_high'
            )
            
        except Exception as e:
            logger.error(f"Error checking criteria: {str(e)}")
            return False
    
    def _recently_analyzed(self, mint_address: str) -> bool:
        """Check if token was recently analyzed"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=10)
            
            for opportunity in self.opportunity_history:
                if (opportunity.mint_address == mint_address and 
                    opportunity.timestamp > cutoff_time):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking recent analysis: {str(e)}")
            return False
    
    async def _rank_opportunities(self, opportunities: List[OpportunitySignal]) -> List[OpportunitySignal]:
        """Rank opportunities by potential"""
        try:
            # Sort by overall score, then by potential return
            ranked = sorted(
                opportunities,
                key=lambda x: (x.overall_score, x.potential_return),
                reverse=True
            )
            
            return ranked[:10]  # Return top 10
            
        except Exception as e:
            logger.error(f"Error ranking opportunities: {str(e)}")
            return opportunities
    
    async def _update_active_opportunities(self, opportunities: List[OpportunitySignal]):
        """Update active opportunities tracking"""
        try:
            # Add new opportunities
            for opportunity in opportunities:
                self.active_opportunities[opportunity.mint_address] = opportunity
            
            # Remove old opportunities (older than 1 hour)
            cutoff_time = datetime.utcnow() - timedelta(hours=1)
            expired_addresses = [
                addr for addr, opp in self.active_opportunities.items()
                if opp.timestamp < cutoff_time
            ]
            
            for addr in expired_addresses:
                del self.active_opportunities[addr]
            
            # Update history
            self.opportunity_history.extend(opportunities)
            
            # Keep only recent history
            if len(self.opportunity_history) > 1000:
                self.opportunity_history = self.opportunity_history[-1000:]
                
        except Exception as e:
            logger.error(f"Error updating active opportunities: {str(e)}")
    
    async def _log_top_opportunities(self, opportunities: List[OpportunitySignal]):
        """Log top opportunities"""
        try:
            if not opportunities:
                return
            
            logger.info(f"Found {len(opportunities)} high-potential opportunities:")
            
            for i, opp in enumerate(opportunities[:5], 1):
                logger.info(
                    f"{i}. {opp.token_name} ({opp.mint_address[:8]}...) - "
                    f"Score: {opp.overall_score:.1f}, "
                    f"Risk: {opp.risk_level}, "
                    f"Potential: {opp.potential_return:.0f}%, "
                    f"Recommendation: {opp.entry_recommendation}"
                )
                
        except Exception as e:
            logger.error(f"Error logging opportunities: {str(e)}")
    
    def get_top_opportunities(self, limit: int = 5) -> List[OpportunitySignal]:
        """Get current top opportunities"""
        try:
            # Sort active opportunities by score
            sorted_opportunities = sorted(
                self.active_opportunities.values(),
                key=lambda x: x.overall_score,
                reverse=True
            )
            
            return sorted_opportunities[:limit]
            
        except Exception as e:
            logger.error(f"Error getting top opportunities: {str(e)}")
            return []
    
    def get_opportunity_summary(self) -> Dict[str, Any]:
        """Get opportunity scanning summary"""
        try:
            active_count = len(self.active_opportunities)
            
            if active_count == 0:
                return {
                    'active_opportunities': 0,
                    'top_score': 0.0,
                    'average_score': 0.0,
                    'risk_distribution': {},
                    'scanning_active': self.scanning_active
                }
            
            scores = [opp.overall_score for opp in self.active_opportunities.values()]
            risk_levels = [opp.risk_level for opp in self.active_opportunities.values()]
            
            risk_distribution = {}
            for risk in risk_levels:
                risk_distribution[risk] = risk_distribution.get(risk, 0) + 1
            
            return {
                'active_opportunities': active_count,
                'top_score': max(scores),
                'average_score': sum(scores) / len(scores),
                'risk_distribution': risk_distribution,
                'scanning_active': self.scanning_active,
                'last_scan': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting opportunity summary: {str(e)}")
            return {}
    
    def stop_scanning(self):
        """Stop opportunity scanning"""
        self.scanning_active = False
        logger.info("Opportunity scanning stopped")

# Example usage function
async def run_opportunity_scanner_example():
    """Example of how to use the opportunity scanner"""
    try:
        # This would be initialized with actual components
        # scanner = OpportunityScanner(data_processor, sniping_strategy, pumpfun_optimizer, market_analyzer)
        
        # Configuration for tonight's session
        config = {
            'min_score_threshold': 7.0,
            'max_rug_risk': 3.0,
            'min_confidence': 0.6,
            'scan_interval': 30
        }
        
        # Start scanning
        # await scanner.start_scanning(config)
        
        # Get top opportunities
        # top_opportunities = scanner.get_top_opportunities(5)
        
        # Print opportunities
        print("🎯 TOP OPPORTUNITIES FOR TONIGHT:")
        print("=" * 50)
        
        # Example opportunity data
        example_opportunities = [
            {
                'name': 'EXAMPLE1',
                'score': 8.7,
                'risk': 'low',
                'potential': 180,
                'recommendation': 'strong_buy',
                'factors': ['High quality analysis', 'Trusted developer', 'Strong community']
            },
            {
                'name': 'EXAMPLE2', 
                'score': 8.2,
                'risk': 'medium',
                'potential': 150,
                'recommendation': 'buy',
                'factors': ['High migration probability', 'Good liquidity']
            }
        ]
        
        for i, opp in enumerate(example_opportunities, 1):
            print(f"{i}. {opp['name']}")
            print(f"   Score: {opp['score']}/10")
            print(f"   Risk: {opp['risk']}")
            print(f"   Potential: {opp['potential']}%")
            print(f"   Recommendation: {opp['recommendation'].upper()}")
            print(f"   Key Factors: {', '.join(opp['factors'])}")
            print()
        
        print("⚠️  Remember: This is educational only. Always DYOR!")
        
    except Exception as e:
        logger.error(f"Error in scanner example: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_opportunity_scanner_example())

