import json
import os

MEMORY_FILE = "memory.json"
MAX_MEMORY = 6   # 최근 대화 6개만 기억


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-MAX_MEMORY:], f, ensure_ascii=False, indent=2)


def add_memory(role, text):
    memory = load_memory()
    memory.append({"role": role, "text": text})
    save_memory(memory)


def get_memory_text():
    memory = load_memory()
    result = ""
    for m in memory:
        result += f"{m['role']}: {m['text']}\n"
    return result.strip()
