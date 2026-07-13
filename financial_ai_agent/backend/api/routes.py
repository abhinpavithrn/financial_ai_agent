"""API routes for the Financial AI Agent."""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.database import get_db
from database.models import Watchlist, Alert, MarketInsight, StockCache, User
from services.finnhub_service import finnhub_service
from agents.market_analyst_agent import market_analyst
from api.schemas import (
    WatchlistCreate, WatchlistResponse,
    AlertCreate, AlertResponse,
    StockQuoteResponse, StockAnalysisResponse
)

router = APIRouter()


# ==================== Stock Data Routes ====================

@router.get("/stock/{symbol}/quote", response_model=StockQuoteResponse)
async def get_stock_quote(symbol: str, db: Session = Depends(get_db)):
    """Get real-time stock quote."""
    try:
        # Check cache first
        cache = db.query(StockCache).filter(
            StockCache.symbol == symbol.upper(),
            StockCache.data_type == 'quote',
            StockCache.expires_at > datetime.utcnow()
        ).first()
        
        if cache:
            return StockQuoteResponse(**cache.data)
        
        # Fetch from API
        quote = finnhub_service.get_stock_quote(symbol.upper())
        
        # Cache the result
        new_cache = StockCache(
            symbol=symbol.upper(),
            data_type='quote',
            data=quote,
            expires_at=datetime.utcnow() + timedelta(seconds=60)
        )
        db.add(new_cache)
        db.commit()
        
        return StockQuoteResponse(**quote)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/profile")
