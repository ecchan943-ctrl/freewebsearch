# 🚀 DuckDuckGo Search API - Render Deployment

## Quick Start

### 1. Deploy to Render (5 minutes)

#### Option A: Deploy via Render Dashboard

1. **Push code to GitHub**
   ```bash
   cd render_ddg_search
   git init
   git add .
   git commit -m "Initial commit - DDG Search API"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `ddg-search-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python main.py`
     - **Instance Type**: `Free` (perfect for 5K searches/day)
   
3. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your API will be at: `https://ddg-search-api.onrender.com`

---

#### Option B: Deploy via Render CLI

```bash
# Install Render CLI
npm install -g @render-cloud/cli

# Login
render login

# Deploy
cd render_ddg_search
render up
```

---

## API Endpoints

### 🔍 Search Endpoint

```http
GET /api/search?q={query}&n={results}&use_cache={true|false}
```

**Parameters:**
- `q` (required): Search query (min 2 characters)
- `n` (optional): Number of results (default: 10, max: 100)
- `use_cache` (optional): Enable caching (default: true)

**Example:**
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=Python+tutorial&n=10"
```

**Response:**
```json
{
  "query": "Python tutorial",
  "results": [
    {
      "title": "Python Tutorial - W3Schools",
      "href": "https://www.w3schools.com/python/",
      "body": "Learn Python programming..."
    }
  ],
  "count": 10,
  "requested": 10,
  "cached": false,
  "timestamp": "2024-03-17T10:30:00",
  "stats": {
    "total_requests": 1,
    "cache_hits": 0,
    "cache_hit_rate": "0.0%"
  }
}
```

---

### 📊 Statistics Endpoint

```http
GET /api/stats
```

**Example:**
```bash
curl "https://ddg-search-api.onrender.com/api/stats"
```

**Response:**
```json
{
  "uptime": "2 days, 5 hours",
  "requests": {
    "total": 5420,
    "per_day": 2400,
    "per_hour": 100
  },
  "cache": {
    "hits": 3200,
    "misses": 2220,
    "hit_rate": "59.0%",
    "max_size": 5000,
    "current_size": 1847
  },
  "search_performance": {
    "successful": 2180,
    "failed": 40,
    "success_rate": "98.2%"
  }
}
```

---

### ❤️ Health Check

```http
GET /
```

**Response:**
```json
{
  "status": "healthy",
  "service": "DuckDuckGo Search API",
  "version": "1.0.0",
  "uptime": "2 days, 5 hours"
}
```

---

## Advanced Search Examples

### Site Restriction
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=Python+site:github.com&n=10"
```

### File Type Filtering
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=ML+tutorial+filetype:pdf&n=10"
```

### Time-Based Search
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=AI+news+2024&n=10"
```

### Exact Phrase
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=%22machine+learning%22+tutorial&n=10"
```

### Exclusion
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=Python+programming+-snake&n=10"
```

### Complex Combination
```bash
curl "https://ddg-search-api.onrender.com/api/search?q=machine+learning+site:github.com+filetype:ipynb&n=10"
```

---

## Performance Expectations

### For 5,000 Searches/Day:

| Metric | Value |
|--------|-------|
| **Cache Hit Rate** | 60-70% |
| **Actual DDG Calls** | ~1,500-2,000/day |
| **Average Response Time** | 1-2 seconds |
| **Cached Response Time** | <100ms |
| **Rate Limit Risk** | Near zero |
| **Cost** | $0 (free tier) |

---

## Caching Behavior

### How LRU Cache Works:

```python
# First request (cold cache) - 1-2 seconds
GET /api/search?q=Python+tutorial
# → Calls DuckDuckGo, caches result

# Second request (cached) - <100ms
GET /api/search?q=Python+tutorial
# → Returns cached result instantly

# Cache automatically stores up to 5,000 unique queries
# Least recently used queries are evicted when full
```

### Cache Statistics:
```bash
# Check cache performance
curl "https://ddg-search-api.onrender.com/api/cache/info"

# Clear cache if needed
curl "https://ddg-search-api.onrender.com/api/cache/clear"
```

---

