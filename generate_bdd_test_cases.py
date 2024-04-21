from jinja2 import Template

template = Template("""
def test_accessibility_{{ persona }}(context):
    context['driver'].get(context['url'])
    assert context['driver'].find_element_by_tag_name('body').is_displayed() == True
""")

def generate_bdd_test_cases(personas, url):
    test_cases = []
    for persona in personas:
        test_case = template.render(persona=persona, url=url)
        test_cases.append(test_case)
    return test_cases