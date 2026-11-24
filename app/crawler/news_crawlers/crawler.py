import json
import os

from app.crawler.news_crawlers.parser import get_articles
from app.crawler.news_crawlers.extractor import extract
from app.crawler.browser_news import BrowserNews


class NewsCrawler:
    def crawl_search(
        self, keyword: str | None, state_id: int, parlimen_id: int, dun_id: int
    ):
        articles = get_articles()
        results = []

        browser = BrowserNews(headless=True)
        page = browser.start()

        try:
            for article in articles:

                print(article["title"])

                try:
                    data = extract(page, article)

                    text = (data["title"] + "\n" + data["body"]).lower()

                    if keyword.lower() not in text:
                        continue

                    results.append(
                        {
                            "state_id": state_id,
                            "parlimen_id": parlimen_id,
                            "dun_id": dun_id,
                            "crawl_type": 2,
                            "keyword_type": 0,
                            "source": article["source"],
                            "keyword": keyword,
                            "title": data["title"],
                            "url": article["url"],
                            "published": article["published"],
                            "body": data["body"],
                        }
                    )

                    print("✓ Related")

                except Exception as e:
                    print(e)

        finally:
            browser.close()
        return results
