from typing import List, Dict, Optional, Any
from enum import Enum, auto
import random

class TrendCategory(Enum):
    BULLISH = auto()
    BEARISH = auto()
    NEUTRAL = auto()

class TrendSourcing:
    """
    Manages cryptocurrency trend sourcing and analysis.
    Provides methods for retrieving and scoring market trends.
    """
    
    @staticmethod
    def fetch_trends(limit: int = 10) -> List[Dict[str, Any]]:
        """
        Simulate fetching cryptocurrency trends from multiple sources.
        
        Args:
            limit (int, optional): Maximum number of trends to return. Defaults to 10.
        
        Returns:
            List of trend dictionaries with market insights.
        """
        mock_trends = [
            {
                "name": f"Crypto_{i}",
                "price_change": round(random.uniform(-10, 10), 2),
                "volume": random.randint(1000, 1000000),
                "category": random.choice(list(TrendCategory))
            } for i in range(limit)
        ]
        return mock_trends
    
    @staticmethod
    def score_trend_relevance(trend: Dict[str, Any], 
                               min_volume: int = 5000, 
                               volatility_threshold: float = 5.0) -> float:
        """
        Calculate a relevance score for a given trend.
        
        Args:
            trend (Dict): Trend information dictionary
            min_volume (int): Minimum trading volume for consideration
            volatility_threshold (float): Price change threshold for significance
        
        Returns:
            float: Trend relevance score between 0 and 1
        """
        if not trend:
            return 0.0
        
        volume_score = min(trend['volume'] / min_volume, 1.0)
        volatility_score = min(abs(trend['price_change']) / volatility_threshold, 1.0)
        
        # Bonus for extreme market movements
        category_bonus = {
            TrendCategory.BULLISH: 1.2,
            TrendCategory.BEARISH: 1.2,
            TrendCategory.NEUTRAL: 1.0
        }.get(trend['category'], 1.0)
        
        # Cap the score at 1.0
        return min(round(volume_score * volatility_score * category_bonus, 2), 1.0)
    
    @classmethod
    def get_top_trends(cls, top_n: int = 5, min_relevance: float = 0.5) -> List[Dict[str, Any]]:
        """
        Retrieve top trends based on relevance scoring.
        
        Args:
            top_n (int): Number of top trends to return
            min_relevance (float): Minimum relevance score for inclusion
        
        Returns:
            List of top trending cryptocurrencies
        """
        all_trends = cls.fetch_trends()
        scored_trends = [
            (trend, cls.score_trend_relevance(trend)) 
            for trend in all_trends
        ]
        
        # Sort by relevance score in descending order
        sorted_trends = sorted(scored_trends, key=lambda x: x[1], reverse=True)
        
        # Filter and return top trends meeting minimum relevance
        return [
            trend for trend, score in sorted_trends 
            if score >= min_relevance
        ][:top_n]