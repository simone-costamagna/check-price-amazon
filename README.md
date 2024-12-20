# Check Price Amazon

This Python project automates price tracking for specified products on Amazon. When a product's price falls below a predefined threshold, it sends an email notification to a configured address. Additionally, a GitHub Actions workflow is included to schedule and automate script execution.

## Features
- **Automated Price Tracking**: Fetches product prices directly from Amazon using Selenium.
- **Email Notifications**: Sends email alerts when a product's price is below the set threshold.
- **Modular Design**: Clean and maintainable code organized into separate modules.
- **Easy Configuration**: Specify product links and price thresholds in a configuration file.
- **Logging**: Provides detailed logs for debugging and tracking operations.
- **GitHub Actions Integration**: Automate script execution at regular intervals.

---

## Prerequisites

### 1. Python Dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Define the following environment variables:
- `EMAIL_ADDRESS`: The email address used to send notifications.
- `GMAIL_TOKEN`: A token or password for the email account.

Use a `.env` file or export these variables manually:
```bash
export EMAIL_ADDRESS="your_email@gmail.com"
export GMAIL_TOKEN="your_email_account_token"
```

---

## Configuration
The products to track are defined in `config.py`. Each entry in the `PRODUCTS` dictionary specifies:
- **Key**: Product URL on Amazon.
- **Value**: Price threshold.

Example:
```python
PRODUCTS = {
    "https://www.amazon.it/example-product": 80.00,
    "https://www.amazon.it/another-product": 25.00,
}
```

---

## Running the Project

### Locally
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python main.py
   ```

### Using GitHub Actions
The project includes a `actions.yml` file to automate the execution of the script using GitHub Actions. This workflow allows you to run the script on a schedule without manual intervention.

1. Ensure you have the following repository secrets configured:
   - `EMAIL_ADDRESS`: The email address used for notifications.
   - `GMAIL_TOKEN`: A token for the email account.

2. Modify the `schedule` block in the `actions.yml` file to adjust the frequency of execution. For example:
   ```yaml
   schedule:
     - cron: '0 22 * * 0'  # Runs every Sunday at 22:00 UTC
   ```

3. Commit and push the workflow file. GitHub Actions will execute the workflow according to the defined schedule.

---

## Project Structure
- **`main.py`**: Entry point for the project, coordinating tasks such as price checking and email notifications.
- **`config.py`**: Configuration file containing product links and price thresholds.
- **`logging_config.py`**: Handles logging setup and configuration.
- **`webdriver_manager.py`**: Manages WebDriver initialization and cleanup.
- **`price_checker.py`**: Contains logic for retrieving and validating product prices.
- **`email_handler.py`**: Manages email notifications for price alerts.
- **`.github/workflows/actions.yml`**: GitHub Actions workflow file for scheduling script execution.
- **`.env`**: File for storing environment variables (not included in the repository; add it locally).
- **`requirements.txt`**: Python packages required.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.
