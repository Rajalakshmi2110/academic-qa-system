import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class TextbookRetriever:
    def __init__(self):
        """Initialize retriever with pre-built index"""
        self.model = SentenceTransformer("all-mpnet-base-v2")
        self.index = None
        self.metadata = None
        self.load_index()
        
    def load_index(self):
        """Load FAISS index and metadata"""
        try:
            self.index = faiss.read_index("embeddings/data/textbook_index.faiss")
            
            with open("embeddings/data/textbook_metadata.json", "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
                
            print(f"Loaded index with {len(self.metadata)} textbook chunks")
            
        except FileNotFoundError:
            print("Index not found. Run build_index.py first.")
            
    def preprocess_query(self, query):
        """Enhance query for better matching"""
        # Add context keywords for technical terms
        enhancements = {
            "tcp": "tcp transmission control protocol",
            "handshake": "three way handshake connection establishment", 
            "routing": "routing algorithm path selection",
            "protocol": "network protocol communication"
        }
        
        query_lower = query.lower()
        for term, enhancement in enhancements.items():
            if term in query_lower:
                query = f"{query} {enhancement}"
                
        return query
    
    def search(self, query, top_k=5, min_score=0.3):
        """Search for relevant textbook chunks"""
        if not self.index or not self.metadata:
            return []
            
        # Preprocess query
        enhanced_query = self.preprocess_query(query)
        
        # Generate query embedding
        query_embedding = self.model.encode([enhanced_query])
        faiss.normalize_L2(query_embedding)
        
        # Search FAISS index
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if score >= min_score:  # Filter by minimum similarity
                chunk = self.metadata[idx].copy()
                chunk["similarity_score"] = float(score)
                results.append(chunk)
                
        return results
    
    def search_by_unit(self, query, unit, top_k=3):
        """Search within specific syllabus unit"""
        all_results = self.search(query, top_k=20)  # Get more results first
        
        # Filter by unit
        unit_results = [r for r in all_results if r["unit"] == unit]
        
        return unit_results[:top_k]
    
    def get_source_priority_results(self, query, top_k=5):
        """Get results with Stallings prioritized over Kurose"""
        results = self.search(query, top_k=top_k*2)
        
        # Separate by source
        stallings_results = [r for r in results if r["source"] == "stallings"]
        kurose_results = [r for r in results if r["source"] == "kurose"]
        
        # Prioritize Stallings, then Kurose
        prioritized = stallings_results[:top_k//2] + kurose_results[:top_k//2]
        
        return prioritized[:top_k]

def test_retrieval():
    """Test the retrieval system"""
    retriever = TextbookRetriever()
    
    test_queries = [
        "What is TCP protocol?",
        "Explain OSI model layers",
        "How does Ethernet work?",
        "What is IP addressing?",
        "Describe network routing algorithms"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        results = retriever.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result['source']}] {result['unit']} - Score: {result['similarity_score']:.3f}")
            print(f"   {result['text'][:100]}...")

if __name__ == "__main__":
    test_retrieval()