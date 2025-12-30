from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

MAX_TOKENS = 250
OVERLAP = 25

def chunk_text(text):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    token_count = 0

    for sent in sentences:
        words = sent.split()
        token_count += len(words)
        current_chunk.append(sent)

        if token_count >= MAX_TOKENS:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-OVERLAP:]
            token_count = sum(len(s.split()) for s in current_chunk)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks
