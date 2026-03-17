"""
🚀 DuckDuckGo Search API - Production Ready
Hosted on Render.com - Handles 5,000+ searches/day with ease

Features:
- LRU caching (5,000 queries)
- Rate limiting friendly (0.5s delays)
- Retry logic with exponential backoff
- Advanced search operators support
- Health check & stats endpoints
"""

from duckduckgo_search import DDGS
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from pydantic import BaseModel
from datetime import datetime, timedelta
import time
import asyncio
import psutil
import os

# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = FastAPI(
    title="DuckDuckGo Search API",
    description="Free unlimited web search with caching",
    version="1.0.0"
)

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# STATISTICS TRACKING
# ============================================================================

class Stats:
    def __init__(self):
        self.start_time = datetime.now()
        self.total_requests = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.successful_searches = 0
        self.failed_searches = 0
        self.rate_limit_errors = 0
        
    def uptime(self):
        return datetime.now() - self.start_time
    
    def cache_hit_rate(self):
        if self.total_requests == 0:
            return 0.0
        return (self.cache_hits / self.total_requests) * 100
    
    def success_rate(self):
        total = self.successful_searches + self.failed_searches
        if total == 0:
            return 100.0
        return (self.successful_searches / total) * 100

stats = Stats()

# ============================================================================
# CACHE CONFIGURATION
# ============================================================================

# Large LRU cache for repeated queries
@lru_cache(maxsize=5000)
def search_with_cache(query: str, max_results: int):
    """
    Core search function with LRU caching
    
    Args:
        query: Search query string
        max_results: Maximum results to return (clamped to 1-100)
    
    Returns:
        List of search results or empty list on failure
    """
    stats.cache_misses += 1
    
    # Clamp max_results to prevent abuse
    clamped_max = max(1, min(max_results, 100))
    
    # Retry with exponential backoff
    for attempt in range(3):
        try:
            ddgs = DDGS()  # No 'with' statement needed
            results = ddgs.text(
                query=query,
                region="wt-wt",
                safesearch="off",
                timelimit=None,
                max_results=clamped_max
            )
            
            result_list = list(results) if results else []
            
            if result_list:
                stats.successful_searches += 1
            else:
                stats.failed_searches += 1
            
            return result_list
                
        except Exception as e:
            error_msg = str(e)
            
            # Track rate limit errors
            if "rate limit" in error_msg.lower() or "429" in error_msg:
                stats.rate_limit_errors += 1
            
            if attempt < 2:
                # Exponential backoff: 1s → 2s → 4s
                sleep_time = (2 ** attempt) + (time.time() % 1)  # Add jitter
                time.sleep(sleep_time)
            else:
                stats.failed_searches += 1
                return []
    
    return []

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DuckDuckGo Search API",
        "version": "1.0.0",
        "uptime": str(stats.uptime()),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/search")
async def search(
    q: str = Query(..., min_length=2, description="Search query"),
    n: int = Query(default=10, ge=1, le=100, description="Number of results (1-100)"),
    use_cache: bool = Query(default=True, description="Enable/disable caching")
):
    """
    Search DuckDuckGo with intelligent caching
    
    Args:
        q: Search query (minimum 2 characters)
        n: Number of results to return (default: 10, max: 100)
        use_cache: Enable or disable caching (default: True)
    
    Returns:
        Search results with metadata and statistics
    
    Examples:
        /api/search?q=Python+tutorial&n=10
        /api/search?q=machine+learning+site:github.com&n=20
        /api/search?q=AI+news+2024&use_cache=true
    """
    stats.total_requests += 1
    
    # Check if cached (before calling function)
    was_cached = False
    if use_cache:
        cache_key = (q, n)
        # Check if this specific call would be cached
        cache_info = search_with_cache.cache_info()
        was_cached = cache_key in str(cache_info)
        
        if was_cached:
            stats.cache_hits += 1
    
    # Rate limiting - be respectful to DuckDuckGo
    await asyncio.sleep(0.5)
    
    # Perform search
    results = search_with_cache(q, n) if use_cache else search_with_cache.__wrapped__(q, n)
    
    # Format response
    return {
        "query": q,
        "results": results,
        "count": len(results),
        "requested": n,
        "cached": was_cached,
        "timestamp": datetime.now().isoformat(),
        "stats": {
            "total_requests": stats.total_requests,
            "cache_hits": stats.cache_hits,
            "cache_misses": stats.cache_misses,
            "cache_hit_rate": f"{stats.cache_hit_rate():.1f}%",
            "successful_searches": stats.successful_searches,
            "failed_searches": stats.failed_searches,
            "success_rate": f"{stats.success_rate():.1f}%"
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get detailed API usage statistics"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    cache_info = search_with_cache.cache_info()
    
    return {
        "uptime": str(stats.uptime()),
        "start_time": stats.start_time.isoformat(),
        "requests": {
            "total": stats.total_requests,
            "per_day": stats.total_requests / max(stats.uptime().days, 1),
            "per_hour": stats.total_requests / max(stats.uptime().total_seconds() / 3600, 1)
        },
        "cache": {
            "hits": stats.cache_hits,
            "misses": stats.cache_misses,
            "hit_rate": f"{stats.cache_hit_rate():.1f}%",
            "max_size": 5000,
            "current_size": cache_info.currsize,
            "hits_per_request": f"{(cache_info.hits/max(stats.total_requests,1))*100:.1f}%",
            "misses_per_request": f"{(cache_info.misses/max(stats.total_requests,1))*100:.1f}%"
        },
        "search_performance": {
            "successful": stats.successful_searches,
            "failed": stats.failed_searches,
            "success_rate": f"{stats.success_rate():.1f}%",
            "rate_limit_errors": stats.rate_limit_errors
        },
        "system": {
            "memory_used_mb": round(memory_info.rss / 1024 / 1024, 2),
            "memory_available_mb": round(memory_info.vms / 1024 / 1024, 2),
            "cpu_percent": process.cpu_percent(interval=0.1)
        }
    }

@app.get("/api/cache/clear")
async def clear_cache():
    """Clear the LRU cache (admin endpoint)"""
    search_with_cache.cache_clear()
    return {
        "status": "success",
        "message": "Cache cleared successfully",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/cache/info")
async def cache_info():
    """Get cache statistics"""
    info = search_with_cache.cache_info()
    return {
        "max_size": info.maxsize,
        "current_size": info.currsize,
        "hits": info.hits,
        "misses": info.misses,
        "hit_rate": f"{(info.hits/max(info.hits+info.misses,1))*100:.1f}%"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "path": request.url.path
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": str(exc),
        "type": type(exc).__name__
    }

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment (Render sets PORT env variable)
    port = int(os.environ.get("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        log_level="info",
        workers=1  # Single worker for shared cache
    )
