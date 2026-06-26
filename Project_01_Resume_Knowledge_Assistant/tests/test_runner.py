import time
from tests.test_cases import TEST_CASES


# ==========================================================
# Run Tests
# ==========================================================
def run_tests(assistant, category="all"):
    # ---------------------------------------------
    # Run All Categories
    # ---------------------------------------------
    if category == "all":
        for test_name in TEST_CASES:
            run_tests(assistant, test_name)
        return

    # ---------------------------------------------
    # Validate Category
    # ---------------------------------------------
    if category not in TEST_CASES:
        print(f"Unknown category : {category}")
        return

    # ---------------------------------------------
    # Header
    # ---------------------------------------------
    print()
    print("=" * 100)
    print(f"                                     TEST CATEGORY : {category.upper()}")
    print("=" * 100)
    questions = TEST_CASES[category]
    passed = 0

    # ---------------------------------------------
    # Execute Questions
    # ---------------------------------------------
    for number, question in enumerate(questions, start=1):
        print()
        print("-" * 80)
        print(f"✓ TEST {number}")
        print("-" * 80)
        print(f"✓ QUESTION : {question}")

        start = time.perf_counter()

        response = assistant.ask(question)

        elapsed = time.perf_counter() - start

        if response["success"]:
            passed += 1

        print()

        print(f"SUCCESS : {response['success']}")
        print(f"LATENCY : {elapsed:.2f} sec")
        print()
        print("✓ ANSWER")
        print("-" * 80)
        print(response["answer"])
        print()
        print("✓ SOURCES")
        print("-" * 80)
        for source in response["sources"]:
            print(f"{source['source_file']} " f"(Page {source['page']})")

    # ---------------------------------------------
    # Summary
    # ---------------------------------------------
    print()
    print("=" * 100)
    print("                                      SUMMARY")
    print("=" * 100)
    print(f"✓ Tests Passed : {passed}")
    print(f"✓ Total Tests  : {len(questions)}")
    print(f"✓ Success Rate : {(passed / len(questions)) * 100:.1f}%")
