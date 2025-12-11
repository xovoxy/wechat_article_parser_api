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
    
    # 查找所有 img 标签
    img_tags = search_area.find_all('img')
    
    for img in img_tags:
        # 优先使用 data-src（微信图片懒加载）
        image_url = img.get('data-src') or img.get('src') or img.get('data-original')
        
        if image_url:
            # 清理和验证 URL
            image_url = image_url.strip()
            if is_valid_image_url(image_url):
                # 避免重复
                if image_url not in image_urls:
                    image_urls.append(image_url)
    
    return image_urls


def is_valid_image_url(url: str) -> bool:
    """
    验证图片 URL 是否有效
    
    Args:
        url: 图片 URL
        
    Returns:
        是否为有效的图片 URL
    """
    if not url:
        return False
    
    # 移除可能的查询参数和片段
    parsed = urlparse(url)
    
    # 检查是否为有效的 HTTP/HTTPS URL
    if parsed.scheme not in ['http', 'https']:
        return False
    
    # 检查路径是否为空
    if not parsed.path:
        return False
    
    # 排除一些明显不是图片的 URL（如 base64 data URI 等）
    if url.startswith('data:'):
        return False
    
    # 微信图片常见域名
    wechat_image_domains = [
        'mmbiz.qpic.cn',
        'mmbiz.qlogo.cn',
        'wx.qlogo.cn',
        'mp.weixin.qq.com'
    ]
    
    # 如果域名是微信图片域名，认为是有效的
    if parsed.netloc in wechat_image_domains:
        return True
    
    # 检查文件扩展名（可选）
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    path_lower = parsed.path.lower()
    if any(path_lower.endswith(ext) for ext in image_extensions):
        return True
    
    # 如果没有扩展名但路径包含图片相关关键词，也认为可能是图片
    if 'image' in path_lower or 'img' in path_lower or 'pic' in path_lower:
        return True
    
    return False
