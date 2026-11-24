# from fastapi import FastAPI
# from pydantic import BaseModel
# from app.crawler.social_media_crawlers.threads.crawler import ThreadsCrawler
# from app.query_crawl import render_get_threads_search
# from app.query_crawl import render_get_news_search
# from fastapi.concurrency import run_in_threadpool

# app = FastAPI()


# class ThreadsRequest(BaseModel):
#     keyword: str
#     max_scrolls: int = 5


# @app.get("/get_search")
# async def get_search(
#     keyword: str, keyword_type: int, dun_id: int, crawl_type: int, max_scrolls: int = 2
# ):

#     threads = await run_in_threadpool(
#         render_get_threads_search,
#         keyword,
#         keyword_type,
#         max_scrolls,
#         dun_id,
#     )

#     news = await run_in_threadpool(
#         render_get_news_search,
#         keyword,
#         dun_id,
#     )
#     data = threads["data"] + news["data"]

#     return {"success": True, "total_posts": len(data), "data": data}
#     # if crawl_type == 1:
#     #     return render_get_threads_search(keyword, keyword_type, dun_id, max_scrolls)
#     # elif crawl_type == 2:
#     #     return render_get_news_search(keyword, dun_id)
from fastapi import FastAPI

# whisp4r
# from app.routes.whisper_router import router as whisper_router
# from app.whisper.config import MODEL_NAME, DEVICE, COMPUTE_TYPE
# from app.whisper.models.response import RootResponse, HealthResponse

# crawler
from app.routes.crawler_router import router as crawler_router

app = FastAPI(title="OSINT API", version="1.0.0")

# Register routers
# app.include_router(whisper_router, prefix="/whisper", tags=["Whisper"])
app.include_router(crawler_router, prefix="/crawler", tags=["Crawler"])


# @app.get("/", response_model=RootResponse)
# def root():
#     return RootResponse(
#         status="running", model=MODEL_NAME, device=DEVICE, compute_type=COMPUTE_TYPE
#     )


# @app.get("/health", response_model=HealthResponse)
# def health():
#     return HealthResponse(success=True)
