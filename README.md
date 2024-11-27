# Copilot Automation Tool

This project automates interactions with Microsoft Copilot using Selenium. It allows users to query Copilot and retrieve responses through a simple programmatic interface.

## Features

- Opens the Microsoft Copilot chat page in an Edge browser.
- Automates text input into the chat interface.
- Retrieves Copilot's response after processing.

## Contents

- **`copilot_automation.py`**: Core automation script with functions to interact with Copilot.
- **`usage.ipynb`**: Jupyter Notebook demonstrating usage examples.
- **`questions_for_copilot.csv`**: Sample file containing 50 test questions (one column: `question`).
- **`requirements.txt`**: File listing the required Python dependencies.

## Usage

### Prerequisites

1. Install Python 3.10+.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure Microsoft Edge browser and its WebDriver are installed.

### Basic Workflow

The tool allows you to send a single question to Copilot and retrieve the response. Below is a simple flow:

1. Open the browser and navigate to the Copilot chat page:
   ```python
   copilot.open_browser()
   ```

2. Start a new chat:
   ```python
   copilot.create_new_chat()
   ```

3. Type your question and submit it:
   ```python
   copilot.type_and_submit_text("What is artificial intelligence?")
   ```

4. Wait for Copilot to process the response and retrieve it:
   ```python
   copilot.wait_for_response()
   response = copilot.get_copilot_response()
   print(response)
   ```

5. Close the browser:
   ```python
   copilot.close_browser()
   ```

### Notes

- **Rate Limits**: After approximately 40 queries, Copilot may repeatedly respond with "Sorry, I wasn't able to respond to that." This could be due to detection mechanisms, organizational settings, or account limitations.
- **Retries**: The script includes retry mechanisms for handling failed queries.
