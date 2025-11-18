"""
Behave environment configuration with hooks for test setup and teardown
"""
import os
import logging
from datetime import datetime
from playwright.sync_api import sync_playwright
from utility.common.logger import Logger
from utility.common.config_reader import ConfigReader
from utility.common.screenshot_helper import ScreenshotHelper

def before_all(context):
    """Setup before all tests"""
    # Initialize logger
    context.logger = Logger().get_logger()
    context.logger.info("Starting test execution")
    
    # Load configuration
    context.config = ConfigReader()
    context.env = context.config.get_environment()
    
    # Initialize screenshot helper
    context.screenshot_helper = ScreenshotHelper()
    
    # Setup Playwright
    context.playwright = sync_playwright().start()
    
    # Browser configuration
    browser_name = context.config.get_browser()
    headless = context.config.get_headless_mode()
    
    if browser_name.lower() == 'chrome':
        context.browser = context.playwright.chromium.launch(headless=headless)
    elif browser_name.lower() == 'firefox':
        context.browser = context.playwright.firefox.launch(headless=headless)
    elif browser_name.lower() == 'safari':
        context.browser = context.playwright.webkit.launch(headless=headless)
    else:
        context.browser = context.playwright.chromium.launch(headless=headless)
    
    context.logger.info(f"Browser {browser_name} initialized in {'headless' if headless else 'headed'} mode")

def after_all(context):
    """Cleanup after all tests"""
    if hasattr(context, 'browser'):
        context.browser.close()
    if hasattr(context, 'playwright'):
        context.playwright.stop()
    context.logger.info("Test execution completed")

def before_scenario(context, scenario):
    """Setup before each scenario"""
    context.logger.info(f"Starting scenario: {scenario.name}")
    
    # Create new page for each scenario
    if hasattr(context, 'browser'):
        context.page = context.browser.new_page()
        context.page.set_viewport_size({"width": 1920, "height": 1080})

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    # Take screenshot on failure
    if scenario.status == "failed" and hasattr(context, 'page'):
        screenshot_path = context.screenshot_helper.take_screenshot(
            context.page, 
            f"failed_{scenario.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        context.logger.error(f"Scenario failed. Screenshot saved: {screenshot_path}")
    
    # Close page
    if hasattr(context, 'page'):
        context.page.close()
    
    context.logger.info(f"Completed scenario: {scenario.name} - Status: {scenario.status}")

def before_step(context, step):
    """Setup before each step"""
    context.logger.debug(f"Executing step: {step.name}")

def after_step(context, step):
    """Cleanup after each step"""
    if step.status == "failed":
        context.logger.error(f"Step failed: {step.name}")