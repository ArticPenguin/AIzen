import requests
import os

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def naver_search(query: str) -> str:
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        return "검색 키 없음"

    r = requests.get(
        "https://openapi.naver.com/v1/search/webkr.json",
        headers={
            "X-Naver-Client-Id": NAVER_CLIENT_ID,
            "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
        },
        params={"query": query, "display": 1},
        timeout=3
    )

    items = r.json().get("items", [])
    if not items:
        return "검색 결과 없음"

    item = items[0]
    title = item["title"].replace("<b>", "").replace("</b>", "")
    desc = item["description"].replace("<b>", "").replace("</b>", "")
    return f"{title}: {desc}"
