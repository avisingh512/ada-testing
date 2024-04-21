from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from axe_selenium_python import Axe
import json

from identify_personas import categorize_personas_by_status, identify_personas, identify_personas_with_violations_and_passes

app = Flask(__name__)

# Reuse the existing functions for testing and persona identification
def run_accessibility_tests(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    driver.quit()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_website():
    url = request.form['url']
    axe_results = run_accessibility_tests(url)
    personas = identify_personas_with_violations_and_passes(axe_results)
    categorized_result = categorize_personas_by_status(personas)
    print(jsonify(categorized_result))
    return jsonify(categorized_result)

@app.route('/execute', methods=['POST'])
def execute_tests():
    url = request.form['url']
    axe_results = run_accessibility_tests(url)
    personas = identify_personas(axe_results)
    # Execute tests as per the defined function
    return jsonify({"status": "Executed", "personas": list(personas)})

if __name__ == '__main__':
    app.run(debug=True)
