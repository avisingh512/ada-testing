from selenium import webdriver
from behave import runner, configuration
from behave import given, then

def execute_test_cases(test_cases, url):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ssl-protocol=TLSv1.2")
    driver = webdriver.Chrome(options=options)
    context = {}
    context['driver'] = driver
    context['url'] = url

    custom_config = configuration.Configuration()
    custom_config.feature_dirs = []  # Set feature directories to an empty list
    behave_runner = runner.Runner(config=custom_config)
    behave_runner.feature_locations = []  # Set feature locations to an empty list

    behave_runner.context = context
    for test_case in test_cases:
        compiled_test_case = compile(test_case, '<string>', 'exec')
        eval(compiled_test_case, globals(), locals())
    behave_runner.run()
    driver.quit()