import os
import logging
from configparser import ConfigParser
from playwright.sync_api import sync_playwright
import allure


def is_local():
    """Determine if the environment is local or CI."""
    return os.getenv("CI", "false").lower() != "true"

def setup_directories(context):
    """Set up required directories based on flags."""
    context.screenshot_dir = "screenshots"
    os.makedirs(context.screenshot_dir, exist_ok=True)

    if context.config.userdata.get("record_video", "false").lower() == "true":
        context.video_dir = "videos"
        os.makedirs(context.video_dir, exist_ok=True)

    context.trace_dir = "traces"
    os.makedirs(context.trace_dir, exist_ok=True)

def get_screenshot_path(scenario_name, step_name=None):
    """Generate a file path for storing screenshots."""
    base_dir = "screenshots"
    os.makedirs(base_dir, exist_ok=True)

    name = scenario_name.replace(" ", "_").replace("/", "_")
    if step_name:
        step = step_name.replace(" ", "_").replace("/", "_")
        filename = f"{name}__{step}.png"
    else:
        filename = f"{name}__final.png"

    return os.path.join(base_dir, filename)

def attach_screenshot_to_allure(path, name):
    """Attach a screenshot to the Allure report."""
    try:
        allure.attach.file(
            path,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
        logging.info(f"Screenshot attached: {name}")
    except Exception as e:
        logging.error(f"Could not attach screenshot: {e}")

def load_config(context):
    """Load settings from behave.ini."""
    config = ConfigParser()
    config.read("behave.ini")

    profile = f"behave:{context.config.userdata.get('profile', 'sit')}"
    if profile not in config:
        raise ValueError(f"Profile '{profile}' not found in behave.ini")

    section = config[profile]
    context.base_url = section.get("baseUrl")
    context.api_url = section.get("apiUrl")
    context.browser_type = section.get("browserType", "chrome").lower()

    context.headless = not is_local()
    context.screenshot_on_step = context.config.userdata.get("screenshot_on_step", "false").lower() == "true"


def before_all(context):
    """Runs before all tests."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("test_log.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("Starting test suite")

    load_config(context)
    setup_directories(context)

    context.playwright = sync_playwright().start()
    browser_type = context.browser_type
    launch_args = {"headless": context.headless}

    if browser_type == "webkit":
        context.browser = context.playwright.webkit.launch(**launch_args)
    elif browser_type == "msedge":
        context.browser = context.playwright.chromium.launch(channel="msedge", **launch_args)
    elif browser_type == "chrome":
        context.browser = context.playwright.chromium.launch(channel="chrome", **launch_args)
    else:
        context.browser = context.playwright.chromium.launch(**launch_args)


def before_scenario(context, scenario):
    """Runs before each scenario."""
    context.scenario = scenario
    logging.info(f"Starting scenario: {scenario.name}")

    context.context = context.browser.new_context(
        accept_downloads=True,
        viewport={"width": 1280, "height": 800},
        ignore_https_errors=True,
        base_url=context.base_url,
        record_video_dir="videos" if context.config.userdata.get("record_video", "false").lower() == "true" else None
    )
    context.page = context.context.new_page()
    context.context.tracing.start(screenshots=True, snapshots=True)


def after_step(context, step):
    """Runs after each step."""
    if context.screenshot_on_step:
        path = get_screenshot_path(context.scenario.name, step.name)
        context.page.screenshot(path=path)
        logging.info(f"Screenshot saved for step: {step.name}")

        # Attach screenshot to Allure report
        attach_screenshot_to_allure(path, f"Screenshot for step: {step.name}")


def after_scenario(context, scenario):
    """Runs after each scenario."""
    try:
        # Final screenshot
        path = get_screenshot_path(scenario.name)
        context.page.screenshot(path=path)
        logging.info(f"Final screenshot saved for scenario: {scenario.name}")

        # Attach final screenshot to Allure report
        attach_screenshot_to_allure(path, f"Final screenshot for scenario: {scenario.name}")

        # Trace
        if context.config.userdata.get("record_video", "false").lower() == "true":
            video_path = context.page.video.path()
            final_video_path = os.path.join(context.video_dir, f"{scenario.name.replace(' ', '_')}.mp4")
            os.rename(video_path, final_video_path)
            logging.info(f"Video saved at: {final_video_path}")
       
        trace_path = f"traces/{scenario.name.replace(' ', '_')}.zip"
        context.context.tracing.stop(path=trace_path)
        logging.info(f"Trace saved at: {trace_path}")

    except Exception as e:
        logging.error(f"Error during after_scenario: {e}")

    finally:
        if context.page:
            context.page.close()
        if context.context:
            context.context.close()


def after_all(context):
    """Runs after all tests."""
    if context.browser:
        context.browser.close()
    if context.playwright:
        context.playwright.stop()
    logging.info("Test suite completed. Playwright shutdown completed.")