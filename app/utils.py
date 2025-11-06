"""工具函数"""
import re
import random
import time
from typing import Optional
from urllib.parse import urlparse


def validate_wechat_url(url: str) -> bool:
    """验证是否为有效的微信公众号文章URL"""
    if not url:
        return False
    
    parsed = urlparse(url)
    if parsed.netloc not in ["mp.weixin.qq.com", "weixin.qq.com"]:
        return False
    
    if not parsed.path.startswith("/s/"):
        return False
    
    return True


def random_delay(min_seconds: float = 1.0, max_seconds: float = 3.0) -> None:
    """随机延迟，用于反爬虫"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)


def clean_text(text: str) -> str:
    """清理文本内容"""
    if not text:
        return ""
    
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除首尾空白
    text = text.strip()
    return text


def format_publish_time(time_str: Optional[str]) -> Optional[str]:
    """格式化发布时间"""
    if not time_str:
        return None
    
    # 移除多余的空白
    time_str = clean_text(time_str)
    return time_str if time_str else None
