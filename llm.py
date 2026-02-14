import os

import google.generativeai as genai

from rag import search_docs
from search import naver_search

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

SEARCH_KEYWORDS = [
    "누구", "뭐", "어디", "언제", "왜",
    "가격", "주가", "뉴스", "오늘", "현재"
]

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def call_llm_stream(prompt: str):
    if not GEMINI_API_KEY:
        yield "GEMINI_API_KEY가 설정되지 않았습니다."
        return

    model = genai.GenerativeModel(GEMINI_MODEL)
    stream = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 256,
        },
        stream=True,
    )

    for chunk in stream:
        text = getattr(chunk, "text", "")
        if text:
            yield text


def need_search(text: str) -> bool:
    return any(k in text for k in SEARCH_KEYWORDS)


def ask_llm(user_message: str):
    # 1. RAG first
    docs = search_docs(user_message)

    if docs:
        context = "\n".join(docs)
        prompt = (
            "Answer the question using ONLY the following document context.\n"
            "Do NOT guess.\n"
            "Summarize in Korean, max 3 lines.\n\n"
            f"Context:\n{context}\n\n"
            f"Question:\n{user_message}"
        )
        return call_llm_stream(prompt)

    # 2. Web search
    if need_search(user_message):
        info = naver_search(user_message)
        prompt = (
            "Summarize the following information in Korean.\n"
            "Max 3 lines.\n\n"
            f"{info}"
        )
        return call_llm_stream(prompt)

    # 3. Normal LLM
    prompt = (
        "Answer the following question in Korean.\n"
        "Max 3 lines.\n\n"
        f"{user_message}"
    )
    return call_llm_stream(prompt)
