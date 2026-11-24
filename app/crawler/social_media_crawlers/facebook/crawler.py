from aapp.crawler.browser import Browser
from app.crawler.social_media_crawlers.facebook.parser import FacebookParser
from app.crawler.social_media_crawlers.facebook.scroll import FacebookScroller


class FacebookCrawler:

    POST_SELECTOR = (
        'div[data-ad-preview="message"][data-ad-comet-preview="message"]'
    )

    def __init__(self):
        self.browser = Browser(headless=True)
        self.parser = FacebookParser()
        self.scroller = FacebookScroller()

    def get_post_key(self, message):
        """
        Try to use the permalink as the unique key.
        If unavailable, fall back to the first 100 chars of text.
        """

        try:
            links = message.locator("a")

            for i in range(links.count()):

                href = links.nth(i).get_attribute("href", timeout=500)

                if not href:
                    continue

                if (
                    "/posts/" in href
                    or "/permalink/" in href
                    or "story.php" in href
                ):

                    if href.startswith("/"):
                        href = "https://www.facebook.com" + href

                        return href

        except:
            pass

        try:
            preview = message.text_content(timeout=1000)

            if preview:
                return preview[:100]

        except:
            pass

        return None

    def expand_post(self, page, message):

        try:

            see_more = message.locator("text=See more")

            if see_more.count():

                see_more.first.scroll_into_view_if_needed()

                see_more.first.click(
                    force=True,
                    timeout=1000
                )

                page.wait_for_timeout(500)

        except:
            pass

    def crawl(self, url, max_scrolls=5):

        playwright, context = self.browser.launch()
        page = context.new_page()

        processed = set()
        results = []

        try:

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            page.wait_for_timeout(5000)

            print(page.title())

            for scroll in range(max_scrolls):

                print(f"\n=== Scroll {scroll + 1} ===")

                page.wait_for_timeout(1000)

                index = 0

                while True:

                    messages = page.locator(self.POST_SELECTOR)

                    count = messages.count()

                    if index >= count:
                        break

                    try:

                        message = messages.nth(index)

                        key = self.get_post_key(message)

                        if not key:
                            index += 1
                            continue

                        if key in processed:
                            index += 1
                            continue

                        processed.add(key)

                        self.expand_post(page, message)

                        # Re-acquire locator after clicking
                        messages = page.locator(self.POST_SELECTOR)

                        if index >= messages.count():
                            break

                        message = messages.nth(index)
                        print(f"POST {index}")
                        text = self.parser.parse_post(message)

                        if text:

                            results.append({
                                "url": key if key.startswith("http") else None,
                                "text": text
                            })

                    except Exception as e:

                        print(e)

                    index += 1

                print("Scrolling...")

                self.scroller.scroll(page, max_scrolls=1)

                page.wait_for_timeout(2000)

            return results

        finally:

            context.close()
            playwright.stop()


if __name__ == "__main__":

    crawler = FacebookCrawler()

    posts = crawler.crawl(
        "https://www.facebook.com/BernamaOfficial",
        max_scrolls=5
    )

    for i, text in enumerate(posts, start=1):
        print("=" * 80)
        print(f"POST {i}")
        print("=" * 80)
        print(text)
        print()