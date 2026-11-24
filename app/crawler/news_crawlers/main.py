import json
import os

from parser import get_articles

from extractor import extract

from playwright.sync_api import sync_playwright

DUN = input("Enter Keyword: ")

articles = get_articles()

results = []

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    for article in articles:

        print(article["title"])

        try:

            data = extract(
                page,
                article
            )

            text = (
                data["title"] +
                "\n" +
                data["body"]
            ).lower()

            if DUN.lower() not in text:

                continue

            results.append({

                "source": article["source"],

                "title": data["title"],

                "url": article["url"],

                "published": article["published"],

                "body": data["body"]
            })

            print("✓ Related")

        except Exception as e:

            print(e)

    browser.close()

os.makedirs(
    "output",
    exist_ok=True
)

with open(
    "output/articles.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        results,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"\nFound {len(results)} related articles.")