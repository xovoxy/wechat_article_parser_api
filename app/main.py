"""FastAPI 主入口"""
import time
from datetime import datetime
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import ArticleResponse, HealthResponse
from app.crawler import get_crawler, close_crawler
from app.parser import ArticleParser
from app.utils import validate_wechat_url, clean_article_url, random_delay
from app.config import settings

# 应用启动时间
start_time = time.time()

app = FastAPI(
    title="WeChat Article Parser API",
    description="一个用于解析微信公众号文章内容的 RESTful API 服务",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print("Starting WeChat Article Parser API...")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    await close_crawler()
    print("Shutting down WeChat Article Parser API...")


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """健康检查接口"""
    uptime = int(time.time() - start_time)
    return HealthResponse(
        status="ok",
        uptime=f"{uptime}s"
    )


@app.get("/api/parse", response_model=ArticleResponse)
async def parse_article(
    url: str = Query(..., description="微信公众号文章URL")
):
    """
    解析微信公众号文章
    
    - **url**: 微信公众号文章链接（例如：https://mp.weixin.qq.com/s/abcd1234）
    """
    # 验证URL
    if not validate_wechat_url(url):
        raise HTTPException(
            status_code=400,
            detail="Invalid WeChat article URL. URL must be from mp.weixin.qq.com"
        )
    
    # 清理URL，去掉查询参数
    url = clean_article_url(url)
    
    try:
        # 获取爬虫实例
        crawler = await get_crawler()
        
        # 随机延迟（反爬虫）
        random_delay(settings.MIN_DELAY, settings.MAX_DELAY)
        
        # 抓取文章HTML
        html = await crawler.fetch_article(url)
        
        if not html:
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch article content"
            )
        
        # 解析文章内容
        parser = ArticleParser()
        article_data = parser.parse(html, url)
        
        # 添加解析时间
        article_data["parsed_at"] = datetime.utcnow().isoformat() + "Z"
        
        return ArticleResponse(**article_data)
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error parsing article: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "WeChat Article Parser API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
