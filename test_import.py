"""
Quick test to verify duckduckgo_search import works
"""

try:
    from duckduckgo_search import DDGS
    print("✅ Import successful!")
    
    # Test a simple search
    print("\n🔍 Testing search...")
    with DDGS() as ddgs:
        results = ddgs.text(
            query="test",
            region="wt-wt",
            safesearch="off",
            max_results=3
        )
        result_list = list(results)
        print(f"✅ Search returned {len(result_list)} results")
        
        if result_list:
            print(f"\n📄 First result:")
            print(f"   Title: {result_list[0].get('title', 'N/A')[:50]}...")
            print(f"   URL: {result_list[0].get('href', 'N/A')}")
            
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
