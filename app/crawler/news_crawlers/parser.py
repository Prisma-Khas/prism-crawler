import feedparser
from app.crawler.news_crawlers.feeds import RSS_FEEDS

def get_articles():

    articles = []

    for feed in RSS_FEEDS:

        print(f"Reading {feed['name']}...")

        rss = feedparser.parse(feed["rss"])

        for item in rss.entries:

            articles.append({

                "source": feed["name"],
                "title": item.title,
                "url": item.link,
                "published": item.get("published", "")
            })

    return articles