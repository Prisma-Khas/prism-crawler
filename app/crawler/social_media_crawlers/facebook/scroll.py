import time


class FacebookScroller:

    def scroll(self, page, max_scrolls=10):

        previous = page.evaluate(
            "document.body.scrollHeight"
        )

        for _ in range(max_scrolls):

            page.evaluate(
                "window.scrollTo(0, document.body.scrollHeight)"
            )

            time.sleep(2)

            current = page.evaluate(
                "document.body.scrollHeight"
            )

            if current == previous:
                break

            previous = current