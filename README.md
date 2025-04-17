# Playwright-Python Cucumber Framework

## Table of Contents
1. [Project Overview](#project-overview)
2. [Framework Structure](#framework-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Configuration](#configuration)
5. [Running Tests](#running-tests)
6. [Hooks](#hooks)
7. [Generate Report](#generate-report)
8. [CI/CD Integration](#cicd-integration)
9. [Features and Methodology](#features-and-methodology)
10. [Conclusion](#conclusion)

This repository contains a scalable test automation framework built using Playwright, Python, and Behave (BDD). 
The framework is designed for efficient and parallel execution of browser-based tests. 
It follows the Page Object Model (POM) pattern and uses Playwright for cross-browser automation. 
The framework also supports CI/CD integration, multi-environment testing, and advanced features like screenshots, 
trace logs, and video recording.

## Project Overview

The goal of this project is to provide a maintainable and scalable test automation framework for web applications. It integrates Playwright for modern browser automation and Behave for behavior-driven development (BDD).

### Key Features:
- **Playwright :** Fast, cross-browser automation (Chromium, WebKit, Firefox).
- **Behave (BDD):** Gherkin-based syntax for defining tests.
- **Page Object Model (POM):** Encapsulation of page-specific actions.
- **Base Page:** Shared methods like `select_dropdown`, and `select_radio_button`.
- **Screenshots:** Captured on every step (if enabled) and at the end of scenarios.
- **Trace Viewer:** Playwright tracing enabled per scenario for debugging.
- **Multi-Environment Support:** Multiple environments defined in `behave.ini`.
- **CI/CD Integration:** GitHub Actions pipeline for automated execution.

## Framework Structure

```plaintext
project-root/
├── features/                # Feature files (BDD scenarios)
│   ├── pages/               # Page Object files (BasePage, LoginPage, etc.)
│   ├── steps/               # Step definition files
│   ├── environment.py       # Hooks for setup and teardown
│   └── *.feature            # Feature files with scenarios
├── screenshots/             # Screenshots captured during tests
├── traces/                  # Playwright trace sessions (zip files)
├── behave.ini               # Configurations for different environments
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```
```

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SowmyaMoturu/playwright_python_behave.git
   cd playwright-python-framework
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   python -m playwright install  # Install Playwright browsers
   ```

## Configuration

- **behave.ini:** This file defines environment configurations such as base URLs, API URLs, and browser types for different environments (e.g., `sit`, `uat`). Update it with your environment-specific details.

Example `behave.ini`:

```ini
[behave:sit]
baseUrl = https://sit.example.com
apiUrl = https://api.sit.example.com
browserType = chrome

[behave:uat]
baseUrl = https://uat.example.com
apiUrl = https://api.uat.example.com
browserType = webkit
```

- **Environment Profiles:** Set the environment at runtime by passing the profile flag:
  ```bash
  behave -D profile=uat
  ```

## Running Tests

### **Run All Tests:**
```bash
behave
```

### **Run Tests for Specific Profile:**
```bash
behave -D profile=uat
```

### **Run Debug Tests:**
To run tests in debug mode, use the `--no-capture` option to view the output in real-time:
```bash
behave --no-capture
```

### **Run a Specific Feature File:**
To run tests from a specific feature file, provide the path to the file:
```bash
behave features/login.feature
```

### **Run Tests with Specific Tags:**
```bash
behave --tags @smoke
```

### **Run Tests for a Specific Scenario:**
```bash
behave --name "New User Registration"
```
### **Run Tests with Video Recording:**

To enable video recording for your tests, ensure the `record_video` option is set in your configuration

```bash
behave -D record_video=true
```

The recorded videos will be saved in the `videos/` directory for each scenario. These videos can be used for debugging and reviewing test execution.

### **Capture Screenshot on Every Step:**
To enable screenshots on every step, pass the `screenshot_on_step` option during test execution:

```bash
behave -D screenshot_on_step=true
```

The screenshots will be saved in the `screenshots/` directory for each step. These can be used for debugging and reporting purposes.

## Hooks

The framework includes hooks for enabling advanced debugging features like tracing, screenshots, and video recording. These hooks are defined in the `environment.py` file and are triggered during test execution. Tracing captures detailed logs for each scenario, while screenshots and video recordings provide visual evidence of test steps and failures. These artifacts are stored in their respective directories (`traces/`, `screenshots/`, `videos/`) and can be used for debugging and reporting purposes.

## **Generate Report:**

### **Steps to Generate Allure Report:**

1. Run your tests with the Allure formatter:
```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure
```

2. **Serve the Allure report:**

   ```bash
   allure serve reports/allure
   ```

```bash
allure serve reports/allure
```

## CI/CD Integration

The repository includes a sample GitHub Actions workflow to automate test execution. Key steps include:

- **Triggering Tests:** Automatically triggered on a push to the `main` branch.
- **Environment Setup:** Installs dependencies and Playwright browsers.
- **Test Execution:** Runs specific test suites like smoke or regression tests.
- **Parallel Jobs:** Supports running multiple test jobs concurrently.

Refer to the `.github/workflows/ci.yml` file for the complete configuration.

## Features and Methodology

### Trace Logs and Videos:
- **Trace Logs:** Each scenario generates trace logs, which are stored in the `traces/` folder. These logs are in a zip file format, and you can open them in the [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) for detailed step-by-step debugging.
  
- **Video Recording:** Videos of test execution are recorded and stored in the `videos/` folder. The video captures the entire browser session for each scenario, useful for debugging failures.

### Screenshots:
- Screenshots are captured on every step (if enabled) and when a scenario finishes. The screenshots are saved in the `screenshots/` directory, and you can attach them to test reports (e.g., Allure or HTML reports).

## Conclusion

This framework provides a modern, scalable, and maintainable way to automate browser testing using Playwright, Python, and Behave. It supports parallel test execution, CI/CD integration, and advanced debugging features like tracing, screenshots, and video recording. With multi-environment support, it’s designed to fit seamlessly into modern test automation workflows.