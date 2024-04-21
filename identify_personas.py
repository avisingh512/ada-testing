from selenium import webdriver
from axe_selenium_python import Axe

# Function to run accessibility tests using axe-core and Selenium
def run_accessibility_tests(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Initialize axe for accessibility testing
    axe = Axe(driver)
    axe.inject()  # Inject the axe-core javascript into the page
    results = axe.run()  # Run accessibility tests

    driver.quit()
    return results

# Function to identify personas based on accessibility issues
def identify_personas(axe_results):
    personas = set()
    for violation in axe_results['violations']:
        # Visual Impairments: Issues primarily affecting users with visual disabilities
        visual_issues = ['image-alt', 'object-alt', 'image-redundant-alt', 'input-image-alt', 'color-contrast']
        if any(issue in violation['id'] for issue in visual_issues):
            personas.add('Visually Impaired')

        # Auditory Impairments: Issues that affect users who are deaf or hard of hearing
        auditory_issues = ['audio-caption', 'video-caption', 'video-description']
        if any(issue in violation['id'] for issue in auditory_issues):
            personas.add('Auditory Impaired')

        # Cognitive Impairments: Issues affecting users with cognitive or neurological disabilities
        cognitive_issues = [
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
            'aria-setsize', 'aria-sort', 'aria-valuemax', 'aria-valuemin', 'aria-valuenow', 
            'aria-valuetext', 'landmark-one-main'
        ]
        if any(issue in violation['id'] for issue in cognitive_issues):
            personas.add('Cognitively Impaired')

        # Motor Impairments: Issues affecting users with limited fine motor control
        motor_issues = ['button-name', 'tabindex']
        if any(issue in violation['id'] for issue in motor_issues):
            personas.add('Motor Impaired')

        # Users who rely on screen readers or other assistive technologies
        assistive_tech_issues = ['aria-', 'role-', 'semantic-', 'status-messages']
        if any(issue in violation['id'] for issue in assistive_tech_issues):
            personas.add('Assistive Technology Users')

    return personas

def identify_personas_with_violations_and_passes(axe_results):
    persona_issues_map = {
        'Visually Impaired': [
            'color-contrast', 'image-alt', 'object-alt', 'image-redundant-alt', 'input-image-alt'
        ],
        'Auditory Impaired': [
            'audio-caption', 'video-caption', 'video-description'
        ],
        'Motor Impaired': [
            'button-name', 'tabindex', 'keyboard', 'focus-visible'
        ],
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
            'aria-setsize', 'aria-sort', 'aria-valuemax', 'aria-valuemin', 'aria-valuenow', 
            'aria-valuetext', 'landmark-one-main'
        ],
        'Assistive Technology Users': [
            'aria-', 'role-', 'semantic-', 'status-messages'
        ]
    }

    persona_results = {persona: {'violations': [], 'passes': [], 'status': 'Pass'} for persona in persona_issues_map}

    # Process violations and assign status based on presence of violations
    for violation in axe_results['violations']:
        for persona, issues in persona_issues_map.items():
            if any(issue in violation['id'] for issue in issues):
                persona_results[persona]['violations'].append(violation['description'])
                persona_results[persona]['status'] = 'Fail'  # Set status to Fail if any violations are present

    # Process passes
    for pass_ in axe_results['passes']:
        for persona, issues in persona_issues_map.items():
            if any(issue in pass_['id'] for issue in issues):
                persona_results[persona]['passes'].append(pass_['description'])
                if not persona_results[persona]['violations']:  # Only set to Pass if there are no violations
                    persona_results[persona]['status'] = 'Pass'

    return persona_results

def categorize_personas_by_status(persona_results):
    categorized_result = {
        'Passed': [],
        'Failed': []
    }

    for persona, details in persona_results.items():
        category = 'Passed' if details['status'] == 'Pass' else 'Failed'
        categorized_result[category].append({
            'Persona': persona,
            'Details': details['passes'] if details['status'] == 'Pass' else details['violations'],
            'Status': details['status']
        })

    return categorized_result

