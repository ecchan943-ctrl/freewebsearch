"""
🧪 Test Suite for DuckDuckGo Search API on Render
Tests all endpoints, caching, rate limiting, and advanced search
"""

import requests
import time
from datetime import datetime

# Change this to your Render URL after deployment
BASE_URL = "https://ddg-search-api.onrender.com"

def test_health_check():
    """Test health check endpoint"""
    print("\n❤️ Testing Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "service" in data
    assert "uptime" in data
    
    print(f"✅ Status: {data['status']}")
    print(f"✅ Service: {data['service']}")
    print(f"✅ Uptime: {data['uptime']}")
    print("✅ Health check PASSED\n")


def test_basic_search():
    """Test basic search functionality"""
    print("\n🔍 Testing Basic Search")
    print("="*60)
    
    query = "Python tutorial"
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={"q": query, "n": 5}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["query"] == query
    assert "results" in data
    assert len(data["results"]) <= 5
    assert "cached" in data
    assert "stats" in data
    
    print(f"✅ Query: {data['query']}")
    print(f"✅ Results: {len(data['results'])} found")
    print(f"✅ Cached: {data['cached']}")
    print(f"✅ First result: {data['results'][0]['title'][:50]}...")
    print("✅ Basic search PASSED\n")


def test_caching():
    """Test LRU caching functionality"""
    print("\n💾 Testing Caching")
    print("="*60)
    
    query = "What is artificial intelligence?"
    
    # First request (cold cache)
    print("📝 First request (cold cache)...")
    start = time.time()
    response1 = requests.get(
        f"{BASE_URL}/api/search",
        params={"q": query, "n": 5}
    )
    time1 = time.time() - start
    data1 = response1.json()
    
    print(f"   ⏱️  Time: {time1:.2f}s")
    print(f"   ✅ Cached: {data1['cached']}")
    
    # Second request (should be cached)
    print("\n📝 Second request (should be cached)...")
    start = time.time()
    response2 = requests.get(
        f"{BASE_URL}/api/search",
        params={"q": query, "n": 5}
    )
    time2 = time.time() - start
    data2 = response2.json()
    
    print(f"   ⏱️  Time: {time2:.4f}s")
    print(f"   ✅ Cached: {data2['cached']}")
    
    # Verify caching works
    assert time2 < time1, "Cached request should be faster"
    assert data2["cached"] == True or time2 < 0.1, "Should use cache"
    
    speedup = time1 / max(time2, 0.001)
    print(f"\n✅ Cache speedup: {speedup:.1f}x faster")
    print("✅ Caching PASSED\n")


def test_advanced_search_operators():
    """Test advanced search operators"""
    print("\n🧪 Testing Advanced Search Operators")
    print("="*60)
    
    tests = [
        ("Site restriction", "Python site:github.com", 5),
        ("File type", "ML tutorial filetype:pdf", 5),
        ("Time-based", "AI news 2024", 5),
        ("Exact phrase", '"machine learning" tutorial', 5),
        ("Exclusion", "Python programming -snake", 5),
    ]
    
    for test_name, query, n in tests:
        print(f"\n🔍 Testing: {test_name}")
        print(f"   Query: {query}")
        
        response = requests.get(
            f"{BASE_URL}/api/search",
            params={"q": query, "n": n}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        print(f"   ✅ Results: {len(data['results'])} found")
        
        if data['results']:
            print(f"   📄 First: {data['results'][0]['title'][:60]}...")
        
        time.sleep(0.5)  # Be respectful
    
    print("\n✅ All advanced operators PASSED\n")


def test_rate_limiting_handling():
    """Test that rate limiting is properly handled"""
    print("\n⚡ Testing Rate Limiting Handling")
    print("="*60)
    
    queries = [f"test query {i}" for i in range(1, 11)]
    successful = 0
    failed = 0
    
    start_time = time.time()
    
    for i, query in enumerate(queries, 1):
        try:
            response = requests.get(
                f"{BASE_URL}/api/search",
                params={"q": query, "n": 2}
            )
            
            if response.status_code == 200:
                successful += 1
                print(f"[{i:2d}/10] ✅ Success")
            else:
                failed += 1
                print(f"[{i:2d}/10] ❌ Failed: {response.status_code}")
            
            time.sleep(0.5)  # Built-in delay
            
        except Exception as e:
            failed += 1
            print(f"[{i:2d}/10] ❌ Error: {e}")
    
    total_time = time.time() - start_time
    success_rate = (successful / len(queries)) * 100
    
    print(f"\n📊 Results:")
    print(f"   Successful: {successful}/{len(queries)} ({success_rate:.1f}%)")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Average per query: {total_time/len(queries):.2f}s")
    
    assert success_rate >= 80, f"Success rate too low: {success_rate}%"
    print("✅ Rate limiting handling PASSED\n")


def test_statistics_endpoint():
    """Test statistics endpoint"""
    print("\n📊 Testing Statistics Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/stats")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure
    assert "uptime" in data
    assert "requests" in data
    assert "cache" in data
    assert "search_performance" in data
    
    print(f"✅ Uptime: {data['uptime']}")
    print(f"✅ Total requests: {data['requests']['total']}")
    print(f"✅ Cache hit rate: {data['cache']['hit_rate']}")
    print(f"✅ Success rate: {data['search_performance']['success_rate']}")
    
    if data['requests']['per_day'] > 0:
        print(f"✅ Requests/day: {data['requests']['per_day']:.0f}")
    
    print("✅ Statistics endpoint PASSED\n")


def test_error_handling():
    """Test error handling"""
    print("\n❌ Testing Error Handling")
    print("="*60)
    
    # Test invalid query (too short)
    print("📝 Testing invalid query (too short)...")
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={"q": "a"}  # Too short
    )
    
    assert response.status_code == 400
    print("   ✅ Correctly rejected short query")
    
    # Test missing required parameter
    print("\n📝 Testing missing query parameter...")
    response = requests.get(f"{BASE_URL}/api/search")
    
    assert response.status_code == 422  # Validation error
    print("   ✅ Correctly rejected missing parameter")
    
    # Test invalid results count
    print("\n📝 Testing invalid results count...")
    response = requests.get(
        f"{BASE_URL}/api/search",
        params={"q": "test", "n": 200}  # Over limit
    )
    
    assert response.status_code == 422
    print("   ✅ Correctly rejected excessive results")
    
    print("\n✅ Error handling PASSED\n")


def test_max_results():
    """Test maximum results per query"""
    print("\n📈 Testing Max Results")
    print("="*60)
    
    query = "machine learning tutorial"
    
    # Test different max_results values
    test_values = [5, 10, 20, 50]
    
    for n in test_values:
        print(f"\n🔍 Testing max_results={n}")
        response = requests.get(
            f"{BASE_URL}/api/search",
            params={"q": query, "n": n}
        )
        
        data = response.json()
        received = len(data['results'])
        
        print(f"   Requested: {n}")
        print(f"   Received: {received}")
        
        if n <= 43:
            assert received == n, f"Expected {n} results, got {received}"
            print(f"   ✅ Perfect")
        else:
            print(f"   ⚠️  DDG caps at ~43 results")
        
        time.sleep(0.5)
    
    print("\n✅ Max results testing PASSED\n")


def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("🚀 DUCKDUCKGO SEARCH API - COMPLETE TEST SUITE")
    print("="*60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Base URL: {BASE_URL}")
    print("="*60)
    
    try:
        # Run all tests
        test_health_check()
        test_basic_search()
        test_caching()
        test_advanced_search_operators()
        test_rate_limiting_handling()
        test_statistics_endpoint()
        test_error_handling()
        test_max_results()
        
        # Final summary
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 Your DuckDuckGo Search API is production-ready!")
        print("\n📊 Next Steps:")
        print("   1. Monitor /api/stats regularly")
        print("   2. Set up alerts for rate limit errors")
        print("   3. Enjoy free unlimited search! 🚀")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        raise
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
