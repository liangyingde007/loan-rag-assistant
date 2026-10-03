"""Topic keyword retrieval with a small character-bigram ranking signal."""
import math
import re
from rag.loader import load_demo_document
from rag.splitter import split_sections

def normalize(text):
    return re.sub(r"[^\w\u4e00-\u9fff]", "", text.lower())

def bigrams(text):
    return {text[index:index + 2] for index in range(len(text) - 1)}

def retrieve(question, top_k=3):
    normalized = normalize(question)
    question_grams = bigrams(normalized)
    hits = []
    for section in split_sections(load_demo_document()):
        matched = [word for word in section["keywords"] if normalize(word) in normalized]
        # Common words such as "贷款" alone must not trigger a fabricated answer.
        if not matched:
            continue
        overlap = len(question_grams & bigrams(normalize(section["title"] + section["text"])))
        score = round(sum(1 + math.log(len(word)) for word in matched) + overlap * .1, 3)
        hits.append({**section, "matched_keywords": matched, "score": score})
    return sorted(hits, key=lambda section: (-section["score"], section["position"]))[:top_k]
