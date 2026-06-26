from src.bootstrap import initialize_system


# ==========================================================
# Main
# ==========================================================
def main():
    assistant, stats = initialize_system()
    questions = [
        "Which projects used Python?",
        "Which company was that for?",
        "What technologies were used?",
    ]
    for question in questions:
        print()
        print("=" * 100)
        print(f"✓ QUESTION : {question}")
        print("=" * 100)

        answer = assistant.ask(question)

        print()
        print("✓ ANSWER")
        print("-" * 80)
        print(answer)


# ==========================================================
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
