import json
import os
from search import naver_search, parse_search_result

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")


def load_knowledge():
    knowledge = {}
    for file in os.listdir(KNOWLEDGE_DIR):
        if file.endswith(".json"):
            with open(os.path.join(KNOWLEDGE_DIR, file), "r", encoding="utf-8") as f:
                knowledge.update(json.load(f))
    return knowledge


LOCAL_KNOWLEDGE = load_knowledge()


def local_answer(question):
    for key, value in LOCAL_KNOWLEDGE.items():
        if key in question:
            return f"[지식DB]\n{value}"
    return None


def summarize(results):
    if not results:
        return "관련된 검색 결과를 찾지 못했습니다."

    top = results[:2]  # 상위 2개만 사용
    summary = "네이버 검색 기준으로 보면,\n"
    for i, r in enumerate(top, 1):
        summary += f"{i}. {r}\n"

    return summary.strip()


def think(question):
    # 1️⃣ 로컬 지식 우선
    local = local_answer(question)
    if local:
        return local

    # 2️⃣ 네이버 검색
    search_data = naver_search(question)
    results = parse_search_result(search_data)

    # 3️⃣ 규칙 기반 요약
    return summarize(results)
