from playwright.sync_api import Locator


class FacebookParser:

    def parse_post(self, message):

        text = message.locator("div[dir='auto']")

        for i in range(text.count()):
            print(text.nth(i).inner_text())