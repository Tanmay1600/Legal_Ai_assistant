import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('BAAI/bge-base-en-v1.5')
# Load datasets
files = ["cleaned_data.json"]

data = []

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data.extend(json.load(f))

# Prepare questions with BGE prefix
questions = [
    "Represent this sentence for retrieval: " + item["question"]
    for item in data
]

# Generate embeddings
embeddings = model.encode(
    questions,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True
)

# Convert to float32
embeddings = embeddings.astype("float32")

# Normalize for cosine similarity
faiss.normalize_L2(embeddings)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save index
faiss.write_index(index, "legal_index.faiss")

# Save data
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f)

print("✅ Index built and saved!")