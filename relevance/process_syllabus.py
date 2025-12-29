import json
import re
from sentence_transformers import SentenceTransformer

class SyllabusProcessor:
    """Process syllabus content for relevance checking"""
    
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
    def extract_clean_topics(self, syllabus_file):
        """Extract clean topic keywords from syllabus"""
        with open(syllabus_file, 'r', encoding='utf-8') as f:
            syllabus_data = json.load(f)
        
        # Define unit-specific keywords based on actual syllabus content
        unit_topics = {
            "Unit 1": ["data communication", "networking", "OSI", "TCP/IP", "protocol architecture", "layered architecture", "reference models", "hosts", "switches", "routers", "gateways"],
            "Unit 2": ["physical layer", "data link layer", "DLL", "sublayers", "ethernet", "CSMA/CD", "token ring", "VLAN", "wireless", "bluetooth", "framing", "flow control", "error detection", "collision domain", "CSMA/CA", "IEEE 802.11", "MAC", "LLC", "broadcast networks"],
            "Unit 3": ["network layer", "packet switching", "routing", "distance vector", "link state", "RIP", "OSPF", "BGP", "IPv4", "IPv6", "IP addressing", "addressing", "subnetting", "subnet", "CIDR", "VLSM", "DHCP", "NAT", "ICMP", "IP packet format", "effective IP address management"],
            "Unit 4": ["transport layer", "TCP", "UDP", "connection establishment", "flow control", "congestion control", "application layer", "HTTP", "HTTPS", "web protocols", "FTP", "email protocols", "DNS", "sockets", "port numbers", "client server"],
            "Unit 5": ["network monitoring", "network management", "SNMP", "MIB", "wireshark", "fault detection", "SDN", "control plane", "data plane", "network provisioning"]
        }
        
        return unit_topics
    
    def create_unit_embeddings(self, unit_topics):
        """Create embeddings for each unit's topics"""
        unit_embeddings = {}
        
        for unit, topics in unit_topics.items():
            # Combine topics into descriptive text
            topic_text = " ".join(topics)
            embedding = self.model.encode([topic_text])
            unit_embeddings[unit] = {
                "topics": topics,
                "text": topic_text,
                "embedding": embedding[0]
            }
            
        return unit_embeddings
    
    def save_syllabus_embeddings(self, output_file):
        """Process and save syllabus embeddings"""
        # Extract topics
        unit_topics = self.extract_clean_topics("../data/processed/chunks/syllabus.json")
        
        # Create embeddings
        unit_embeddings = self.create_unit_embeddings(unit_topics)
        
        # Save for relevance checker
        import numpy as np
        
        syllabus_data = {}
        for unit, data in unit_embeddings.items():
            syllabus_data[unit] = {
                "topics": data["topics"],
                "text": data["text"],
                "embedding": data["embedding"].tolist()  # Convert numpy to list for JSON
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(syllabus_data, f, indent=2, ensure_ascii=False)
            
        print(f"Syllabus embeddings saved to {output_file}")
        return syllabus_data

def main():
    processor = SyllabusProcessor()
    processor.save_syllabus_embeddings("syllabus_embeddings.json")

if __name__ == "__main__":
    main()