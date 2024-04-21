from execute_test_cases import execute_test_cases
from generate_bdd_test_cases import generate_bdd_test_cases
from identify_personas import identify_personas, run_accessibility_tests


def main():
    url = "https://www.w3.org/WAI/demos/bad/"
    axe_results = run_accessibility_tests(url)
    personas = identify_personas(axe_results)
    execute_test_cases(personas, url)


if __name__ == "__main__":
    main()