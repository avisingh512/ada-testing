from execute_test_cases import execute_test_cases
from generate_bdd_test_cases import generate_bdd_test_cases
from identify_personas import identify_personas


def main():
    url = "https://www.w3.org/WAI/demos/bad/"
    personas = identify_personas(url)
    test_cases = generate_bdd_test_cases(personas, url)
    execute_test_cases(test_cases, url)


if __name__ == "__main__":
    main()