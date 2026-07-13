"""Database models for the Financial AI Agent."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model for authentication and personalization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    watchlists = relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")


class Watchlist(Base):
    """Watchlist model for storing user's tracked stocks."""
    
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, index=True, nullable=False)
    name = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="watchlists")


class Alert(Base):
    """Price alert model for stock notifications."""
    
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, index=True, nullable=False)
    condition = Column(String, nullable=False)  # 'above', 'below'
    target_price = Column(Float, nullable=False)
    triggered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")


class MarketInsight(Base):
    """Stored AI-generated market insights."""
    
    __tablename__ = "market_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    insight_type = Column(String, index=True)  # 'summary', 'analysis', 'recommendation'
    content = Column(String, nullable=False)
    insight_metadata = Column(JSON, nullable=True)  # Store additional context
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    model_version = Column(String, nullable=True)


class StockCache(Base):
    """Cache for stock data to reduce API calls."""
    
    __tablename__ = "stock_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    data_type = Column(String, index=True, nullable=False)  # 'price', 'profile', 'news'
    data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
