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
    query_text = "Represent this sentence for retrieval: " + query

    query_embedding = embed_model.encode([query_text])
    faiss.normalize_L2(query_embedding)

    D, I = index.search(query_embedding, k=20)

    candidates = [data[i]["question"] for i in I[0]]
    answers = [data[i]["answer"] for i in I[0]]

    # 🔥 FILTER: keyword match
    query_words = set(query.lower().split())

    best_score = -999
    best_answer = "No correct legal answer found."

    for i in range(len(candidates)):
        text = (candidates[i] + " " + answers[i]).lower()

        # keyword overlap
        overlap = len(query_words.intersection(text.split()))

        score = D[0][i] + overlap * 0.3

        if score > best_score:
            best_score = score
            best_answer = answers[i]

    return best_answer