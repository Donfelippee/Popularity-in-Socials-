import pytest
from src.trend_sourcing import TrendSourcing, TrendCategory

def test_fetch_trends():
    """Test trend fetching mechanism"""
    trends = TrendSourcing.fetch_trends()
    assert len(trends) > 0
    assert all(isinstance(trend, dict) for trend in trends)
    assert all('name' in trend and 'price_change' in trend for trend in trends)

def test_score_trend_relevance():
    """Test trend relevance scoring"""
    test_trend = {
        'name': 'TestCrypto',
        'price_change': 7.5,
        'volume': 10000,
        'category': TrendCategory.BULLISH
    }
    
    score = TrendSourcing.score_trend_relevance(test_trend)
    assert 0 <= score <= 1.0
    
    # Test with extreme values
    high_volatility_trend = {
        'name': 'VolatileCrypto',
        'price_change': 15.0,
        'volume': 500000,
        'category': TrendCategory.BEARISH
    }
    
    high_score = TrendSourcing.score_trend_relevance(high_volatility_trend)
    assert high_score > 1.0

def test_get_top_trends():
    """Test retrieving top trends"""
    top_trends = TrendSourcing.get_top_trends()
    
    assert isinstance(top_trends, list)
    assert all('name' in trend for trend in top_trends)
    assert len(top_trends) <= 5  # Default top_n

def test_edge_cases():
    """Test trend sourcing with edge case inputs"""
    # Test with None/empty input
    assert TrendSourcing.score_trend_relevance(None) == 0.0
    assert TrendSourcing.score_trend_relevance({}) == 0.0

    # Test minimal volume trends
    minimal_trend = {
        'name': 'MinimalTrend',
        'price_change': 1.0,
        'volume': 100,
        'category': TrendCategory.NEUTRAL
    }
    
    minimal_score = TrendSourcing.score_trend_relevance(minimal_trend)
    assert 0 <= minimal_score < 0.5