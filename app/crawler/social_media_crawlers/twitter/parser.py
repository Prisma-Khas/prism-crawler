import re
import emoji
from playwright.sync_api import Locator


class TwitterParser:

    def clean_text(self, text: str) -> str:

        # Remove emojis
        text = emoji.replace_emoji(text, replace="")

        # Remove extra blank lines
        text = re.sub(r"\n+", "\n", text)

        # Remove multiple spaces
        text = re.sub(r" +", " ", text)

        return text.strip()

    def parse_post(self, keyword: str, message: Locator, search_url: str):

        # Published time
        posted = None

        try:
            posted = message.locator("time").first.get_attribute("datetime")
        except Exception:
            pass

        # Tweet URL
        url = search_url

        try:
            href = (
                message.locator("time")
                .locator("xpath=ancestor::a")
                .first
                .get_attribute("href")
            )

            if href:
                url = f"https://x.com{href}"

        except Exception:
            pass

        # Tweet text
        longest = ""

        try:

            text = message.locator(
                '[data-testid="tweetText"]'
            ).inner_text(timeout=500)

            text = self.clean_text(text)

            if keyword.lower() in text.lower():
                longest = text

        except Exception:
            pass

        return {
            "text": longest if len(longest) >= 10 else None,
            "url": url,
            "published": posted,
        }