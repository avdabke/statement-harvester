import os
from playwright.sync_api import sync_playwright

AUTH_FILE = "fidium_auth.json"
DOWNLOAD_DIR = "./bills"

def login_and_save_session(page, context):
    print("Navigating to login page...")
    page.goto("https://auth.fidium.net")

    # --- Fill in credentials ---
    page.locator('input[type="email"], input[name="username"], #username').fill(FIDIUM_USERNAME)
    page.locator('input[type="password"], #password').fill(FIDIUM_PASSWORD)
    page.get_by_role("button", name="Continue").click()
    # page.locator('button[type="submit"], input[name="action"], input[type="submit"]').click()

    # --- Handle 2FA if prompted ---
    try:
        otp_input = page.locator('input[name="otp"], input[name="code"], #2fa-input')
        otp_input.wait_for(timeout=5000)
        code = input("Enter your 2FA code: ")
        otp_input.fill(code)
        page.locator('button[type="submit"]').click()
    except:
        print("No 2FA prompt detected, continuing...")

    # Wait for dashboard to load
    print("waited for load state = networkidle") 
    #page.wait_for_load_state("networkidle")

    # Save session so future runs skip login
    context.storage_state(path=AUTH_FILE)
    print("Session saved!")

def download_bill(page):
    print("Looking for statement...")

    #import code
    #code.interact(local=locals())

    # Navigate to billing page — adjust URL if needed
    # page.goto("https://auth.fidium.net/billing")  # or /account/billing, /invoices, etc.
    page.locator(':has-text("View Statement")')
    page.wait_for_load_state("networkidle")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    # Wait for a download to be triggered
    with page.expect_download() as download_info:
        # Click the most recent bill download link — adjust selector as needed
        # page.locator('a[href*=".pdf"], button:has-text("Download"), a:has-text("Download Bill")').first.click()
        page.locator('a:has-text("View Statement")').first.click()

    download = download_info.value
    save_path = os.path.join(DOWNLOAD_DIR, download.suggested_filename)
    download.save_as(save_path)
    print(f"Bill downloaded to: {save_path}")

# avd changes to run playwright in python interactive REPL
# instead of running it in a context, instantiate an object

p = sync_playwright().start()

# with sync_playwright() as p:
# Use saved session if available, otherwise do full login
if os.path.exists(AUTH_FILE):
    print("Using saved session...")
    context = p.chromium.launch_persistent_context(
        "",
        headless=False,
        storage_state=AUTH_FILE
    )
else:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    login_and_save_session(context.new_page(), context)

page = context.new_page()
#download_bill(page)
#context.close()
