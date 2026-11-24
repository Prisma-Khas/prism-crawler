from app.crawler.news_crawlers.selectors import SELECTORS

def extract(page, article):

    selector = SELECTORS[article["source"]]

    page.goto(
    article["url"],
    wait_until="domcontentloaded",
    timeout=60000
    )   

    title = page.locator(
        selector["title"]
    ).inner_text()

    body = page.locator(
        selector["body"]
    ).inner_text()

    return {

        "title": title,

        "body": body
    }