async def get_stock_profile(symbol: str, db: Session = Depends(get_db)):
    """Get company profile."""
    try:
        # Check cache
        cache = db.query(StockCache).filter(
            StockCache.symbol == symbol.upper(),
            StockCache.data_type == 'profile',
            StockCache.expires_at > datetime.utcnow()
        ).first()
        
        if cache:
            return cache.data
        
        # Fetch from API
        profile = finnhub_service.get_company_profile(symbol.upper())
        
        # Cache for 24 hours
        new_cache = StockCache(
            symbol=symbol.upper(),
            data_type='profile',
            data=profile,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db.add(new_cache)
        db.commit()
        
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/news")
async def get_stock_news(symbol: str, days: int = 7):
    """Get company news."""
    try:
        news = finnhub_service.get_company_news(symbol.upper(), days=days)
        return {"symbol": symbol.upper(), "news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/earnings")
async def get_earnings(symbol: str):
    """Get earnings calendar."""
    try:
        earnings = finnhub_service.get_earnings_calendar(symbol.upper())
        return earnings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/financials")
async def get_financials(symbol: str):
    """Get company financials."""
    try:
        financials = finnhub_service.get_basic_financials(symbol.upper())
        return financials
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/insider-transactions")
async def get_insider_transactions(symbol: str):
    """Get insider transactions."""
    try:
        transactions = finnhub_service.get_insider_transactions(symbol.upper())
        return {"symbol": symbol.upper(), "transactions": transactions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/recommendations")
async def get_recommendations(symbol: str):
    """Get analyst recommendations."""
    try:
        recommendations = finnhub_service.get_recommendation_trends(symbol.upper())
        price_target = finnhub_service.get_price_target(symbol.upper())
        
        return {
            "symbol": symbol.upper(),
            "recommendations": recommendations,
            "priceTarget": price_target
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== AI Analysis Routes ====================

@router.get("/stock/{symbol}/analysis")
async def get_stock_analysis(symbol: str, db: Session = Depends(get_db)):
    """Generate AI-powered stock analysis."""
    try:
        # Fetch all required data
        quote = finnhub_service.get_stock_quote(symbol.upper())
        profile = finnhub_service.get_company_profile(symbol.upper())
        news = finnhub_service.get_company_news(symbol.upper(), days=7)
        
        # Generate AI summary
        summary = market_analyst.generate_stock_summary(
            symbol=symbol.upper(),
            quote=quote,
            profile=profile,
            news=news
        )
        
        # Store insight
        insight = MarketInsight(
            symbol=symbol.upper(),
            insight_type='summary',
            content=summary,
            metadata={'quote': quote, 'profile': profile}
        )
        db.add(insight)
        db.commit()
        
        return {
            "symbol": symbol.upper(),
            "summary": summary,
            "quote": quote,
            "profile": profile,
            "news": news[:5]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stock/{symbol}/recommendation")
async def get_ai_recommendation(symbol: str, db: Session = Depends(get_db)):
    """Get AI-generated investment recommendation."""
    try:
        quote = finnhub_service.get_stock_quote(symbol.upper())
        recommendations = finnhub_service.get_recommendation_trends(symbol.upper())
        price_target = finnhub_service.get_price_target(symbol.upper())
        news = finnhub_service.get_company_news(symbol.upper(), days=3)
        
        # Simple sentiment analysis (can be enhanced)
        sentiment = "neutral"
        if news:
            # Basic sentiment based on news count
            sentiment = "positive" if len(news) > 5 else "neutral"
        
        recommendation = market_analyst.generate_recommendation(
            symbol=symbol.upper(),
            quote=quote,
            analyst_recommendations=recommendations,
            price_target=price_target,
            news_sentiment=sentiment
        )
        
        # Store insight
        insight = MarketInsight(
            symbol=symbol.upper(),
            insight_type='recommendation',
            content=recommendation
        )
        db.add(insight)
        db.commit()
        
        return {
            "symbol": symbol.upper(),
            "recommendation": recommendation,
            "analystData": recommendations,
            "priceTarget": price_target
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/market/overview")
async def get_market_overview(db: Session = Depends(get_db)):
    """Get AI-generated market overview."""
    try:
        market_news = finnhub_service.get_market_news('general')
        
        overview = market_analyst.generate_market_overview(market_news)
        
        # Store insight
        insight = MarketInsight(
            symbol='MARKET',
            insight_type='overview',
            content=overview
        )
        db.add(insight)
        db.commit()
        
        return {
            "overview": overview,
            "news": market_news[:10]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Watchlist Routes ====================

@router.post("/watchlist")
async def add_to_watchlist(
    item: WatchlistCreate,
    user_id: int = 1,  # TODO: Get from authentication
    db: Session = Depends(get_db)
):
    """Add stock to watchlist."""
    try:
        # Check if already exists
        existing = db.query(Watchlist).filter(
            Watchlist.user_id == user_id,
            Watchlist.symbol == item.symbol.upper()
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Stock already in watchlist")
        
        # Get company name
        try:
            profile = finnhub_service.get_company_profile(item.symbol.upper())
            company_name = profile.get('name', item.symbol.upper())
        except:
            company_name = item.symbol.upper()
        
        watchlist_item = Watchlist(
            user_id=user_id,
            symbol=item.symbol.upper(),
            name=company_name,
            notes=item.notes
        )
        db.add(watchlist_item)
        db.commit()
        db.refresh(watchlist_item)
        
        return watchlist_item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/watchlist")
async def get_watchlist(
    user_id: int = 1,  # TODO: Get from authentication
    db: Session = Depends(get_db)
):
    """Get user's watchlist."""
    watchlist = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    return watchlist


@router.delete("/watchlist/{watchlist_id}")
async def remove_from_watchlist(
    watchlist_id: int,
    user_id: int = 1,  # TODO: Get from authentication
    db: Session = Depends(get_db)
):
    """Remove stock from watchlist."""
    item = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == user_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    
    db.delete(item)
    db.commit()
    
    return {"message": "Removed from watchlist"}


# ==================== Search Route ====================

@router.get("/search")
async def search_stocks(q: str):
    """Search for stocks by symbol or name."""
    try:
        results = finnhub_service.search_symbol(q)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== WebSocket for Real-Time Updates ====================

class ConnectionManager:
    """Manage WebSocket connections."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/ws/stock/{symbol}")
async def websocket_stock_updates(websocket: WebSocket, symbol: str):
    """WebSocket endpoint for real-time stock updates."""
    await manager.connect(websocket)
    
    try:
        while True:
            # Fetch latest quote
            quote = finnhub_service.get_stock_quote(symbol.upper())
            
            # Send to client
            await websocket.send_json({
                "type": "quote_update",
                "symbol": symbol.upper(),
                "data": quote
            })
            
            # Wait before next update
            await asyncio.sleep(5)  # Update every 5 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