## Monitoring & Alerts

### Key Metrics to Watch:

1. **Cache Hit Rate**
   - Target: >60%
   - If low: Increase repeated queries

2. **Success Rate**
   - Target: >95%
   - If low: Check rate limit errors in stats

3. **Rate Limit Errors**
   - Target: 0
   - If >10: Reduce request frequency

4. **Memory Usage**
   - Target: <500MB
   - Free tier has 512MB limit

### Check Stats Regularly:
```bash
# Automated monitoring script
while true; do
  curl -s "https://ddg-search-api.onrender.com/api/stats" | jq '.search_performance'
  sleep 60
done
```

---

## Troubleshooting

### Issue: Slow Response Times

**Solution:**
- Check cache hit rate (should be >60%)
- Increase caching with `use_cache=true`
- Verify server isn't overloaded (check `/api/stats`)

---

### Issue: Rate Limit Errors

**Solution:**
- Already handled automatically with backoff
- If persistent, increase delay in `main.py`:
  ```python
  await asyncio.sleep(1.0)  # Increase from 0.5s to 1.0s
  ```

---

### Issue: Empty Results

**Possible Causes:**
1. Query too specific (no results exist)
2. HTML parsing issue (DDG changed structure)
3. Temporary network issue

**Solution:**
- Try simpler query
- Check if DDG is accessible
- Wait and retry (temporary issue)

---

## Cost Estimation

### Render Free Tier:
- ✅ **500 hours/month** free (~20 days continuous)
- ✅ **512MB RAM** per instance
- ✅ **Sufficient for 5K searches/day**

### If You Need More:

**Render Hobby ($7/month):**
- Unlimited hours
- Better performance
- Still handles 5K easily

**Total Monthly Cost: $0-7**

---

## Security Considerations

### Production Recommendations:

1. **Add API Key Authentication**
   ```python
   @app.get("/api/search")
   async def search(
       q: str,
       n: int = 10,
       x_api_key: str = Header(...)
   ):
       if x_api_key != os.environ.get("API_KEY"):
           raise HTTPException(status_code=401)
   ```

2. **Rate Limit Clients**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   
   @app.get("/api/search")
   @limiter.limit("10/minute")  # 10 requests per minute per IP
   async def search(request: Request, q: str):
       ...
   ```

3. **Enable HTTPS Only**
   - Render provides free SSL certificates
   - All endpoints are HTTPS by default

---

## Environment Variables (Optional)

Create `.env` file for local development:

```bash
# Optional configuration
PORT=8000
API_KEY=your_secret_key_here
CACHE_SIZE=5000
SEARCH_DELAY=0.5  # Seconds between searches
MAX_RESULTS=100
```

Load in production:
```bash
# Render dashboard → Environment → Add variables
```

---

## Local Development

### Run Locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Test endpoint
curl "http://localhost:8000/api/search?q=test"
```

### Test Suite:

```bash
# Run comprehensive tests
python test_deployment.py
```

---

## Scaling Beyond 5K/Day

### Optimization Strategies:

1. **Increase Cache Size**
   ```python
   @lru_cache(maxsize=20000)  # From 5K to 20K
   ```

2. **Add Redis Cache** (for multiple instances)
   ```python
   import redis
   r = redis.Redis(host='your-redis-host')
   
   def cached_search(query):
       cached = r.get(f"search:{query}")
       if cached:
           return json.loads(cached)
       
       results = search_with_cache(query)
       r.setex(f"search:{query}", 3600, json.dumps(results))
       return results
   ```

3. **Horizontal Scaling**
   - Deploy multiple instances
   - Use load balancer
   - Share cache via Redis

---

## Support & Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Render Docs**: https://render.com/docs
- **DDG Package**: https://pypi.org/project/duckduckgo-search/

---

## License

MIT License - Free to use and modify

---

## 🎉 Ready to Deploy!

```bash
# Quick deploy checklist:
✅ Code ready (main.py)
✅ Dependencies listed (requirements.txt)
✅ Push to GitHub
✅ Deploy on Render
✅ Test endpoints
✅ Monitor stats
✅ Enjoy free unlimited search! 🚀
```
