from app.crawler.browser_threads import Browser
from app.crawler.social_media_crawlers.threads.parser import ThreadsParser
from app.crawler.social_media_crawlers.threads.scroll import ThreadsScroller


class ThreadsCrawler:

    POST_SELECTOR = 'div[data-pagelet^="threads_search_results_"]'

    def __init__(self):
        self.browser = Browser(headless=True)
        self.parser = ThreadsParser()
        self.scroller = ThreadsScroller()

    def crawl_search(self, url, keyword, state_id: int, parlimen_id: int, keyword_type: int, max_scrolls: int, dun_id: int | None = None):

        playwright, context = self.browser.launch()
        page = context.new_page()

        processed = set()
        posts = []
        results = []

        try:

            page.goto(url)

            print(page.title())

            for scroll in range(max_scrolls):

                print(f"\ntr=== Scroll {scroll + 1} ===")

                messages = page.locator(self.POST_SELECTOR)

                count = messages.count()

                print(f"tr Visible results: {count}")

                for i in range(count):

                    try:

                        message = messages.nth(i)

                        post = self.parser.parse_post(keyword, message, url)

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

                print("Scrolling tr...")

                self.scroller.scroll(page, max_scrolls=1)

                page.wait_for_timeout(2000)

            for i, post in enumerate(posts, start=1):

                results.append(
                    {
                        "state_id": state_id,
                        "parlimen_id": parlimen_id,
                        "dun_id": dun_id,
                        "crawl_type": 1,
                        "keyword_type": keyword_type,
                        "source": "Threads",
                        "keyword": keyword,
                        "title": "-",
                        "url": None,
                        "published": post["published"],
                        "body": post["text"],
                    }
                )

            return results

        finally:

            context.close()
            playwright.stop()

