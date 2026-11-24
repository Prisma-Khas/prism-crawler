import asyncio
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from app.query_crawl import (
    render_post_threads_search,
    render_post_twitter_search,
    render_post_news_search,
)

router = APIRouter()


class DunItem(BaseModel):
    dun_id: int
    keyword: str


class SearchRequest(BaseModel):
    keyword: str | None = None
    state_id: int | None = None
    parlimen_id: int | None = None
    dun_id: int | None = None
    duns: List[DunItem] | None = None
    keyword_type: int
    crawl_type: List[int]
    max_scrolls: int = 2


@router.post("/get_search")
async def get_search(request: SearchRequest):

    threads = {"data": []}
    news = {"data": []}
    twitter = {"data": []}

    # Determine searches
    if request.keyword_type in (1, 2):

        if not request.keyword:
            raise HTTPException(
                status_code=400,
                detail="keyword is required."
            )

        searches = [
            {
                "keyword": request.keyword,
                "dun_id": request.dun_id,
            }
        ]

    elif request.keyword_type == 3:

        if not request.duns:
            raise HTTPException(
                status_code=400,
                detail="duns is required when keyword_type = 3."
            )

        searches = [
            {
                "keyword": d.keyword,
                "dun_id": d.dun_id,
            }
            for d in request.duns
        ]

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid keyword_type."
        )

    # Crawl
    for search in searches:

        tasks = []

        if 1 in request.crawl_type:
            tasks.append(
                (
                    "threads",
                    run_in_threadpool(
                        render_post_threads_search,
                        search["keyword"],
                        request.keyword_type,
                        request.max_scrolls,
                        request.state_id,
                        request.parlimen_id,
                        search["dun_id"],
                    )
                )
            )
            tasks.append(
                (
                    "twitter",
                    run_in_threadpool(
                        render_post_twitter_search,
                        search["keyword"],
                        request.keyword_type,
                        request.max_scrolls,
                        request.state_id,
                        request.parlimen_id,
                        search["dun_id"],
                    )
                )
            )

        if 2 in request.crawl_type:
            tasks.append(
                (
                    "news",
                    run_in_threadpool(
                        render_post_news_search,
                        search["keyword"],
                        request.state_id,
                        request.parlimen_id,
                        search["dun_id"],
                    )
                )
            )

        if not tasks:
            continue

        task_names = [t[0] for t in tasks]
        task_coroutines = [t[1] for t in tasks]

        results = await asyncio.gather(*task_coroutines)

        for task_name, result in zip(task_names, results):

            if not result:
                continue

            if task_name == "threads":
                threads["data"].extend(result.get("data", []))

            elif task_name == "news":
                news["data"].extend(result.get("data", []))
            elif task_name == "twitter":
                twitter["data"].extend(result.get("data", []))

    data = threads["data"] + news["data"] + twitter["data"]

    return {
        "success": True,
        "total_posts": len(data),
        "data": data,
    }