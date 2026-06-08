"""
Abstract storage layer for session management with Redis and in-memory implementations.

This module provides a clean abstraction for session state persistence, enabling
seamless scaling from local development (in-memory with thread-safety) to production
(distributed Redis with explicit TTL management).
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class UserSession(BaseModel):
    """Represents a user session with conversation state and metadata."""
    
    phone_number: str = Field(..., description="Unique identifier for the session")
    state: str = Field(default="IDLE_INQUIRY", description="Current state in state machine")
    history: list[dict[str, Any]] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict, description="Custom metadata")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
        }


class BaseSessionStorage(ABC):
    """Abstract base class for session storage implementations."""

    @abstractmethod
    async def get(self, key: str) -> Optional[UserSession]:
        """
        Retrieve a session by key.
        
        Args:
            key: Session identifier (typically phone number)
            
        Returns:
            UserSession if found, None otherwise
        """
        pass

    @abstractmethod
    async def set(self, key: str, session: UserSession) -> None:
        """
        Store or update a session.
        
        Args:
            key: Session identifier
            session: UserSession object to persist
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """
        Delete a session.
        
        Args:
            key: Session identifier to delete
        """
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a session exists."""
        pass

    @abstractmethod
    async def cleanup_expired(self, ttl_seconds: int = 1800) -> int:
        """
        Remove expired sessions.
        
        Args:
            ttl_seconds: Time-to-live threshold in seconds (default: 30 minutes)
            
        Returns:
            Number of sessions deleted
        """
        pass


class InMemorySessionStorage(BaseSessionStorage):
    """
    Thread-safe in-memory session storage using Python threading.Lock.
    
    Suitable for development and testing. Implements explicit TTL cleanup
    to prevent memory leaks from abandoned sessions.
    """

    def __init__(self):
        self._store: dict[str, UserSession] = {}
        self._lock = threading.Lock()
        logger.info("InMemorySessionStorage initialized (thread-safe mode)")

    async def get(self, key: str) -> Optional[UserSession]:
        """Retrieve session with thread-safe locking."""
        with self._lock:
            if key in self._store:
                return self._store[key]
            return None

    async def set(self, key: str, session: UserSession) -> None:
        """Store session with thread-safe locking."""
        session.updated_at = datetime.now(timezone.utc)
        with self._lock:
            self._store[key] = session
            logger.debug(f"Session stored: {key} (state={session.state})")

    async def delete(self, key: str) -> None:
        """Delete session with thread-safe locking."""
        with self._lock:
            if key in self._store:
                del self._store[key]
                logger.debug(f"Session deleted: {key}")

    async def exists(self, key: str) -> bool:
        """Check session existence with thread-safe locking."""
        with self._lock:
            return key in self._store

    async def cleanup_expired(self, ttl_seconds: int = 1800) -> int:
        """
        Remove sessions older than TTL threshold.
        
        Args:
            ttl_seconds: Time-to-live threshold (default: 30 minutes = 1800 seconds)
            
        Returns:
            Number of sessions deleted
        """
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(seconds=ttl_seconds)
        deleted_count = 0

        with self._lock:
            expired_keys = [
                key
                for key, session in self._store.items()
                if session.updated_at < threshold
            ]
            for key in expired_keys:
                del self._store[key]
                deleted_count += 1

        if deleted_count > 0:
            logger.info(f"Cleanup: Deleted {deleted_count} expired sessions")
        
        return deleted_count

    def get_store_size(self) -> int:
        """Get current number of sessions (for monitoring)."""
        with self._lock:
            return len(self._store)


class RedisSessionStorage(BaseSessionStorage):
    """
    Distributed Redis-backed session storage with explicit TTL.
    
    Production-grade implementation suitable for multi-worker deployments.
    Requires Redis to be available. Falls back gracefully if Redis is unavailable.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", ttl_seconds: int = 1800):
        """
        Initialize Redis session storage.
        
        Args:
            redis_url: Redis connection URL
            ttl_seconds: Default TTL for sessions (30 minutes)
        """
        self.redis_url = redis_url
        self.ttl_seconds = ttl_seconds
        self.redis_client = None
        self._initialized = False
        logger.info(f"RedisSessionStorage configured (ttl={ttl_seconds}s, url={redis_url})")

    async def _ensure_connection(self) -> bool:
        """
        Lazy-initialize Redis connection. Returns True if connection successful.
        
        This prevents startup failures if Redis is temporarily unavailable.
        """
        if self._initialized:
            return True

        try:
            import aioredis
            
            self.redis_client = await aioredis.create_redis_pool(
                self.redis_url,
                encoding="utf-8",
                minsize=1,
                maxsize=10,
            )
            self._initialized = True
            logger.info("Redis connection established")
            return True
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Falling back to in-memory storage.")
            self._initialized = False
            return False

    async def get(self, key: str) -> Optional[UserSession]:
        """Retrieve session from Redis with TTL enforcement."""
        if not await self._ensure_connection():
            return None

        try:
            data = await self.redis_client.get(f"session:{key}")
            if data:
                session_dict = json.loads(data)
                # Reconstruct datetime objects
                session_dict["created_at"] = datetime.fromisoformat(session_dict["created_at"])
                session_dict["updated_at"] = datetime.fromisoformat(session_dict["updated_at"])
                return UserSession(**session_dict)
            return None
        except Exception as e:
            logger.error(f"Redis GET error: {e}")
            return None

    async def set(self, key: str, session: UserSession) -> None:
        """Store session in Redis with explicit TTL."""
        if not await self._ensure_connection():
            return

        try:
            session.updated_at = datetime.now(timezone.utc)
            session_json = session.json()
            await self.redis_client.setex(
                f"session:{key}",
                self.ttl_seconds,
                session_json
            )
            logger.debug(f"Session stored in Redis: {key} (ttl={self.ttl_seconds}s)")
        except Exception as e:
            logger.error(f"Redis SET error: {e}")

    async def delete(self, key: str) -> None:
        """Delete session from Redis."""
        if not await self._ensure_connection():
            return

        try:
            await self.redis_client.delete(f"session:{key}")
            logger.debug(f"Session deleted from Redis: {key}")
        except Exception as e:
            logger.error(f"Redis DELETE error: {e}")

    async def exists(self, key: str) -> bool:
        """Check if session exists in Redis."""
        if not await self._ensure_connection():
            return False

        try:
            exists = await self.redis_client.exists(f"session:{key}")
            return bool(exists)
        except Exception as e:
            logger.error(f"Redis EXISTS error: {e}")
            return False

    async def cleanup_expired(self, ttl_seconds: int = 1800) -> int:
        """
        Redis automatically handles TTL cleanup via EXPIREAT.
        This method is a no-op for Redis backend.
        """
        logger.debug("Redis cleanup skipped (automatic TTL management)")
        return 0

    async def close(self):
        """Close Redis connection pool."""
        if self.redis_client:
            self.redis_client.close()
            await self.redis_client.wait_closed()
            logger.info("Redis connection closed")


