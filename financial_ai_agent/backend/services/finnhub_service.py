"""Finnhub API service for fetching financial data."""

import finnhub
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


class FinnhubService:
    """Service for interacting with Finnhub API."""
    
    def __init__(self):
        self.client = finnhub.Client(api_key=settings.FINNHUB_API_KEY)
    
    def get_stock_quote(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock quote.
        
        Returns: {
            'c': current price,
            'h': high price of the day,
            'l': low price of the day,
            'o': open price of the day,
            'pc': previous close price,
            't': timestamp
        }
        """
        try:
            quote = self.client.quote(symbol)
            quote['symbol'] = symbol
            quote['timestamp'] = datetime.now().isoformat()
            return quote
        except Exception as e:
            raise Exception(f"Error fetching quote for {symbol}: {str(e)}")
    
    def get_company_profile(self, symbol: str) -> Dict[str, Any]:
        """
        Get company profile information.
        
        Returns company details including name, industry, market cap, etc.
        """
        try:
            profile = self.client.company_profile2(symbol=symbol)
            return profile
        except Exception as e:
            raise Exception(f"Error fetching profile for {symbol}: {str(e)}")
    
    def get_company_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get company news for the past N days.
        
        Returns list of news articles with headline, summary, url, etc.
        """
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)
            
            news = self.client.company_news(
                symbol=symbol,
                _from=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d')
            )
            return news
        except Exception as e:
            raise Exception(f"Error fetching news for {symbol}: {str(e)}")
    
    def get_market_news(self, category: str = 'general') -> List[Dict[str, Any]]:
        """
        Get general market news.
        
        Categories: general, forex, crypto, merger
        """
        try:
            news = self.client.general_news(category=category, min_id=0)
            return news[:20]  # Limit to 20 articles
        except Exception as e:
            raise Exception(f"Error fetching market news: {str(e)}")
    
    def get_earnings_calendar(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Get earnings calendar.
        
        If symbol is provided, filters for that symbol.
        """
        try:
            to_date = datetime.now() + timedelta(days=30)
            from_date = datetime.now() - timedelta(days=7)
            
            if symbol:
                earnings = self.client.earnings_calendar(
                    _from=from_date.strftime('%Y-%m-%d'),
                    to=to_date.strftime('%Y-%m-%d'),
                    symbol=symbol
                )
            else:
                earnings = self.client.earnings_calendar(
                    _from=from_date.strftime('%Y-%m-%d'),
                    to=to_date.strftime('%Y-%m-%d')
                )
            return earnings
        except Exception as e:
            raise Exception(f"Error fetching earnings calendar: {str(e)}")
    
    def get_company_financials(self, symbol: str, statement: str = 'ic') -> Dict[str, Any]:
        """
        Get company financial statements.
        
        statement: 'bs' (balance sheet), 'ic' (income statement), 'cf' (cash flow)
        """
        try:
            financials = self.client.financials_reported(
                symbol=symbol,
                freq='annual'
            )
            return financials
        except Exception as e:
            raise Exception(f"Error fetching financials for {symbol}: {str(e)}")
    
    def get_insider_transactions(self, symbol: str) -> List[Dict[str, Any]]:
        """Get insider transactions for a company."""
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=90)
            
            transactions = self.client.stock_insider_transactions(
                symbol=symbol,
                _from=from_date.strftime('%Y-%m-%d'),
                to=to_date.strftime('%Y-%m-%d')
            )
            return transactions.get('data', [])
        except Exception as e:
            raise Exception(f"Error fetching insider transactions for {symbol}: {str(e)}")
    
    def get_recommendation_trends(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get analyst recommendation trends.
        
        Returns buy/hold/sell recommendations over time.
        """
        try:
            recommendations = self.client.recommendation_trends(symbol)
            return recommendations
        except Exception as e:
            raise Exception(f"Error fetching recommendations for {symbol}: {str(e)}")
    
    def get_price_target(self, symbol: str) -> Dict[str, Any]:
        """Get analyst price targets."""
        try:
            target = self.client.price_target(symbol)
            return target
        except Exception as e:
            raise Exception(f"Error fetching price target for {symbol}: {str(e)}")
    
    def search_symbol(self, query: str) -> List[Dict[str, Any]]:
        """Search for stock symbols."""
        try:
            results = self.client.symbol_lookup(query)
            return results.get('result', [])
        except Exception as e:
            raise Exception(f"Error searching for symbol: {str(e)}")
    
    def get_basic_financials(self, symbol: str) -> Dict[str, Any]:
        """Get basic financial metrics."""
        try:
            financials = self.client.company_basic_financials(symbol, 'all')
            return financials
        except Exception as e:
            raise Exception(f"Error fetching basic financials for {symbol}: {str(e)}")


# Singleton instance
finnhub_service = FinnhubService()
