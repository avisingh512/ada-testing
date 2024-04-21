import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
import re
from behave import given, when, then  # Assuming these are the BDD decorators you're using

def execute_test_cases(test_cases, url):
    driver = webdriver.Chrome()

    # Define the BDD decorators
    def step(arg):
        pass

    # Assume these are the BDD decorators you're using
    given = step
    when = step
    then = step

    for test_case in test_cases:
        # Extract the persona from the test_case using regex
        match = re.search(r"the website is accessible for (.+?) users", test_case)
        test_case_name = match.group(1) if match else "Unknown"

        with allure.step(f"Executing test case: {test_case_name}"):
            try:
                if isinstance(test_case, str) and test_case.strip():
                    exec(test_case)

                allure.attach(body=f"Test case {test_case_name} passed", name="test_result", attachment_type=AttachmentType.TEXT)
            except AssertionError as e:
                allure.attach(body=f"Test case {test_case_name} failed: {e}", name="test_result", attachment_type=AttachmentType.TEXT)
                raise

    driver.quit()
