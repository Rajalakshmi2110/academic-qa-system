import json
import numpy as np
from retriever import TextbookRetriever
from collections import defaultdict

class IndexingEvaluator:
    def __init__(self):
        self.retriever = TextbookRetriever()
        
    def evaluate_coverage(self):
        """Evaluate unit and source coverage in the index"""
        metadata = self.retriever.metadata
        
        # Unit distribution
        unit_counts = defaultdict(int)
        source_counts = defaultdict(int)
        
        for chunk in metadata:
            unit_counts[chunk["unit"]] += 1
            source_counts[chunk["source"]] += 1
            
        print("=== COVERAGE ANALYSIS ===")
        print(f"Total indexed chunks: {len(metadata)}")
        print("\nUnit Distribution:")
        for unit in sorted(unit_counts.keys()):
            print(f"  {unit}: {unit_counts[unit]} chunks")
            
        print("\nSource Distribution:")
        for source in sorted(source_counts.keys()):
            print(f"  {source}: {source_counts[source]} chunks")
            
        return unit_counts, source_counts
    
    def test_computer_networks_queries(self):
        """Test retrieval with Computer Networks specific queries"""
        test_queries = [
            # Unit 1 - Introduction & Architecture
            ("What is computer network?", "Unit 1"),
            ("Explain protocol architecture", "Unit 1"),
            ("OSI model layers", "Unit 1"),
            
            # Unit 2 - Data Link Layer
            ("Ethernet protocol", "Unit 2"),
            ("CSMA/CD algorithm", "Unit 2"),
            ("Error detection methods", "Unit 2"),
            
            # Unit 3 - Network Layer
            ("IP addressing scheme", "Unit 3"),
            ("Routing algorithms", "Unit 3"),
            ("IPv4 vs IPv6", "Unit 3"),
            
            # Unit 4 - Transport Layer
            ("TCP vs UDP", "Unit 4"),
            ("Flow control mechanisms", "Unit 4"),
            ("Congestion control", "Unit 4"),
            
            # Unit 5 - Application Layer
            ("HTTP protocol", "Unit 5"),
            ("DNS resolution", "Unit 5"),
            ("Email protocols", "Unit 5")
        ]
        
        print("\n=== QUERY TESTING ===")
        correct_unit_matches = 0
        total_queries = len(test_queries)
        
        for query, expected_unit in test_queries:
            results = self.retriever.search(query, top_k=3, min_score=0.3)
            
            print(f"\nQuery: '{query}' (Expected: {expected_unit})")
            
            if results:
                top_result = results[0]
                retrieved_unit = top_result["unit"]
                score = top_result["similarity_score"]
                source = top_result["source"]
                
                match = "PASS" if retrieved_unit == expected_unit else "FAIL"
                if retrieved_unit == expected_unit:
                    correct_unit_matches += 1
                    
                print(f"  {match} Retrieved: {retrieved_unit} [{source}] (Score: {score:.3f})")
                print(f"    Text: {top_result['text'][:80]}...")
            else:
                print("  FAIL No results found")
                
        accuracy = (correct_unit_matches / total_queries) * 100
        print(f"\nUnit Matching Accuracy: {correct_unit_matches}/{total_queries} ({accuracy:.1f}%)")
        
        return accuracy
    
    def test_source_prioritization(self):
        """Test if Stallings (primary) is prioritized over Kurose"""
        queries = [
            "TCP protocol implementation",
            "Network layer routing",
            "Data link layer protocols"
        ]
        
        print("\n=== SOURCE PRIORITIZATION TEST ===")
        stallings_first_count = 0
        
        for query in queries:
            results = self.retriever.get_source_priority_results(query, top_k=5)
            
            if results:
                stallings_results = [r for r in results if r["source"] == "stallings"]
                kurose_results = [r for r in results if r["source"] == "kurose"]
                
                print(f"\nQuery: '{query}'")
                print(f"  Stallings results: {len(stallings_results)}")
                print(f"  Kurose results: {len(kurose_results)}")
                
                if stallings_results and (not kurose_results or stallings_results[0]["similarity_score"] >= kurose_results[0]["similarity_score"]):
                    stallings_first_count += 1
                    print("  PASS Stallings prioritized correctly")
                else:
                    print("  FAIL Prioritization issue")
                    
        prioritization_rate = (stallings_first_count / len(queries)) * 100
        print(f"\nStallings Prioritization Rate: {stallings_first_count}/{len(queries)} ({prioritization_rate:.1f}%)")
        
        return prioritization_rate
    
    def analyze_similarity_distribution(self):
        """Analyze similarity score distribution"""
        test_query = "What is TCP protocol?"
        results = self.retriever.search(test_query, top_k=20, min_score=0.0)
        
        scores = [r["similarity_score"] for r in results]
        
        print("\n=== SIMILARITY SCORE ANALYSIS ===")
        print(f"Query: '{test_query}'")
        print(f"Results found: {len(results)}")
        
        if scores:
            print(f"Score range: {min(scores):.3f} - {max(scores):.3f}")
            print(f"Average score: {np.mean(scores):.3f}")
            print(f"Results above 0.5: {len([s for s in scores if s > 0.5])}")
            print(f"Results above 0.3: {len([s for s in scores if s > 0.3])}")
            
        return scores
    
    def generate_evaluation_report(self):
        """Generate comprehensive evaluation report"""
        print("=" * 60)
        print("TEXTBOOK SEMANTIC INDEXING EVALUATION REPORT")
        print("=" * 60)
        
        # Coverage analysis
        unit_counts, source_counts = self.evaluate_coverage()
        
        # Query testing
        accuracy = self.test_computer_networks_queries()
        
        # Source prioritization
        prioritization_rate = self.test_source_prioritization()
        
        # Similarity analysis
        scores = self.analyze_similarity_distribution()
        
        # Summary
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        print(f"PASS Total chunks indexed: {len(self.retriever.metadata)}")
        print(f"PASS Units covered: {len(unit_counts)}/5")
        print(f"PASS Sources indexed: {len(source_counts)} (stallings, kurose)")
        print(f"PASS Unit matching accuracy: {accuracy:.1f}%")
        print(f"PASS Source prioritization rate: {prioritization_rate:.1f}%")
        
        if accuracy >= 70 and prioritization_rate >= 60:
            print("\nSUCCESS MODULE 2 SEMANTIC INDEXING: PASSED")
            print("Ready to proceed to Module 3!")
        else:
            print("\nWARNING MODULE 2 SEMANTIC INDEXING: NEEDS IMPROVEMENT")
            print("Consider adjusting similarity thresholds or chunk quality.")

def main():
    evaluator = IndexingEvaluator()
    evaluator.generate_evaluation_report()

if __name__ == "__main__":
    import sys
    import io
    # Set UTF-8 encoding for Windows console
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()