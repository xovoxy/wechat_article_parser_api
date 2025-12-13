"""工具函数"""
import re
import random
import time
from typing import Optional, List
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag


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


def extract_image_urls(soup: BeautifulSoup, content_div: Optional[Tag] = None) -> List[str]:
    """
    从 BeautifulSoup 对象中提取所有图片 URL
    
    Args:
        soup: BeautifulSoup 对象
        content_div: 可选的正文容器元素，如果提供则只从此元素中提取
        
    Returns:
        图片 URL 列表
    """
    image_urls = []
    
    # 确定搜索范围
    search_area = content_div if content_div else soup
    
    # 1. 查找所有 img 标签
    img_tags = search_area.find_all('img')
    
    for img in img_tags:
        # 跳过封面图（已经在 cover 字段中）
        if img.get('class') and 'rich_media_cover_img' in img.get('class', []):
            continue
        
        # 优先使用 src（实际加载的图片），然后是 data-src（懒加载占位符）
        # 微信图片通常 src 是实际加载的图片，data-src 是懒加载的原始图片
        image_url = (
            img.get('src') or  # 优先使用 src（实际加载的图片）
            img.get('data-src') or  # 然后是 data-src（懒加载）
            img.get('data-original') or
            img.get('data-lazy-src') or
            img.get('data-lazy')
        )
        
        if image_url:
            # 清理 URL（移除可能的锚点）
            image_url = image_url.split('#')[0].strip()
            
            # 只保留完整的 HTTP/HTTPS URL，忽略相对路径
            if image_url.startswith(('http://', 'https://')):
                # 避免重复
                if image_url not in image_urls:
                    image_urls.append(image_url)
    
    # 2. 查找所有 a 标签中的 imgurl 属性（微信文章中的图片链接）
    a_tags = search_area.find_all('a', attrs={'imgurl': True})
    for a_tag in a_tags:
        imgurl = a_tag.get('imgurl')
        if imgurl:
            # 清理 URL（移除可能的锚点）
            imgurl = imgurl.split('#')[0].strip()
            
            # 只保留完整的 HTTP/HTTPS URL，忽略相对路径
            if imgurl.startswith(('http://', 'https://')):
                # 避免重复
                if imgurl not in image_urls:
                    image_urls.append(imgurl)
    
    return image_urls
