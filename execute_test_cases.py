from selenium import webdriver

def execute_test_cases(test_cases, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ssl-protocol=TLSv1.2")
    driver = webdriver.Chrome(options=options)
    context = {'driver': driver, 'url': url}

    for test_case in test_cases:
        try:
            exec(test_case, context)
            print(f"Test case '{test_case.split()[1]}' passed.")
        except AssertionError as e:
            print(f"Test case '{test_case.split()[1]}' failed: {e}")
        except Exception as e:
            print(f"Test case '{test_case.split()[1]}' failed with an unexpected error: {e}")

    driver.quit()