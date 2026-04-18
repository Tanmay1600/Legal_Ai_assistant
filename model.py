import faiss
import json
from sentence_transformers import SentenceTransformer, CrossEncoder

embed_model = SentenceTransformer('BAAI/bge-base-en-v1.5')
reranker = CrossEncoder('BAAI/bge-reranker-base')
# Load FAISS index
index = faiss.read_index("legal_index.faiss")

# Load data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


def get_answer(query):
    # Add BGE prefix
    query_text = "Represent this sentence for retrieval: " + query

    query_embedding = embed_model.encode([query_text])
    faiss.normalize_L2(query_embedding)

    # Get top 20 results
    D, I = index.search(query_embedding, k=20)

    candidates = [data[i]["question"] for i in I[0]]
    answers = [data[i]["answer"] for i in I[0]]

    # Re-rank
    pairs = [[query, c] for c in candidates]
    scores = reranker.predict(pairs)

    best_idx = scores.argmax()

    return answers[best_idx] 