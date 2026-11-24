from urllib.parse import quote

from app.crawler.browser_twitter import Browser
from app.crawler.social_media_crawlers.twitter.parser import TwitterParser
from app.crawler.social_media_crawlers.twitter.scroll import TwitterScroller


class TwitterCrawler:

    POST_SELECTOR = "article"

    def __init__(self):
        self.browser = Browser(headless=True)
        self.parser = TwitterParser()
        self.scroller = TwitterScroller()
        
    def ensure_login(self, page):

        page.goto("https://x.com/home")

        # Already logged in
        if "login" not in page.url and "flow" not in page.url:
            print("Already logged in.")
            return

        print("Please log in to X in the opened browser.")
        input("Press ENTER after login...")

        page.reload()

        if "login" in page.url or "flow" in page.url:
            raise Exception("Login failed.")

        print("Login successful.")

    def crawl_search(
        self,
        url: str,
        keyword,
        state_id: int,
        parlimen_id: int,
        keyword_type: int,
        max_scrolls: int,
        dun_id: int | None = None,
    ):

        playwright, context = self.browser.launch()
        page = context.new_page()

        self.ensure_login(page)

        processed = set()
        posts = []
        results = []

        try:

            page.goto(url)

            print(page.title())

            for scroll in range(max_scrolls):

                print(f"\ntw=== Scroll {scroll + 1} ===")

                messages = page.locator(self.POST_SELECTOR)

                count = messages.count()

                print(f"tw Visible results: {count}")

                for i in range(count):

                    try:

                        message = messages.nth(i)

                        post = self.parser.parse_post(
                            keyword,
                            message,
                            url,
                        )

                        if not post:
                            continue

                        post_text = post["text"]

                        if not post_text:
                            continue

                        if post_text in processed:
                            continue

                        processed.add(post_text)
                        posts.append(post)

                        print("-" * 60)
                        print(post_text)

                    except Exception as e:
                        print(e)

                print("Scrolling tw...")

                self.scroller.scroll(page, max_scrolls=1)

                page.wait_for_timeout(2000)

            for post in posts:

                results.append(
                    {
                        "state_id": state_id,
                        "parlimen_id": parlimen_id,
                        "dun_id": dun_id,
                        "crawl_type": 1,
                        "keyword_type": keyword_type,
                        "source": "Twitter",
                        "keyword": keyword,
                        "title": "-",
                        "url": post["url"],
                        "published": post["published"],
                        "body": post["text"],
                    }
                )

            return results

        finally:

            context.close()
            playwright.stop()