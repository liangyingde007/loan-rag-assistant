from rag.generator import generate
from rag.loader import load_demo_document
from rag.retriever import retrieve

def answer_question(question):
    context = retrieve(question)
    reply = generate(question, context)
    document = load_demo_document()
    citations = [{
        "number": index + 1, "section_id": section["id"], "title": section["title"],
        "text": section["text"], "document_id": section["document_id"],
        "document_title": section["document_title"], "version": section["version"],
        "position": section["position"], "matched_keywords": section["matched_keywords"],
        "source_url": f"/api/documents/{section['document_id']}",
        "score": section["score"],
    } for index, section in enumerate(context)]
    return {
        **reply, "question": question, "context": [section["text"] for section in context],
        "citations": citations, "data_mode": "sample", "retrieval_mode": "topic_keywords",
        "document": {"id": document["id"], "title": document["title"], "version": document["version"]},
        "notice": document["notice"],
        "trace": [
            {"label": "定位主题", "detail": "用条例主题关键词与同义表达匹配问题，不把通用词当作答案依据。"},
            {"label": "检索原文", "detail": f"在示例文档中找到 {len(context)} 个相关段落，保留章节、版本和原文。"},
            {"label": "组织回答", "detail": "返回相关原文并对应引用编号；缺少主题或具体数值时明确提示，不调用大模型。"},
        ],
    }
