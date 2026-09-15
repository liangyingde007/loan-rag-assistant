def load_document(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
