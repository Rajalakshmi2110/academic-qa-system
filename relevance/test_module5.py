from relevance_checker import QuestionRelevanceChecker

def test_module5():
    """Test Module 5 - Question Relevance Checking"""
    checker = QuestionRelevanceChecker()
    
    print("TESTING MODULE 5: QUESTION RELEVANCE CHECKING")
    print("=" * 55)
    
    # Test cases with expected outcomes
    test_cases = [
        # Unit 1 - Data Communication & Networking
        ("What is OSI model?", "RELEVANT", "Unit 1"),
        ("Explain TCP/IP protocol stack", "RELEVANT", "Unit 1"),
        
        # Unit 2 - Physical & Data Link Layers  
        ("How does Ethernet work?", "RELEVANT", "Unit 2"),
        ("What is CSMA/CD?", "RELEVANT", "Unit 2"),
        
        # Unit 3 - Network Layer
        ("Explain IP addressing", "RELEVANT", "Unit 3"),
        ("What is routing algorithm?", "RELEVANT", "Unit 3"),
        
        # Unit 4 - Transport & Application
        ("What is TCP protocol?", "RELEVANT", "Unit 4"),
        ("Explain HTTP protocol", "RELEVANT", "Unit 4"),
        
        # Unit 5 - Network Management
        ("What is SNMP?", "RELEVANT", "Unit 5"),
        ("Explain network monitoring", "RELEVANT", "Unit 5"),
        
        # Partially relevant
        ("What is computer security?", "PARTIALLY_RELEVANT", None),
        
        # Irrelevant
        ("How to cook pasta?", "IRRELEVANT", None),
        ("What is machine learning?", "IRRELEVANT", None)
    ]\n    \n    correct_relevance = 0\n    correct_unit = 0\n    total_tests = len(test_cases)\n    \n    for question, expected_relevance, expected_unit in test_cases:\n        result = checker.check_relevance(question)\n        \n        relevance_match = result['relevance'] == expected_relevance\n        unit_match = expected_unit is None or result['best_unit'] == expected_unit\n        \n        if relevance_match:\n            correct_relevance += 1\n        if unit_match:\n            correct_unit += 1\n            \n        status = \"PASS\" if (relevance_match and unit_match) else \"FAIL\"\n        \n        print(f\"{status}: '{question}'\")\n        print(f\"  Expected: {expected_relevance} | Got: {result['relevance']}\")\n        print(f\"  Score: {result['similarity_score']:.3f}\")\n        \n    print(\"\\n\" + \"=\" * 55)\n    print(f\"RESULTS:\")\n    print(f\"Relevance Accuracy: {correct_relevance}/{total_tests} ({correct_relevance/total_tests*100:.1f}%)\")\n    print(f\"Unit Accuracy: {correct_unit}/{total_tests} ({correct_unit/total_tests*100:.1f}%)\")\n    \n    if correct_relevance >= total_tests * 0.8:  # 80% threshold\n        print(\"\\nSUCCESS: MODULE 5 RELEVANCE CHECKING PASSED\")\n        print(\"Ready for first review demonstration!\")\n    else:\n        print(\"\\nWARNING: MODULE 5 needs improvement\")\n\ndef test_threshold_sensitivity():\n    \"\"\"Test different threshold values\"\"\"\n    checker = QuestionRelevanceChecker()\n    \n    print(\"\\nTHRESHOLD SENSITIVITY ANALYSIS:\")\n    print(\"-\" * 40)\n    \n    test_question = \"What is TCP protocol?\"\n    result = checker.check_relevance(test_question)\n    \n    print(f\"Question: {test_question}\")\n    print(f\"Best Score: {result['similarity_score']:.3f}\")\n    print(f\"Current Thresholds: Relevant={checker.RELEVANT_THRESHOLD}, Partial={checker.PARTIAL_THRESHOLD}\")\n    print(f\"Classification: {result['relevance']}\")\n\nif __name__ == \"__main__\":\n    test_module5()\n    test_threshold_sensitivity()