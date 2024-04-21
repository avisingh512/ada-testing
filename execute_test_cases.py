from selenium import webdriver
from behave import given, then
from behave.runner import Runner
from behave.configuration import Configuration

def execute_test_cases(test_cases, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ssl-protocol=TLSv1.2")
    driver = webdriver.Chrome(options=options)
    context = {}
    context['driver'] = driver
    context['url'] = url

    custom_config = Configuration()
    custom_config.feature_dirs = [] 
    behave_runner = Runner(config=custom_config)
    behave_runner.feature_locations = [] 

    behave_runner.context = context
    for test_case in test_cases:
        compiled_test_case = compile(test_case, '<string>', 'exec')
        try:
            exec(compiled_test_case, globals(), locals())
            print(f"Test case '{test_case.split()[1]}' passed.")
        except AssertionError as e:
            print(f"Test case '{test_case.split()[1]}' failed: {e}")
        except Exception as e:
            print(f"Test case '{test_case.split()[1]}' failed with an unexpected error: {e}")

    driver.quit()