class HybridSessionStorage(BaseSessionStorage):
    """
    Hybrid storage that falls back from Redis to in-memory gracefully.
    
    Attempts Redis operations first, falls back to in-memory storage
    if Redis is unavailable, ensuring system resilience.
    """

    def __init__(self, redis_url: str = "redis://localhost:6379", ttl_seconds: int = 1800):
        self.redis_storage = RedisSessionStorage(redis_url, ttl_seconds)
        self.memory_storage = InMemorySessionStorage()
        self.ttl_seconds = ttl_seconds
        self._use_redis = False
        logger.info("HybridSessionStorage initialized (Redis primary, in-memory fallback)")

    async def get(self, key: str) -> Optional[UserSession]:
        """Get from Redis, fall back to in-memory if needed."""
        session = await self.redis_storage.get(key)
        if session is None:
            session = await self.memory_storage.get(key)
        return session

    async def set(self, key: str, session: UserSession) -> None:
        """Store in both Redis and in-memory for redundancy."""
        await self.redis_storage.set(key, session)
        await self.memory_storage.set(key, session)

    async def delete(self, key: str) -> None:
        """Delete from both storages."""
        await self.redis_storage.delete(key)
        await self.memory_storage.delete(key)

    async def exists(self, key: str) -> bool:
        """Check in Redis first, fall back to in-memory."""
        exists = await self.redis_storage.exists(key)
        if not exists:
            exists = await self.memory_storage.exists(key)
        return exists

    async def cleanup_expired(self, ttl_seconds: int = 1800) -> int:
        """Cleanup in-memory storage (Redis handles its own)."""
        return await self.memory_storage.cleanup_expired(ttl_seconds)
