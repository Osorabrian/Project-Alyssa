from agent_core import AlyssaAgent


def main() -> None:
    agent = AlyssaAgent()

    print("Alyssa - Jessup CS Student Support Agent")
    print("Type a question, or 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        answer, _ = agent.answer(question)
        print(f"\nAgent:\n{answer}\n")


if __name__ == "__main__":
    main()
