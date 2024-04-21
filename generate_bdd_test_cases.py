from behave import given, when, then

def generate_bdd_test_cases(personas, url):
    test_cases = []
    for persona in personas:
        test_case = f"""
@given('the website is accessible for {persona} users')
def test_accessibility_{persona}(context):
    pass
@when('I navigate to the website')
def navigate_to_website(context):
    context.driver.get('{url}')
@then('the website is accessible for {persona} users')
def check_accessibility_{persona}(context):
    assert context.driver.find_element_by_tag_name('body').is_displayed() == True
"""
        test_cases.append(test_case)
    return test_cases