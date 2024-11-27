from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
import random

# Global variable for the WebDriver instance
driver = None

def try_find_element(by, value, max_attempts=5, wait_time=5):
    """
    Retry finding a web element until it is found or the maximum number of attempts is reached.
    """
    global driver
    for attempt in range(max_attempts):
        try:
            return driver.find_element(by, value)
        except Exception as e:
            print(f"Attempt {attempt + 1} to find element {value} failed: {e}")
            if attempt < max_attempts - 1:
                time.sleep(wait_time)
    raise Exception(f"Could not find element {value} after {max_attempts} attempts.")

def open_browser():
    """
    Initialize and open the browser to the Copilot chat page.
    """
    global driver
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
    driver.get("https://m365.cloud.microsoft/chat")
    time.sleep(5)
    print("Browser opened and navigated to the Copilot chat page.")

def type_and_submit_text(text):
    """
    Type text into the chat box and submit by pressing Enter.
    """
    global driver
    iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
    driver.switch_to.frame(iframe)
    text_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="m365-chat-editor-target-element"]'))
    )
    text_box.send_keys(text)
    text_box.send_keys(Keys.ENTER)
    driver.switch_to.default_content()

def wait_for_response():
    """
    Wait until Copilot has finished generating the response.
    """
    global driver
    iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
    driver.switch_to.frame(iframe)
    stop_button_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[2]/button/span[2]'
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, stop_button_xpath)))
    WebDriverWait(driver, 300).until(EC.invisibility_of_element_located((By.XPATH, stop_button_xpath)))
    driver.switch_to.default_content()

def get_copilot_response():
    """
    Retrieve Copilot's full response.
    """
    global driver
    iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
    driver.switch_to.frame(iframe)
    response_container_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[3]'
    response_container = try_find_element(By.XPATH, response_container_xpath)
    response_text = driver.execute_script("return arguments[0].innerText;", response_container)
    driver.switch_to.default_content()
    return response_text

def create_new_chat():
    """
    Start a new conversation in Copilot.
    """
    global driver
    iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
    driver.switch_to.frame(iframe)
    new_chat_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div/button'))
    )
    new_chat_button.click()
    driver.switch_to.default_content()

def close_browser():
    """
    Close the browser instance.
    """
    global driver
    if driver:
        driver.quit()

def rate_manage_query(text, delay_range=(5, 15), max_retries=3):
    """
    Manage the rate of queries to avoid being detected or blocked.
    Retries the entire query process if any step fails.
    """
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries} for query: '{text}'")
            create_new_chat()
            type_and_submit_text(text)
            wait_for_response()
            response = get_copilot_response()

            # Check if response is valid
            if "Sorry, I wasn't able to respond to that" in response:
                raise Exception("Invalid response detected.")

            print(f"Query succeeded on attempt {attempt + 1}.")
            time.sleep(random.uniform(*delay_range))  # Random delay before next query
            return response

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print("Retrying the query after a delay...")
                time.sleep(random.uniform(*delay_range))

    print(f"All retries failed for query: '{text}'")
    return None
