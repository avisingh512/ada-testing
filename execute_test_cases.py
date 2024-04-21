from selenium import webdriver
from axe_selenium_python import Axe

def execute_test_cases(personas, url):
    # Setup WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode for automation
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Initialize Axe for accessibility testing
    axe = Axe(driver)
    axe.inject()

    results = axe.run()  # Run accessibility tests once and use the results for all personas

    for persona in personas:
        print(f"\nExecuting test for {persona} on {url}")
        persona_issues_found = False

        # Define a comprehensive list of issue IDs for each persona
        issues = {
            'Visually Impaired': ['color-contrast', 'image-alt', 'object-alt', 'image-redundant-alt', 'input-image-alt'],
            'Auditory Impaired': ['audio-caption', 'video-caption', 'video-description'],
            'Motor Impaired': ['button-name', 'tabindex', 'keyboard', 'focus-visible'],
            'Cognitively Impaired': [
                'aria-', 'label', 'definition-list', 'link-in-text-block', 'document-title', 
                'duplicate-id-active', 'frame-title', 'html-has-lang', 'html-lang-valid', 
                'html-xml-lang-mismatch', 'layout-table', 'list', 'listitem', 'marquee', 
                'meta-refresh', 'meta-viewport', 'radiogroup', 'region', 'scope-attr-valid', 
                'scrollable-region-focusable', 'select-name', 'server-side-image-map', 
                'tabindex', 'td-has-header', 'th-has-data-cells', 'valid-lang', 'label-content-name-mismatch', 
                'label-title-only', 'aria-allowed-attr', 'aria-required-attr', 'aria-required-children', 
                'aria-required-parent', 'aria-roles', 'aria-valid-attr-value', 'aria-valid-attr', 
                'aria-allowed-role', 'aria-hidden-body', 'aria-hidden-focus', 'aria-input-field-name', 
                'aria-toggle-field-name', 'aria-progressbar-name', 'aria-meter-name', 'aria-radiogroup', 
                'aria-range', 'aria-roledescription', 'aria-activedescendant', 'aria-autocomplete', 
                'aria-checked', 'aria-disabled', 'aria-expanded', 'aria-haspopup', 'aria-level', 
                'aria-modal', 'aria-multiline', 'aria-multiselectable', 'aria-orientation', 
                'aria-placeholder', 'aria-posinset', 'aria-readonly', 'aria-required', 'aria-selected', 
                'aria-setsize', 'aria-sort', 'aria-valuemax', 'aria-valuemin', 'aria-valuenow', 'aria-valuetext', 
                'landmark-one-main'
            ],
            'Assistive Technology Users': ['aria-', 'role-', 'semantic-', 'status-messages']
        }

        # Check for relevant violations
        for violation in results['violations']:
            if any(issue in violation['id'] for issue in issues[persona]):
                persona_issues_found = True
                print(f"Failure for {persona}: {violation['id']} - {violation['description']}")
                # Also include specific failure details, if available
                for node in violation['nodes']:
                    print(f"  Element affected: {node['html']}")
                    print(f"  Failure reason: {node['failureSummary']}")

        # Print results based on the presence of violations
        if persona_issues_found:
            print(f"Test for {persona} failed.")
        else:
            print(f"Test for {persona} passed.")

    driver.quit()
