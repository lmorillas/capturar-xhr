#  https://www.rkengler.com/how-to-capture-network-traffic-when-scraping-with-selenium-and-python/

from time import sleep

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import json

# make chrome log requests
capabilities = DesiredCapabilities.CHROME.copy()
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
capabilities['goog:chromeOptions'] = {
                'perfLoggingPrefs': {
                    'traceCategories': 'v8,blink.console,disabled-by-default-devtools.timeline'
                }}


driver = webdriver.Chrome(
    desired_capabilities=capabilities #, executable_path="./chromedriver"
)

# fetch a site that does xhr requests
url = 'https://datacovid.salud.aragon.es/covid/'
driver.get(url)

sleep(5) 

casos = driver.find_element_by_link_text('Casos')
casos.click()

sleep(5) 

logs_raw = driver.get_log("performance")

logs = [json.loads(lr["message"])["message"] for lr in logs_raw if 'xhr' in lr['message']]

json.dump(logs, open('logs.json', 'w'))

print(json.dumps(logs, indent=True))