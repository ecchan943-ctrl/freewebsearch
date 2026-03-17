# 🚀 Quick Deploy Guide - 5 Minutes to Production

## Step-by-Step Deployment

### **Step 1: Push to GitHub** (2 minutes)

```bash
# Navigate to project
cd render_ddg_search

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "🚀 DuckDuckGo Search API - Ready for Render"

# Create GitHub repository (go to github.com/new)
# Then connect your repo:
git remote add origin https://github.com/YOUR_USERNAME/ddg-search-api.git
git branch -M main
git push -u origin main
```

---

### **Step 2: Deploy on Render** (3 minutes)

#### **Option A: Via Render Dashboard (Easiest)**

1. **Go to Render**: https://render.com
2. **Sign up/Login** (use GitHub login for easiest setup)
3. **Click "New +"** → **"Web Service"**
4. **Connect Repository**:
   - Select your `ddg-search-api` repository
   - Click "Connect"

5. **Configure Service**:
   ```
   Name: ddg-search-api
   Region: Oregon (closest to you)
   Branch: main
   
   Root Directory: (leave blank)
   
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python main.py
   
   Instance Type: Free ✅
   ```

6. **Advanced Settings** (optional):
   - Auto-Deploy: ✅ Enabled (recommended)
   - Health Check Path: `/`

7. **Click "Create Web Service"**

8. **Wait 2-3 minutes** for deployment...

9. **Done!** Your API is live at:
   ```
   https://ddg-search-api.onrender.com
   ```

---

### **Step 3: Test Your API** (1 minute)

```bash
# Replace with YOUR Render URL
BASE_URL="https://ddg-search-api.onrender.com"

# Test health check
curl $BASE_URL/

# Test search
curl "$BASE_URL/api/search?q=Python+tutorial&n=5"

# Test caching (run twice)
curl "$BASE_URL/api/search?q=AI+tutorial&n=5"
curl "$BASE_URL/api/search?q=AI+tutorial&n=5"

# Check stats
curl $BASE_URL/api/stats
```

---

## 🎉 That's It! You're Live!

### **Your API Endpoints:**

```
Base URL: https://ddg-search-api.onrender.com

GET /                          # Health check
GET /api/search?q={query}      # Search endpoint
GET /api/stats                 # Statistics
GET /api/cache/info            # Cache info
GET /api/cache/clear           # Clear cache
```

---

## 📊 Monitor Your API

### **Check Stats Daily:**
```bash
curl https://ddg-search-api.onrender.com/api/stats | jq
```

### **Key Metrics:**
- **Cache Hit Rate**: Should be >60%
- **Success Rate**: Should be >95%
- **Rate Limit Errors**: Should be 0
- **Requests/Day**: Track your usage

---

## ⚙️ Configuration Options

### **Environment Variables** (Optional)

In Render Dashboard → Environment → Add Variable:

```
PORT=8000                    # Default port
CACHE_SIZE=5000              # LRU cache size
SEARCH_DELAY=0.5             # Delay between searches (seconds)
MAX_RESULTS=100              # Maximum results per query
API_KEY=your_secret_key      # Optional authentication
```

---

## 🔧 Troubleshooting

### **Issue: Deployment Failed**

**Check Logs in Render Dashboard:**
```
1. Go to your service dashboard
2. Click "Logs" tab
3. Look for errors
4. Common fixes:
   - Missing requirements.txt? → Add it
   - Wrong start command? → Use: python main.py
   - Port issue? → Render auto-detects PORT env variable
```

---

### **Issue: Slow Response Times**

**Solutions:**
1. **Enable Caching** (already enabled by default)
   ```bash
   curl "https://YOUR_URL/api/search?q=test&use_cache=true"
   ```

2. **Check Cache Performance**
   ```bash
   curl https://YOUR_URL/api/stats | jq '.cache'
   ```

3. **Increase Cache Size** (if needed)
   - Edit `main.py`: `@lru_cache(maxsize=10000)`
   - Redeploy (auto-deploys on git push)

---

### **Issue: Rate Limiting**

**Already handled automatically!** The code includes:
- ✅ 0.5s delay between searches
- ✅ Exponential backoff on retry
- ✅ Exception handling
- ✅ Graceful fallback

If you still see rate limits:
1. Check `/api/stats` for `rate_limit_errors`
2. Increase delay in `main.py`:
   ```python
   await asyncio.sleep(1.0)  # Change from 0.5 to 1.0
   ```
3. Redeploy

---

## 📈 Scaling Tips

### **For Up to 5K Searches/Day:**
- ✅ Free tier is perfect
- ✅ No changes needed
- ✅ Just monitor stats

### **For 10K+ Searches/Day:**
1. **Upgrade to Hobby Plan** ($7/month)
   - Unlimited hours (free tier has 500 hours/month limit)
   - Better performance

2. **Optimize Caching**
   ```python
   @lru_cache(maxsize=20000)  # Increase from 5K to 20K
   ```

3. **Add Redis** (for multiple instances)
   - Render Redis: $7/month
   - Shared cache across instances

---

## 🔐 Security (Production)

### **Add API Key Authentication:**

**1. Update main.py:**
```python
from fastapi import Header, HTTPException

@app.get("/api/search")
async def search(
    q: str,
    n: int = 10,
    x_api_key: str = Header(None)
):
    # Check API key
    if x_api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # ... rest of search logic
```

**2. Set Environment Variable in Render:**
```
API_KEY = your_super_secret_key_here
```

**3. Clients must include header:**
```bash
curl -H "x-api-key: your_super_secret_key_here" \
     "https://YOUR_URL/api/search?q=test"
```

---

## 💰 Cost Breakdown

### **Free Tier (Up to 5K searches/day):**
```
Render Web Service (Free):
- 500 hours/month free (~20 days)
- 512MB RAM
- Sufficient for testing & low volume

Total: $0/month ✅
```

### **Hobby Plan (Unlimited):**
```
Render Web Service (Hobby):
- Unlimited hours
- Better performance
- Priority support

Total: $7/month
```

### **Recommended Setup:**
```
Start with Free Tier → Monitor usage → Upgrade if needed
```

---

## 🎯 Next Steps After Deployment

### **Day 1:**
- ✅ Deploy and test basic functionality
- ✅ Run test suite: `python test_deployment.py`
- ✅ Check stats endpoint

### **Week 1:**
- ✅ Monitor daily usage via `/api/stats`
- ✅ Check cache hit rate (target >60%)
- ✅ Verify no rate limit errors

### **Month 1:**
- ✅ Analyze usage patterns
- ✅ Optimize cache size if needed
- ✅ Consider upgrading if approaching limits

---

## 📞 Support

### **Render Documentation:**
- https://render.com/docs

### **FastAPI Documentation:**
- https://fastapi.tiangolo.com

### **DuckDuckGo Search Package:**
- https://pypi.org/project/duckduckgo-search/

---

## 🎉 Success Checklist

```
✅ Code ready (main.py included)
✅ Dependencies listed (requirements.txt)
✅ Pushed to GitHub
✅ Deployed on Render
✅ Tested endpoints
✅ Monitoring stats
✅ Cache working (>60% hit rate)
✅ No rate limit errors
✅ API serving real users

CONGRATULATIONS! 🚀
You now have a production-ready DuckDuckGo Search API!
```

---

**Deployment Time:** ~5 minutes  
**Monthly Cost:** $0 (free tier)  
**Capacity:** 5,000+ searches/day  
**Maintenance:** Set and forget!  

**Enjoy your free unlimited search API!** 🎊
