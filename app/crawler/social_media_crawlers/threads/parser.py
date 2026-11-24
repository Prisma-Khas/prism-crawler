import re
import emoji
from playwright.sync_api import Locator


class ThreadsParser:

    def clean_text(self, text: str) -> str:

        # remove emojie
        text = emoji.replace_emoji(text, replace="")

        # remove indicator
        text = re.sub(r"\n\d+\n/\n\d+\n?", "\n", text)

        # remove button
        text = re.sub(
            r"\n?(Translate|See translation)\n?", "\n", text, flags=re.IGNORECASE
        )

        # remove br
        text = re.sub(r"\n+", "\n", text)

        # rmove spaces
        text = re.sub(r" +", " ", text)

        return text.strip()

    def parse_post(self, keyword: str, message: Locator, url:str):

        # Time
        time_locator = message.locator("time").first

        posted = None
        posted_text = None

        if time_locator.count():
            try:
                posted = time_locator.get_attribute("datetime")
                posted_text = time_locator.inner_text()
            except Exception:
                pass
        spans = message.locator("span")
        longest = ""

        for i in range(spans.count()):
            try:
                span = spans.nth(i)

                # Skip if inside <time>
                if span.locator("xpath=ancestor::time").count() > 0:
                    continue

                text = self.clean_text(span.inner_text(timeout=500))
                
                if keyword.lower() not in text.lower():
                    continue

                if len(text) > len(longest):
                    longest = text

            except Exception:
                pass

        return {"text": longest if len(longest) >= 10 else None, "url": url, "published":posted}
