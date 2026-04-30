# little script to find what user agent is displayed for playwright
import time
from playwright.sync_api import sync_playwright

def visit_site(page, context):
    print("Navigating to page...")
    page.goto("https://www.whatsmyua.info")

    print("waited for load state = networkidle") 
    page.wait_for_load_state("networkidle")
    time.sleep(120)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    visit_site(context.new_page(), context)

