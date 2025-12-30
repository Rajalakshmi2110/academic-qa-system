import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class QuestionRelevanceChecker:
    """Check question relevance against Computer Networks syllabus"""
    
    def __init__(self, syllabus_embeddings_file="syllabus_embeddings.json"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.syllabus_data = self.load_syllabus_embeddings(syllabus_embeddings_file)
        
        # Improved threshold values
        self.RELEVANT_THRESHOLD = 0.28
        self.PARTIAL_THRESHOLD = 0.12
        
    def load_syllabus_embeddings(self, file_path):
        """Load precomputed syllabus embeddings"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert embedding lists back to numpy arrays
            for unit in data:
                data[unit]["embedding"] = np.array(data[unit]["embedding"])
                
            print(f"Loaded syllabus embeddings for {len(data)} units")
            return data
            
        except FileNotFoundError:
            print(f"Syllabus embeddings not found. Run process_syllabus.py first.")
            return {}
    
    def check_relevance(self, question):
        """Check question relevance against syllabus units"""
        if not self.syllabus_data:
            return {"status": "error", "message": "Syllabus data not loaded"}
        
        # Check for non-CN topics first
        question_lower = question.lower()
        non_cn_keywords = [
            "cryptocurrency", "bitcoin", "blockchain", "mining", "wallet",
            "machine learning", "artificial intelligence", "AI", "ML",
            "database", "SQL", "normalization", "DBMS",
            "cooking", "food", "recipe", "pasta",
            "weather", "temperature", "climate",
            "finance", "banking", "stock", "investment"
        ]
        
        if any(keyword in question_lower for keyword in non_cn_keywords):
            return {
                "question": question,
                "relevance": "IRRELEVANT",
                "best_unit": "None",
                "similarity_score": 0.0,
                "message": "Question is not related to Computer Networks syllabus",
                "unit_scores": {}
            }
        
        # Boost confidence for known CN keywords
        cn_keywords = {
            "ip": 0.25, "tcp": 0.25, "udp": 0.25, "http": 0.25, "ftp": 0.25,
            "dns": 0.25, "dhcp": 0.25, "snmp": 0.25, "osi": 0.25, "ethernet": 0.25,
            "routing": 0.20, "switching": 0.20, "protocol": 0.15, "network": 0.10
        }
        
        keyword_boost = 0.0
        for keyword, boost in cn_keywords.items():
            if keyword in question_lower:
                keyword_boost = max(keyword_boost, boost)
        
        # Generate question embedding
        question_embedding = self.model.encode([question])[0]
        
        # Calculate similarity with each unit
        unit_similarities = {}
        
        for unit, unit_data in self.syllabus_data.items():
            similarity = cosine_similarity(
                [question_embedding], 
                [unit_data["embedding"]]
            )[0][0]
            
            # Apply keyword boost
            boosted_similarity = min(1.0, similarity + keyword_boost)
            
            unit_similarities[unit] = {
                "similarity": float(boosted_similarity),
                "topics": unit_data["topics"][:5]  # Top 5 topics for display
            }
        
        # Find best matching unit
        best_unit = max(unit_similarities.keys(), key=lambda u: unit_similarities[u]["similarity"])
        best_score = unit_similarities[best_unit]["similarity"]
        
        # Classify relevance
        if best_score >= self.RELEVANT_THRESHOLD:
            relevance = "RELEVANT"
            message = f"Question is relevant to {best_unit}"
        elif best_score >= self.PARTIAL_THRESHOLD:
            relevance = "PARTIALLY_RELEVANT"
            message = f"Question is partially relevant to {best_unit}"
        else:
            relevance = "IRRELEVANT"
            message = "Question is not related to Computer Networks syllabus"
        
        return {
            "question": question,
            "relevance": relevance,
            "best_unit": best_unit,
            "similarity_score": best_score,
            "message": message,
            "unit_scores": unit_similarities
        }
    
    def batch_check(self, questions):
        """Check relevance for multiple questions"""
        results = []
        for question in questions:
            result = self.check_relevance(question)
            results.append(result)
        return results

def main():
    """Test the relevance checker"""
    checker = QuestionRelevanceChecker()
    
    # Test questions
    test_questions = [
        # Relevant questions
        "What is TCP protocol?",
        "Explain OSI model layers",
        "How does Ethernet work?",
        "What is IP addressing?",
        
        # Partially relevant
        "What is computer security?",
        "Explain database normalization",
        
        # Irrelevant
        "What is machine learning?",
        "How to cook pasta?",
        "What is the weather today?"
    ]
    
    print("QUESTION RELEVANCE CHECKER - MODULE 5 (PARTIAL)")
    print("=" * 60)
    
    for question in test_questions:
        result = checker.check_relevance(question)
        print(f"\nQuestion: {question}")
        print(f"Relevance: {result['relevance']}")
        print(f"Best Unit: {result['best_unit']} (Score: {result['similarity_score']:.3f})")
        print(f"Message: {result['message']}")

if __name__ == "__main__":
    main()