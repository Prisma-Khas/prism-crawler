from playwright.sync_api import sync_playwright
import threading
import asyncio

class Browser:

    def __init__(self, headless=True):
        self.headless = headless

    def launch(self):
        print("Thread:", threading.current_thread().name)

        try:
            loop = asyncio.get_running_loop()
            print("Running loop:", loop)
        except RuntimeError:
            print("No running event loop")

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            user_data_dir="threads_profile",
            headless=self.headless,
            viewport={"width": 1400, "height": 900},
        )

        return playwright, context