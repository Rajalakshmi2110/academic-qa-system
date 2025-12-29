#!/usr/bin/env python3
"""
Simple Test Script for Module 2 - Textbook Semantic Indexing
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retriever import TextbookRetriever

def test_basic_functionality():
    """Test basic retrieval functionality"""
    print("=== TESTING MODULE 2 ===")
    
    # Initialize retriever
    retriever = TextbookRetriever()
    
    if not retriever.index or not retriever.metadata:
        print("[FAIL] Index not loaded")
        return False
    
    print("[PASS] Index loaded:", len(retriever.metadata), "chunks")
    
    # Test queries
    test_cases = [
        "TCP protocol",
        "OSI model", 
        "Ethernet",
        "IP addressing",
        "HTTP"
    ]
    
    print("\n=== QUERY TESTS ===")
    for query in test_cases:
        results = retriever.search(query, top_k=2)
        if results:
            print(f"[PASS] '{query}': {len(results)} results (score: {results[0]['similarity_score']:.3f})")
        else:
            print(f"[FAIL] '{query}': No results")
    
    return True

def test_source_coverage():
    """Test textbook source coverage"""
    retriever = TextbookRetriever()
    
    stallings_count = sum(1 for chunk in retriever.metadata if chunk['source'] == 'stallings')
    kurose_count = sum(1 for chunk in retriever.metadata if chunk['source'] == 'kurose')
    
    print(f"\n=== SOURCE COVERAGE ===")
    print(f"Stallings chunks: {stallings_count}")
    print(f"Kurose chunks: {kurose_count}")
    
    if stallings_count > 0 and kurose_count > 0:
        print("[PASS] Both textbooks indexed")
        return True
    else:
        print("[FAIL] Missing textbook content")
        return False

def test_unit_coverage():
    """Test syllabus unit coverage"""
    retriever = TextbookRetriever()
    
    units = set(chunk['unit'] for chunk in retriever.metadata)
    expected_units = {'Unit 1', 'Unit 2', 'Unit 3', 'Unit 4', 'Unit 5'}
    
    print(f"\n=== UNIT COVERAGE ===")
    print(f"Found units: {sorted(units)}")
    
    if expected_units.issubset(units):
        print("[PASS] All 5 units covered")
        return True
    else:
        print(f"[FAIL] Missing units: {expected_units - units}")
        return False

def main():
    """Run all tests"""
    print("TESTING MODULE 2: TEXTBOOK SEMANTIC INDEXING")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_source_coverage, 
        test_unit_coverage
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n=== RESULTS ===")
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("SUCCESS: MODULE 2 ALL TESTS PASSED")
        print("Ready for Module 3!")
    else:
        print("WARNING: MODULE 2 SOME TESTS FAILED")

if __name__ == "__main__":
    main()