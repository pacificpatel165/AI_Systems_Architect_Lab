import argparse
from src.bootstrap import initialize_system
from tests.test_runner import run_tests


# ==========================================================
# Normal Application
# ==========================================================
def run_application(assistant):
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

        response = assistant.ask(question)
        print()
        print("✓ ANSWER")
        print("-" * 80)
        print(response["answer"])


# ==========================================================
# Parse Command Line Arguments
# ==========================================================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Resume Knowledge Assistant",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--test",
        metavar="CATEGORY",
        choices=[
            "retrieval",
            "metadata",
            "followup",
            "parent",
            "compression",
            "negative",
            "all",
        ],
        help=(
            "Run pipeline validation tests. Examples:\n"
            "retrieval, metadata, followup, parent, compression, negative, all"
        ),
    )


# ==========================================================
# Main
# ==========================================================
def main():
    args = parse_arguments()
    assistant, stats = initialize_system()

    # -----------------------------------------
    # Test Mode
    # -----------------------------------------
    if args.test:
        run_tests(assistant, args.test)

    # -----------------------------------------
    # Normal Mode
    # -----------------------------------------
    else:
        run_application(assistant)


# ==========================================================
# Entry Point
# ==========================================================
if __name__ == "__main__":
    main()
