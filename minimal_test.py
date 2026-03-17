"""
Minimal FastAPI app to test duckduckgo_search
"""

from fastapi import FastAPI
from duckduckgo_search import DDGS

app = FastAPI()

@app.get("/test")
def test_search():
    """Simple test endpoint"""
    try:
        ddgs = DDGS()
        results = ddgs.text(
            query="test",
            max_results=3
        )
        result_list = list(results)
        return {
            "success": True,
            "count": len(result_list),
            "results": result_list[:2] if result_list else []
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
