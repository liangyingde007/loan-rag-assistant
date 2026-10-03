def split_text(text, size=500):
    return [
        text[i:i+size]
        for i in range(0,len(text),size)
    ]

def split_sections(document):
    """Keep clause boundaries and source metadata together."""
    return [{
        **section, "document_id": document["id"],
        "document_title": document["title"], "version": document["version"],
        "position": index + 1,
    } for index, section in enumerate(document["sections"])]
