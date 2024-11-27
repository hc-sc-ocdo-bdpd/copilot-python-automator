# Copilot Automation Tool

This project automates interactions with Microsoft Copilot using Selenium. It allows users to query Copilot with a list of questions and retrieve responses, which are then stored in a CSV file.

## Features

- Opens the Microsoft Copilot chat page in an Edge browser.
- Automates text input into the chat interface.
- Retrieves and stores Copilot's responses.
- Includes rate management to avoid triggering detection.
- Handles retries for queries that fail due to invalid responses.

## Contents

- **`copilot_automation.py`**: Core automation script with functions to interact with Copilot.
- **`usage.ipynb`**: Jupyter Notebook demonstrating how to use the automation script with a CSV file of questions.
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

### Running the Automation

1. Prepare a CSV file (`questions_for_copilot.csv`) with the following format:
   ```csv
   question
   What is AI?
   Explain machine learning.
   ```

2. Run the automation script via the Jupyter Notebook (`usage.ipynb`) or adapt it to your script.

3. Example workflow:
   - Open the browser with `copilot.open_browser()`.
   - Query Copilot using `copilot.rate_manage_query()`.
   - Save responses to the CSV.

4. Responses will be saved in the CSV file, either updating the original or saving to a new file.

### Notes

- **Rate Limits**: After approximately 40 queries, Copilot may repeatedly respond with "Sorry, I wasn't able to respond to that." This could be due to detection mechanisms, organizational settings, or account limitations.
- **Retries**: The script includes retry mechanisms to handle failures in sending or receiving queries.
- **Delay Management**: Adds random delays between queries to reduce the risk of detection.
