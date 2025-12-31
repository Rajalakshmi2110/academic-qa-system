"""
RULE-BASED UNIT CORRECTION AND DUAL-UNIT TAGGING
================================================

This module applies keyword-based override rules and dual-unit tagging
to correct unit mappings based on confidence score analysis findings.

CORRECTION LOGIC:
1. Apply keyword-based override rules for clear protocol/concept mappings
2. Add dual-unit tagging for cross-layer concepts
3. Preserve original predictions and confidence scores
4. Generate corrected dataset with final unit assignments
"""

import json
import re
from relevance_checker import QuestionRelevanceChecker

class UnitCorrector:
    def __init__(self):
        self.checker = QuestionRelevanceChecker()
        
        # Define keyword-based override rules
        self.override_rules = {
            'Unit 1': [
                # Fundamental concepts
                'osi model', 'tcp/ip model', 'protocol architecture', 'layered architecture',
                'host', 'end system', 'edge network', 'core network', 'presentation layer',
                'session layer', 'application layer'
            ],
            'Unit 2': [
                # Physical and Data Link Layer
                'ethernet', 'csma/cd', 'csma/ca', 'mac address', 'llc', 'media access',
                'fiber optic', 'twisted pair', 'wireless', '802.11', 'token ring',
                'vlan', 'switch', 'hub', 'collision domain', 'crc', 'hamming distance',
                'bit stuffing', 'stop-and-wait', 'flow control'
            ],
            'Unit 3': [
                # Network Layer
                'ip address', 'ipv4', 'ipv6', 'routing', 'router', 'nat', 'dhcp',
                'icmp', 'bgp', 'ospf', 'rip', 'cidr', 'subnet', 'tunneling',
                'link-state', 'distance-vector', 'datagram', 'virtual circuit'
            ],
            'Unit 4': [
                # Transport and Application Layer
                'tcp', 'udp', 'http', 'ftp', 'smtp', 'dns', 'socket', 'port',
                'three-way handshake', 'congestion control', 'mime', 'email',
                'web', 'file transfer', 'name resolution', 'stateless', 'connection'
            ],
            'Unit 5': [
                # Network Management
                'snmp', 'mib', 'smi', 'network management', 'monitoring', 'sdn',
                'openflow', 'netconf', 'yang', 'wireshark', 'fault management',
                'northbound api', 'southbound api', 'controller'
            ]
        }
        
        # Define dual-unit concepts (cross-layer)
        self.dual_unit_concepts = {
            ('Unit 1', 'Unit 4'): [
                'transport layer', 'network layer', 'layer separation', 'protocol stack'
            ],
            ('Unit 2', 'Unit 4'): [
                'flow control', 'error control', 'reliability', 'acknowledgment'
            ],
            ('Unit 1', 'Unit 3'): [
                'gateway', 'router', 'network architecture', 'switching'
            ],
            ('Unit 3', 'Unit 4'): [
                'end-to-end', 'host-to-host', 'addressing'
            ],
            ('Unit 1', 'Unit 5'): [
                'network management', 'protocol management', 'architecture management'
            ]
        }
    
    def find_keyword_matches(self, question):
        """Find keyword matches for override rules"""
        question_lower = question.lower()
        matches = {}
        
        for unit, keywords in self.override_rules.items():
            for keyword in keywords:
                if keyword in question_lower:
                    if unit not in matches:
                        matches[unit] = []
                    matches[unit].append(keyword)
        
        return matches
    
    def find_dual_unit_matches(self, question):
        """Find dual-unit concept matches"""
        question_lower = question.lower()
        matches = []
        
        for (unit1, unit2), keywords in self.dual_unit_concepts.items():
            for keyword in keywords:
                if keyword in question_lower:
                    matches.append((unit1, unit2, keyword))
        
        return matches
    
    def apply_correction_rules(self, question, predicted_unit, confidence_score):
        """Apply correction rules to determine final unit assignment"""
        
        # Find keyword matches
        keyword_matches = self.find_keyword_matches(question)
        dual_matches = self.find_dual_unit_matches(question)
        
        # Initialize result
        result = {
            'predicted_unit': predicted_unit,
            'final_unit': predicted_unit,
            'related_units': [predicted_unit],
            'confidence': confidence_score,
            'correction_applied': False,
            'correction_reason': '',
            'keyword_matches': keyword_matches,
            'dual_unit_matches': dual_matches
        }
        
        # Apply override rules (strongest matches first)
        if keyword_matches:
            # Count matches per unit
            match_counts = {unit: len(keywords) for unit, keywords in keyword_matches.items()}
            strongest_unit = max(match_counts.keys(), key=lambda u: match_counts[u])
            
            # Apply override if confidence is low or strong keyword match
            if confidence_score < 0.4 or match_counts[strongest_unit] >= 2:
                result['final_unit'] = strongest_unit
                result['correction_applied'] = True
                result['correction_reason'] = f"Keyword override: {keyword_matches[strongest_unit]}"
        
        # Apply dual-unit tagging
        if dual_matches:
            dual_units = set()
            for unit1, unit2, keyword in dual_matches:
                dual_units.add(unit1)
                dual_units.add(unit2)
            
            # Add dual units to related_units
            result['related_units'] = list(set(result['related_units'] + list(dual_units)))
            
            # If current final_unit not in dual units, consider override
            if result['final_unit'] not in dual_units and confidence_score < 0.5:
                # Choose the dual unit with higher semantic similarity
                best_dual_unit = max(dual_units, key=lambda u: self._get_unit_similarity(question, u))
                result['final_unit'] = best_dual_unit
                result['correction_applied'] = True
                result['correction_reason'] = f"Dual-unit override: {[m[2] for m in dual_matches]}"
        
        return result
    
    def _get_unit_similarity(self, question, unit):
        """Get similarity score for a specific unit"""
        relevance_result = self.checker.check_relevance(question)
        return relevance_result['unit_scores'].get(unit, {}).get('similarity', 0.0)
    
    def correct_dataset(self, dataset_path, output_path):
        """Apply corrections to entire dataset"""
        with open(dataset_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        
        corrected_data = []
        
        print("APPLYING RULE-BASED CORRECTIONS")
        print("=" * 60)
        
        corrections_applied = 0
        dual_tags_added = 0
        
        for q in questions:
            # Get original prediction
            relevance_result = self.checker.check_relevance(q['question'])
            predicted_unit = relevance_result['best_unit']
            confidence = relevance_result['similarity_score']
            
            # Apply corrections
            correction = self.apply_correction_rules(q['question'], predicted_unit, confidence)
            
            # Create corrected entry
            corrected_entry = {
                'id': q['id'],
                'question': q['question'],
                'expected_unit': q['unit'],
                'predicted_unit': correction['predicted_unit'],
                'final_unit': correction['final_unit'],
                'related_units': correction['related_units'],
                'confidence': correction['confidence'],
                'correction_applied': correction['correction_applied'],
                'correction_reason': correction['correction_reason']
            }
            
            corrected_data.append(corrected_entry)
            
            # Track statistics
            if correction['correction_applied']:
                corrections_applied += 1
            if len(correction['related_units']) > 1:
                dual_tags_added += 1
            
            # Print significant corrections
            if correction['correction_applied'] or len(correction['related_units']) > 1:
                print(f"{q['id']}: {correction['predicted_unit']} -> {correction['final_unit']}")
                if correction['correction_reason']:
                    print(f"  Reason: {correction['correction_reason']}")
                if len(correction['related_units']) > 1:
                    print(f"  Related units: {correction['related_units']}")
                print()
        
        # Save corrected dataset
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(corrected_data, f, indent=2, ensure_ascii=False)
        
        print("=" * 60)
        print(f"CORRECTION SUMMARY:")
        print(f"Total questions: {len(questions)}")
        print(f"Corrections applied: {corrections_applied}")
        print(f"Dual-unit tags added: {dual_tags_added}")
        print(f"Corrected dataset saved to: {output_path}")
        
        return corrected_data

def main():
    corrector = UnitCorrector()
    
    # Apply corrections to synthetic dataset
    dataset_path = "../dataset/synthetic_qa_seed.json"
    output_path = "corrected_synthetic_dataset.json"
    
    corrected_data = corrector.correct_dataset(dataset_path, output_path)
    
    # Generate accuracy report
    correct_final = sum(1 for item in corrected_data if item['final_unit'] == item['expected_unit'])
    correct_predicted = sum(1 for item in corrected_data if item['predicted_unit'] == item['expected_unit'])
    
    print(f"\nACCURACY COMPARISON:")
    print(f"Original predictions: {correct_predicted}/50 ({correct_predicted/50*100:.1f}%)")
    print(f"After corrections: {correct_final}/50 ({correct_final/50*100:.1f}%)")
    print(f"Improvement: {correct_final - correct_predicted} questions")

if __name__ == "__main__":
    main()