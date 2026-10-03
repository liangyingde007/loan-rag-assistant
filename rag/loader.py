import json
from pathlib import Path

DEMO_PATH = Path(__file__).resolve().parents[1] / "knowledge_base" / "demo_rules.json"

def load_document(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def load_demo_document():
    document = json.loads(DEMO_PATH.read_text(encoding="utf-8"))
    assert document["kind"] == "sample" and document["sections"]
    ids = [section["id"] for section in document["sections"]]
    assert len(ids) == len(set(ids))
    return document
