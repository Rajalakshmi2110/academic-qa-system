#!/usr/bin/env python3
"""
Interactive Demo for Module 2 - Textbook Semantic Indexing
"""

from retriever import TextbookRetriever

def demo_search():
    """Interactive search demo"""
    retriever = TextbookRetriever()
    
    print("MODULE 2 DEMO: Textbook Semantic Search")
    print("=" * 45)
    print(f"Loaded {len(retriever.metadata)} textbook chunks")
    print("Enter Computer Networks questions (or 'quit' to exit)")
    print()
    
    while True:
        query = input("Query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
            
        if not query:
            continue
            
        results = retriever.search(query, top_k=3)
        
        if results:
            print(f"\nFound {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. [{result['source'].upper()}] {result['unit']} (Score: {result['similarity_score']:.3f})")
                print(f"   {result['text'][:120]}...")
        else:
            print("No results found.")
        
        print("-" * 45)

if __name__ == "__main__":
    demo_search()