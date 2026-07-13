"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ==================== Watchlist Schemas ====================

class WatchlistCreate(BaseModel):
    symbol: str = Field(..., description="Stock symbol")
    notes: Optional[str] = None


class WatchlistResponse(BaseModel):
    id: int
    symbol: str
    name: Optional[str]
    added_at: datetime
    notes: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== Alert Schemas ====================

class AlertCreate(BaseModel):
    symbol: str
    condition: str = Field(..., description="'above' or 'below'")
    target_price: float


class AlertResponse(BaseModel):
    id: int
    symbol: str
    condition: str
    target_price: float
    triggered: bool
    created_at: datetime
    triggered_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ==================== Stock Data Schemas ====================

class StockQuoteResponse(BaseModel):
    symbol: str
    c: float = Field(..., description="Current price")
    h: float = Field(..., description="High price of the day")
    l: float = Field(..., description="Low price of the day")
    o: float = Field(..., description="Open price of the day")
    pc: float = Field(..., description="Previous close price")
    t: Optional[int] = Field(None, description="Timestamp")
    timestamp: Optional[str] = None


class CompanyProfile(BaseModel):
    name: str
    ticker: str
    exchange: Optional[str]
    industry: Optional[str]
    logo: Optional[str]
    marketCapitalization: Optional[float]
    shareOutstanding: Optional[float]
    
    class Config:
        extra = "allow"


class NewsArticle(BaseModel):
    headline: str
    summary: Optional[str]
    url: str
    datetime: int
    source: Optional[str]
    image: Optional[str]


class StockAnalysisResponse(BaseModel):
    symbol: str
    summary: str
    quote: Dict[str, Any]
    profile: Dict[str, Any]
    news: List[Dict[str, Any]]


class RecommendationResponse(BaseModel):
    symbol: str
    recommendation: str
    analystData: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]


# ==================== User Schemas ====================

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
