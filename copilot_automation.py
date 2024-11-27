from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

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
    try:
        iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
        driver.switch_to.frame(iframe)
        print("Switched to iframe.")

        text_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="m365-chat-editor-target-element"]'))
        )
        print("Text box found.")
        text_box.send_keys(text)
        print(f'Text "{text}" typed into the text box.')
        text_box.send_keys(Keys.ENTER)
        print("Text submitted (Enter key pressed).")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"An error occurred while typing and submitting text: {e}")

def wait_for_response():
    """
    Wait until Copilot has finished generating the response.
    """
    global driver
    try:
        iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
        driver.switch_to.frame(iframe)
        print("Switched to iframe for waiting for response.")

        stop_button_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[3]/div/div[1]/div[2]/div/div[2]/div[2]/button/span[2]'

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, stop_button_xpath))
        )
        print("Stop generation button is present. Waiting for response to finish.")

        WebDriverWait(driver, 300).until(
            EC.invisibility_of_element_located((By.XPATH, stop_button_xpath))
        )
        print("Response generation finished.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"An error occurred while waiting for the response: {e}")

def get_copilot_response():
    """
    Retrieve Copilot's full response.
    """
    global driver
    try:
        iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
        driver.switch_to.frame(iframe)
        print("Switched to iframe for response retrieval.")

        response_container_xpath = '/html/body/div[1]/div/div/div/div/div/div/div[1]/div[1]/div[3]'
        response_container = try_find_element(By.XPATH, response_container_xpath)
        response_text = driver.execute_script("return arguments[0].innerText;", response_container)
        print(f"Copilot's full response:\n{response_text}")
        driver.switch_to.default_content()
        return response_text
    except Exception as e:
        print(f"An error occurred while retrieving Copilot's response: {e}")
        return None

def create_new_chat():
    """
    Start a new conversation in Copilot.
    """
    global driver
    try:
        iframe = try_find_element(By.XPATH, '//*[@id="iframe:d870f6cd-4aa5-4d42-9626-ab690c041429"]')
        driver.switch_to.frame(iframe)
        print("Switched to iframe for New Chat button.")

        new_chat_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div/button'))
        )
        new_chat_button.click()
        print("New Chat button clicked.")
        driver.switch_to.default_content()
    except Exception as e:
        print(f"An error occurred while clicking the New Chat button: {e}")

def close_browser():
    """
    Close the browser instance.
    """
    global driver
    if driver:
        driver.quit()
        print("Browser closed.")
