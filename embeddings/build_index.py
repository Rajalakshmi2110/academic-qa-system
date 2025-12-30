import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os
from tqdm import tqdm

class TextbookEmbedder:
    def __init__(self, model_name="all-mpnet-base-v2"):
        """Initialize with better Sentence-BERT model"""
        self.model = SentenceTransformer(model_name)
        self.dimension = 768  # all-mpnet-base-v2 embedding dimension
        
    def load_textbook_chunks(self):
        """Load only textbook chunks (highest priority)"""
        textbook_chunks = []
        
        # Load Stallings (primary textbook)
        with open("data/processed/chunks/textbooks/stallings.json", "r", encoding="utf-8") as f:
            stallings = json.load(f)
            textbook_chunks.extend(stallings)
            
        # Load Kurose (secondary textbook)  
        with open("data/processed/chunks/textbooks/kurose.json", "r", encoding="utf-8") as f:
            kurose = json.load(f)
            textbook_chunks.extend(kurose)
            
        print(f"Loaded {len(textbook_chunks)} textbook chunks")
        return textbook_chunks
    
    def generate_embeddings(self, chunks):
        """Generate embeddings for textbook chunks"""
        texts = [chunk["text"] for chunk in chunks]
        
        print("Generating embeddings...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        return embeddings
    
    def build_faiss_index(self, embeddings):
        """Build FAISS index for similarity search"""
        index = faiss.IndexFlatIP(self.dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        index.add(embeddings.astype('float32'))
        
        print(f"Built FAISS index with {index.ntotal} vectors")
        return index
    
    def save_index_and_metadata(self, index, chunks, embeddings):
        """Save FAISS index and chunk metadata"""
        os.makedirs("data", exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(index, "data/textbook_index.faiss")
        
        # Save metadata (without embeddings to save space)
        metadata = []
        for i, chunk in enumerate(chunks):
            metadata.append({
                "id": i,
                "unit": chunk["unit"],
                "topic": chunk["topic"], 
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"]
            })
            
        with open("data/textbook_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
        # Save embeddings separately for analysis
        np.save("data/textbook_embeddings.npy", embeddings)
        
        print("Saved index and metadata to data/")

def main():
    embedder = TextbookEmbedder()
    
    # Load textbook chunks only
    chunks = embedder.load_textbook_chunks()
    
    # Generate embeddings
    embeddings = embedder.generate_embeddings(chunks)
    
    # Build FAISS index
    index = embedder.build_faiss_index(embeddings)
    
    # Save everything
    embedder.save_index_and_metadata(index, chunks, embeddings)
    
    print(f"[OK] Textbook semantic indexing complete!")
    print(f"Total indexed chunks: {len(chunks)}")

if __name__ == "__main__":
    main()