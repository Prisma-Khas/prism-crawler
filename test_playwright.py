from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    context = p.chromium.launch_persistent_context(
        user_data_dir="./facebook_profile",
        channel="chrome",          # Use installed Google Chrome
        headless=True
    )

    page = context.pages[0] if context.pages else context.new_page()

    page.goto("https://www.facebook.com")

    input("Login manually, then press Enter...")

    context.close()