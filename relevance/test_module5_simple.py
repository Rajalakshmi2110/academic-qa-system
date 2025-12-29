from relevance_checker import QuestionRelevanceChecker

def test_module5():
    """Test Module 5 - Question Relevance Checking"""
    checker = QuestionRelevanceChecker()
    
    print("TESTING MODULE 5: QUESTION RELEVANCE CHECKING")
    print("=" * 55)
    
    # Test cases with expected outcomes
    test_cases = [
        ("What is OSI model?", "RELEVANT"),
        ("What is TCP protocol?", "RELEVANT"), 
        ("How does Ethernet work?", "RELEVANT"),
        ("Explain IP addressing", "RELEVANT"),
        ("What is SNMP?", "RELEVANT"),
        ("What is computer security?", "PARTIALLY_RELEVANT"),
        ("How to cook pasta?", "IRRELEVANT"),
        ("What is machine learning?", "IRRELEVANT")
    ]
    
    correct = 0
    total = len(test_cases)
    
    for question, expected in test_cases:
        result = checker.check_relevance(question)
        actual = result['relevance']
        
        match = actual == expected
        if match:
            correct += 1
            
        status = "PASS" if match else "FAIL"
        print(f"{status}: '{question}'")
        print(f"  Expected: {expected} | Got: {actual}")
        print(f"  Score: {result['similarity_score']:.3f}")
        
    print("\n" + "=" * 55)
    print(f"ACCURACY: {correct}/{total} ({correct/total*100:.1f}%)")
    
    if correct >= total * 0.7:
        print("SUCCESS: MODULE 5 PASSED")
    else:
        print("WARNING: MODULE 5 needs improvement")

if __name__ == "__main__":
    test_module5()