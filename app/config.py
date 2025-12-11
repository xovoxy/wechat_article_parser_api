"""环境配置模块"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    
    # 并发控制
    MAX_CONCURRENCY: int = int(os.getenv("MAX_CONCURRENCY", "5"))
    
    # User-Agent
    USER_AGENT: str = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # API Token (可选)
    API_TOKEN: Optional[str] = os.getenv("API_TOKEN", None)
    
    # 请求延迟配置（秒）
    MIN_DELAY: float = 1.0
    MAX_DELAY: float = 3.0
    
    # Playwright 配置
    PLAYWRIGHT_HEADLESS: bool = True
    PLAYWRIGHT_TIMEOUT: int = 30000  # 30秒
    
    # DashScope 配置
    DASHSCOPE_API_KEY: Optional[str] = os.getenv("DASHSCOPE_API_KEY", None)
    
    # 图片文章检测阈值
    IMAGE_ARTICLE_TEXT_THRESHOLD: int = int(os.getenv("IMAGE_ARTICLE_TEXT_THRESHOLD", "100"))  # 文本长度阈值
    IMAGE_ARTICLE_MIN_IMAGES: int = int(os.getenv("IMAGE_ARTICLE_MIN_IMAGES", "3"))  # 最少图片数量
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
