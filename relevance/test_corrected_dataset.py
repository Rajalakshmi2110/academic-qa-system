"""
TEST ALL 50 CORRECTED QUESTIONS
===============================

Test the corrected synthetic dataset to validate final unit assignments
against expected units and measure overall accuracy improvement.
"""

import json

def test_corrected_dataset():
    """Test all 50 questions from corrected dataset"""
    
    # Load corrected dataset
    with open("corrected_synthetic_dataset.json", 'r', encoding='utf-8') as f:
        corrected_data = json.load(f)
    
    print("TESTING ALL 50 CORRECTED QUESTIONS")
    print("=" * 80)
    
    # Track results
    original_correct = 0
    final_correct = 0
    corrections_made = 0
    dual_unit_tags = 0
    
    print(f"{'ID':<12} {'Expected':<8} {'Predicted':<8} {'Final':<8} {'Orig':<4} {'Final':<5} {'Corrected'}")
    print("-" * 80)
    
    for item in corrected_data:
        # Check accuracy
        orig_match = item['predicted_unit'] == item['expected_unit']
        final_match = item['final_unit'] == item['expected_unit']
        
        if orig_match:
            original_correct += 1
        if final_match:
            final_correct += 1
        if item['correction_applied']:
            corrections_made += 1
        if len(item['related_units']) > 1:
            dual_unit_tags += 1
            
        # Display results
        orig_symbol = "Y" if orig_match else "N"
        final_symbol = "Y" if final_match else "N"
        corrected_symbol = "Y" if item['correction_applied'] else ""
        
        print(f"{item['id']:<12} {item['expected_unit']:<8} {item['predicted_unit']:<8} "
              f"{item['final_unit']:<8} {orig_symbol:<4} {final_symbol:<5} {corrected_symbol}")
    
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS:")
    print(f"Total Questions: 50")
    print(f"Original Accuracy: {original_correct}/50 ({original_correct/50*100:.1f}%)")
    print(f"Final Accuracy: {final_correct}/50 ({final_correct/50*100:.1f}%)")
    print(f"Improvement: +{final_correct - original_correct} questions ({(final_correct - original_correct)/50*100:.1f}%)")
    print(f"Corrections Applied: {corrections_made}")
    print(f"Dual-Unit Tags: {dual_unit_tags}")
    
    # Show remaining errors
    errors = [item for item in corrected_data if item['final_unit'] != item['expected_unit']]
    if errors:
        print(f"\nREMAINING ERRORS ({len(errors)} questions):")
        print("-" * 60)
        for error in errors:
            print(f"{error['id']}: Expected {error['expected_unit']}, Got {error['final_unit']}")
            print(f"  Question: {error['question'][:70]}...")
            print(f"  Confidence: {error['confidence']:.3f}")
            if error['correction_applied']:
                print(f"  Correction: {error['correction_reason']}")
            print()
    
    # Show successful corrections
    successful_corrections = [item for item in corrected_data 
                            if item['correction_applied'] and item['final_unit'] == item['expected_unit']
                            and item['predicted_unit'] != item['expected_unit']]
    
    if successful_corrections:
        print(f"SUCCESSFUL CORRECTIONS ({len(successful_corrections)} questions):")
        print("-" * 60)
        for correction in successful_corrections:
            print(f"{correction['id']}: {correction['predicted_unit']} -> {correction['final_unit']}")
            print(f"  Reason: {correction['correction_reason']}")
            print()

if __name__ == "__main__":
    test_corrected_dataset()