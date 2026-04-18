import json

files = [
    "constitution_qa.json",
    "crpc_qa.json",
    "ipc_qa.json"
]

data = []

# Load all data
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        data.extend(json.load(f))

print(f"Original size: {len(data)}")

cleaned = []
seen = set()

for item in data:
    q = item["question"].strip()
    a = item["answer"].strip()

    # ❌ Remove very short / useless answers
    if len(a) < 25:
        continue

    # ❌ Remove junk answers
    bad_patterns = [
        "chapter",
        "form no",
        "section 1",
        "rule",
        "act ",
        "definition",
        "title",
        "preliminary"
    ]

    if any(bp in a.lower() for bp in bad_patterns):
        continue

    # ❌ Remove duplicates (based on question)
    key = q.lower()
    if key in seen:
        continue
    seen.add(key)

    # ✅ Normalize question
    q = q.replace("?", "").strip().capitalize() + "?"

    cleaned.append({
        "question": q,
        "answer": a
    })

print(f"Cleaned size: {len(cleaned)}")

# Save cleaned file
with open("cleaned_data.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=2)

print("✅ Cleaned dataset saved as cleaned_data.json")