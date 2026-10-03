"""Compose an extractive reply. No external language model is called."""
import re

def needs_numeric_answer(question):
    return bool(re.search(r"多少|几[年天月日点]|比例|百分|数值|金额|最高额度|最低利率|最新利率|月供.*算", question))

def generate(question, context):
    if not context:
        return {"status": "not_found", "answer": "没有在示例知识库中找到足够依据。可以询问提前还款、贷款期限、申请材料或还款安排；本演示不会从文档之外补出答案。"}
    quotes = "\n\n".join(f"[{index + 1}] {section['text']}" for index, section in enumerate(context))
    if needs_numeric_answer(question) and not any(section["has_numeric_terms"] for section in context):
        return {"status": "insufficient", "answer": "找到了相关段落，但示例文档没有提供你询问的具体数值，无法据此给出金额、年限或利率。\n\n相关原文：\n" + quotes}
    return {"status": "answered", "answer": "示例文档中的相关说明：\n\n" + quotes}
