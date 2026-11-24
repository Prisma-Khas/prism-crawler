from playwright.sync_api import sync_playwright
import threading
import asyncio

class BrowserNews:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        print("Thread:", threading.current_thread().name)

        try:
            loop = asyncio.get_running_loop()
            print("Running loop:", loop)
        except RuntimeError:
            print("No running event loop")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=self.headless
        )
        self.page = self.browser.new_page()
        return self.page

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()