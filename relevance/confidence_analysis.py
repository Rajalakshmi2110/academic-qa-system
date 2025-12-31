"""
CONFIDENCE SCORE ANALYSIS FOR SYNTHETIC QA DATASET
==================================================

This script analyzes confidence scores for all 50 questions in the synthetic dataset
to identify questions with high, medium, and low confidence mappings.

CONFIDENCE SCORING LOGIC:
1. Semantic Similarity: Cosine similarity between question embedding and syllabus unit embeddings
2. Keyword Boosting: Additional confidence for networking terms (TCP, IP, HTTP, etc.)
3. Final Score: min(1.0, semantic_similarity + keyword_boost)

CONFIDENCE LEVELS:
- HIGH: Score >= 0.6 (clear unit mapping)
- MEDIUM: Score 0.35-0.6 (possible cross-unit overlap)  
- LOW: Score < 0.35 (ambiguous mapping)

AMBIGUITY DETECTION:
- Low absolute confidence (< 0.35)
- Small difference between top-2 unit scores (< 0.08)
"""

import json
import numpy as np
from relevance_checker import QuestionRelevanceChecker
import pandas as pd

class ConfidenceAnalyzer:
    def __init__(self):
        self.checker = QuestionRelevanceChecker()
        
    def analyze_question_confidence(self, question, expected_unit):
        """Analyze confidence for a single question"""
        result = self.checker.check_relevance(question)
        
        # Get all unit scores
        unit_scores = [(unit, data['similarity']) for unit, data in result['unit_scores'].items()]
        unit_scores.sort(key=lambda x: x[1], reverse=True)
        
        top_unit, top_score = unit_scores[0]
        second_score = unit_scores[1][1] if len(unit_scores) > 1 else 0.0
        
        # Determine confidence level
        if top_score >= 0.6:
            confidence_level = "HIGH"
        elif top_score >= 0.35:
            confidence_level = "MEDIUM"
        else:
            confidence_level = "LOW"
            
        # Check for ambiguity
        score_gap = top_score - second_score
        is_ambiguous = top_score < 0.35 or score_gap < 0.08
        
        # Determine ambiguity reason
        ambiguity_reason = ""
        if is_ambiguous:
            if top_score < 0.35:
                ambiguity_reason = "Low absolute confidence"
            elif score_gap < 0.08:
                ambiguity_reason = f"Close scores (gap: {score_gap:.3f})"
                
        return {
            'predicted_unit': top_unit,
            'confidence_score': top_score,
            'confidence_level': confidence_level,
            'second_best_score': second_score,
            'score_gap': score_gap,
            'is_ambiguous': is_ambiguous,
            'ambiguity_reason': ambiguity_reason,
            'unit_match': top_unit == expected_unit,
            'all_unit_scores': dict(unit_scores)
        }
    
    def analyze_dataset(self, dataset_path):
        """Analyze confidence for entire dataset"""
        with open(dataset_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
            
        results = []
        
        print("CONFIDENCE SCORE ANALYSIS")
        print("=" * 80)
        print(f"Analyzing {len(questions)} questions...")
        print()
        
        for q in questions:
            analysis = self.analyze_question_confidence(q['question'], q['unit'])
            
            results.append({
                'id': q['id'],
                'question': q['question'][:60] + "..." if len(q['question']) > 60 else q['question'],
                'expected_unit': q['unit'],
                'predicted_unit': analysis['predicted_unit'],
                'confidence_score': analysis['confidence_score'],
                'confidence_level': analysis['confidence_level'],
                'unit_match': analysis['unit_match'],
                'is_ambiguous': analysis['is_ambiguous'],
                'ambiguity_reason': analysis['ambiguity_reason'],
                'score_gap': analysis['score_gap']
            })
            
        return results
    
    def generate_summary_table(self, results):
        """Generate summary table and statistics"""
        df = pd.DataFrame(results)
        
        print("SUMMARY TABLE:")
        print("=" * 120)
        print(f"{'ID':<12} {'Question':<45} {'Expected':<8} {'Predicted':<8} {'Score':<6} {'Level':<8} {'Match':<5} {'Ambiguous'}")
        print("-" * 120)
        
        for _, row in df.iterrows():
            match_symbol = "Y" if row['unit_match'] else "N"
            ambig_symbol = "!" if row['is_ambiguous'] else ""
            
            print(f"{row['id']:<12} {row['question']:<45} {row['expected_unit']:<8} {row['predicted_unit']:<8} "
                  f"{row['confidence_score']:<6.3f} {row['confidence_level']:<8} {match_symbol:<5} {ambig_symbol}")
        
        print("\n" + "=" * 120)
        
        # Statistics
        total = len(results)
        high_conf = len(df[df['confidence_level'] == 'HIGH'])
        medium_conf = len(df[df['confidence_level'] == 'MEDIUM']) 
        low_conf = len(df[df['confidence_level'] == 'LOW'])
        ambiguous = len(df[df['is_ambiguous'] == True])
        correct_predictions = len(df[df['unit_match'] == True])
        
        print("STATISTICS:")
        print(f"Total Questions: {total}")
        print(f"High Confidence (>=0.6): {high_conf} ({high_conf/total*100:.1f}%)")
        print(f"Medium Confidence (0.35-0.6): {medium_conf} ({medium_conf/total*100:.1f}%)")
        print(f"Low Confidence (<0.35): {low_conf} ({low_conf/total*100:.1f}%)")
        print(f"Ambiguous Questions: {ambiguous} ({ambiguous/total*100:.1f}%)")
        print(f"Correct Unit Predictions: {correct_predictions} ({correct_predictions/total*100:.1f}%)")
        
        # Highlight problematic questions
        print("\nPROBLEMATIC QUESTIONS (Low confidence or ambiguous):")
        print("-" * 80)
        problematic = df[(df['confidence_score'] < 0.35) | (df['is_ambiguous'] == True)]
        
        for _, row in problematic.iterrows():
            print(f"{row['id']}: {row['question']}")
            print(f"  Score: {row['confidence_score']:.3f} | Reason: {row['ambiguity_reason']}")
            print()

def main():
    analyzer = ConfidenceAnalyzer()
    dataset_path = "../dataset/synthetic_qa_seed.json"
    
    results = analyzer.analyze_dataset(dataset_path)
    analyzer.generate_summary_table(results)
    
    # Save detailed results
    with open("confidence_analysis_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed results saved to: confidence_analysis_results.json")

if __name__ == "__main__":
    main()