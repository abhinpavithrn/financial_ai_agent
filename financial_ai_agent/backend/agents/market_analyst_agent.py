"""AI Agent for generating market insights and analysis."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, List, Any, Optional
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


class MarketAnalystAgent:
    """AI Agent that analyzes market data and generates insights."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    def generate_stock_summary(
        self,
        symbol: str,
        quote: Dict[str, Any],
        profile: Dict[str, Any],
        news: List[Dict[str, Any]]
    ) -> str:
        """Generate a natural language summary of a stock."""
        
        prompt = ChatPromptTemplate.from_template("""
You are a professional financial analyst. Generate a concise, insightful summary of the following stock.

Stock Symbol: {symbol}
Company Name: {company_name}
Industry: {industry}

Current Price: ${current_price}
Previous Close: ${previous_close}
Day High: ${day_high}
Day Low: ${day_low}
Price Change: {price_change}%

Market Cap: ${market_cap}

Recent News Headlines:
{news_headlines}

Provide a 2-3 paragraph summary that includes:
1. Current stock performance and key price metrics
2. Company overview and industry position
3. Notable recent news and market sentiment
4. Brief outlook based on available data

Be professional, objective, and data-driven.
""")
        
        # Calculate price change percentage
        price_change = ((quote['c'] - quote['pc']) / quote['pc']) * 100 if quote['pc'] != 0 else 0
        
        # Format news headlines
        news_headlines = "\n".join([
            f"- {article.get('headline', 'N/A')} ({article.get('datetime', '')})"
            for article in news[:5]
        ])
        
        messages = prompt.format_messages(
            symbol=symbol,
            company_name=profile.get('name', 'N/A'),
            industry=profile.get('finnhubIndustry', 'N/A'),
            current_price=f"{quote['c']:.2f}",
            previous_close=f"{quote['pc']:.2f}",
            day_high=f"{quote['h']:.2f}",
            day_low=f"{quote['l']:.2f}",
            price_change=f"{price_change:+.2f}",
            market_cap=f"{profile.get('marketCapitalization', 0):.2f}M",
            news_headlines=news_headlines if news_headlines else "No recent news available"
        )
        
        result = self.llm.invoke(messages)
        return result.content
    
    def analyze_earnings(
        self,
        symbol: str,
        earnings_data: Dict[str, Any],
        financials: Dict[str, Any]
    ) -> str:
        """Analyze earnings data and provide insights."""
        
        prompt = ChatPromptTemplate.from_template("""
You are a financial analyst specializing in earnings analysis.

Company: {symbol}

Earnings Data:
{earnings_summary}

Financial Metrics:
{financial_metrics}

Provide a detailed analysis including:
1. Earnings performance and trends
2. Key financial metrics interpretation
3. Strengths and concerns
4. Forward-looking considerations

Be analytical and highlight important numbers.
""")
        
        messages = prompt.format_messages(
            symbol=symbol,
            earnings_summary=json.dumps(earnings_data, indent=2),
            financial_metrics=json.dumps(financials, indent=2)
        )
        
        result = self.llm.invoke(messages)
        return result.content
    
    def generate_market_overview(
        self,
        market_news: List[Dict[str, Any]],
        trending_stocks: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate overall market overview and sentiment."""
        
        prompt = ChatPromptTemplate.from_template("""
You are a market analyst providing a daily market overview.

Top Market News:
{news_summary}

{trending_section}

Provide a comprehensive market overview including:
1. Key market themes and trends
2. Sentiment analysis (bullish/bearish/neutral)
3. Notable events and their potential impact
4. Sectors to watch

Keep it concise but informative (3-4 paragraphs).
""")
        
        # Format news
        news_summary = "\n".join([
            f"- {article.get('headline', 'N/A')}\n  {article.get('summary', '')[:200]}..."
            for article in market_news[:10]
        ])
        
        # Format trending stocks if provided
        trending_section = ""
        if trending_stocks:
            trending_section = "\nTrending Stocks:\n" + "\n".join([
                f"- {stock.get('symbol', 'N/A')}: ${stock.get('price', 'N/A')}"
                for stock in trending_stocks[:5]
            ])
        
        messages = prompt.format_messages(
            news_summary=news_summary,
            trending_section=trending_section
        )
        
        result = self.llm.invoke(messages)
        return result.content
    
    def generate_recommendation(
        self,
        symbol: str,
        quote: Dict[str, Any],
        analyst_recommendations: List[Dict[str, Any]],
        price_target: Dict[str, Any],
        news_sentiment: str
    ) -> str:
        """Generate investment recommendation based on multiple data points."""
        
        prompt = ChatPromptTemplate.from_template("""
You are an investment advisor providing guidance based on comprehensive analysis.

Stock: {symbol}
Current Price: ${current_price}

Analyst Consensus:
{analyst_data}

Price Target:
Target High: ${target_high}
Target Low: ${target_low}
Target Mean: ${target_mean}

News Sentiment: {sentiment}

Provide a balanced investment recommendation including:
1. Summary of analyst opinions
2. Price target analysis relative to current price
3. Risk factors and considerations
4. Recommended action (Buy/Hold/Sell) with rationale

IMPORTANT: This is for educational purposes only and not financial advice.
""")
        
        messages = prompt.format_messages(
            symbol=symbol,
            current_price=f"{quote['c']:.2f}",
            analyst_data=json.dumps(analyst_recommendations, indent=2),
            target_high=f"{price_target.get('targetHigh', 0):.2f}",
            target_low=f"{price_target.get('targetLow', 0):.2f}",
            target_mean=f"{price_target.get('targetMean', 0):.2f}",
            sentiment=news_sentiment
        )
        
        result = self.llm.invoke(messages)
        return result.content
    
    def explain_metric(self, metric_name: str, metric_value: Any, context: str = "") -> str:
        """Explain a financial metric in simple terms."""
        
        prompt = ChatPromptTemplate.from_template("""
Explain the following financial metric in simple, easy-to-understand language:

Metric: {metric_name}
Value: {metric_value}
Context: {context}

Provide:
1. What this metric means
2. How to interpret the current value
3. Why it matters to investors
4. General benchmark or what's considered good/bad

Keep it concise (2-3 sentences).
""")
        
        messages = prompt.format_messages(
            metric_name=metric_name,
            metric_value=str(metric_value),
            context=context
        )
        
        result = self.llm.invoke(messages)
        return result.content


# Singleton instance
market_analyst = MarketAnalystAgent()
