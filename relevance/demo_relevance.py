from relevance_checker import QuestionRelevanceChecker

def interactive_demo():
    """Interactive demo for question relevance checking"""
    checker = QuestionRelevanceChecker()
    
    print("MODULE 5 (PARTIAL): QUESTION RELEVANCE CHECKER")
    print("=" * 50)
    print("Enter questions to check relevance against Computer Networks syllabus")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        if not question:
            continue
            
        result = checker.check_relevance(question)
        
        print(f"\n--- RELEVANCE CHECK RESULT ---")
        print(f"Status: {result['relevance']}")
        print(f"Best Match: {result['best_unit']}")
        print(f"Confidence: {result['similarity_score']:.3f}")
        print(f"Feedback: {result['message']}")
        
        if result['relevance'] != 'IRRELEVANT':
            topics = result['unit_scores'][result['best_unit']]['topics']
            print(f"Related Topics: {', '.join(topics[:3])}")
        
        print("-" * 50)

if __name__ == "__main__":
    interactive_demo()