from brain import think

def main():
    print("sanE_bot 실행됨 (무료 버전)")
    print("종료하려면 exit 입력")

    while True:
        q = input("\n질문 > ")
        if q.lower() in ["exit", "quit"]:
            print("sanE_bot 종료")
            break

        answer = think(q)
        print("\n[답변]")
        print(answer)


if __name__ == "__main__":
    main()
