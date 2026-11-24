from fastapi.responses import HTMLResponse
from app.crawler.social_media_crawlers.threads.crawler import ThreadsCrawler
from app.crawler.social_media_crawlers.twitter.crawler import TwitterCrawler
from app.crawler.news_crawlers.crawler import NewsCrawler
from urllib.parse import quote

def render_post_threads_search(
    keyword: str, keyword_type: int, max_scrolls: int, state_id: int, parlimen_id: int, dun_id: int
):
    crawler = ThreadsCrawler()

    search_keyword = ''
    if keyword_type == 1:
        search_keyword = f"Parlimen {keyword}"
    elif keyword_type == 2:
        search_keyword = f"Dun {keyword}"
             
    search_keyword = f'"{search_keyword}"'
    
    url = f"https://www.threads.com/search?" f"q={quote(search_keyword)}&serp_type=tags"
    results = crawler.crawl_search(
        url=url,
        keyword=keyword,
        state_id=state_id,
        parlimen_id=parlimen_id,
        keyword_type=keyword_type,
        max_scrolls=max_scrolls,
        dun_id=dun_id,
    )
    
    return {"success": True, "total_posts": len(results), "data": results}

def render_post_twitter_search(
    keyword: str,
    keyword_type: int,
    max_scrolls: int,
    state_id: int,
    parlimen_id: int,
    dun_id: int,
):
    crawler = TwitterCrawler()
    
    if keyword_type == 1:
            search_keyword = f"Parlimen {keyword}"
    elif keyword_type == 2:
        search_keyword = f"Dun {keyword}"
    else:
        search_keyword = keyword

    search_keyword = quote(f'"{search_keyword}"')

    url = (
        f"https://x.com/search?"
        f"q={search_keyword}&src=typed_query&f=live"
    )
    
    results = crawler.crawl_search(
        url=url,
        keyword=keyword,
        keyword_type=keyword_type,
        state_id=state_id,
        parlimen_id=parlimen_id,
        dun_id=dun_id,
        max_scrolls=max_scrolls,
    )
    
    return {
        "success": True,
        "total_posts": len(results),
        "data": results,
    }



def render_post_news_search(keyword: str, state_id: int, parlimen_id: int, dun_id: int):
    crawler = NewsCrawler()
    results = crawler.crawl_search(keyword=keyword, state_id=state_id, parlimen_id=parlimen_id, dun_id=dun_id)
    return {"success": True, "total_posts": len(results), "data": results}
