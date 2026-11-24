from playwright.sync_api import sync_playwright


class Browser:

    def __init__(self, headless=False):
        self.headless = headless

    def launch(self):

        playwright = sync_playwright().start()

        context = playwright.chromium.launch_persistent_context(
            user_data_dir="twitter_profile",
            headless=self.headless,
            viewport={"width": 1400, "height": 900},
        )

        return playwright, context