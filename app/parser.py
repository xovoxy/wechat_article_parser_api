"""HTML 解析模块"""
from typing import Optional
from bs4 import BeautifulSoup
from app.utils import clean_text, format_publish_time


class ArticleParser:
    """文章解析器"""
    
    @staticmethod
    def parse(html: str, url: str) -> dict:
        """解析微信公众号文章HTML"""
        soup = BeautifulSoup(html, 'lxml')
        
        # 提取标题
        title = ArticleParser._extract_title(soup)
        
        # 提取作者
        author = ArticleParser._extract_author(soup)
        
        # 提取发布时间
        publish_time = ArticleParser._extract_publish_time(soup)
        
        # 提取封面图
        cover = ArticleParser._extract_cover(soup)
        
        # 提取正文
        content_html, content_text = ArticleParser._extract_content(soup)
        
        # 提取阅读量和点赞数
        read_count, like_count = ArticleParser._extract_stats(soup)
        
        return {
            "title": title,
            "author": author,
            "publish_time": publish_time,
            "cover": cover,
            "content_html": content_html,
            "content_text": content_text,
            "read_count": read_count,
            "like_count": like_count,
            "url": url
        }
    
    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> str:
        """提取标题"""
        # 方法1: 从 meta 标签
        meta_title = soup.find('meta', property='og:title')
        if meta_title and meta_title.get('content'):
            return clean_text(meta_title['content'])
        
        # 方法2: 从 h1 或 h2 标签
        title_tag = soup.find('h1', class_='rich_media_title') or soup.find('h2', class_='rich_media_title')
        if title_tag:
            return clean_text(title_tag.get_text())
        
        # 方法3: 从 title 标签
        title_tag = soup.find('title')
        if title_tag:
            return clean_text(title_tag.get_text())
        
        return "未找到标题"
    
    @staticmethod
    def _extract_author(soup: BeautifulSoup) -> Optional[str]:
        """提取作者"""
        # 方法1: 从 meta 标签
        meta_author = soup.find('meta', property='og:article:author')
        if meta_author and meta_author.get('content'):
            return clean_text(meta_author['content'])
        
        # 方法2: 从 strong 标签中的公众号名称
        author_tag = soup.find('strong', class_='profile_nickname')
        if author_tag:
            return clean_text(author_tag.get_text())
        
        # 方法3: 从 a 标签
        author_tag = soup.find('a', class_='rich_media_meta_link')
        if author_tag:
            return clean_text(author_tag.get_text())
        
        return None
    
    @staticmethod
    def _extract_publish_time(soup: BeautifulSoup) -> Optional[str]:
        """提取发布时间"""
        # 方法1: 从 meta 标签
        meta_time = soup.find('meta', property='og:article:published_time')
        if meta_time and meta_time.get('content'):
            return format_publish_time(meta_time['content'])
        
        # 方法2: 从 em 标签
        time_tag = soup.find('em', class_='rich_media_meta_text')
        if time_tag:
            time_text = time_tag.get_text()
            if any(char.isdigit() for char in time_text):  # 包含数字
                return format_publish_time(time_text)
        
        # 方法3: 从 id 为 publish_time 的元素
        time_tag = soup.find(id='publish_time')
        if time_tag:
            return format_publish_time(time_tag.get_text())
        
        return None
    
    @staticmethod
    def _extract_cover(soup: BeautifulSoup) -> Optional[str]:
        """提取封面图"""
        # 方法1: 从 meta 标签
        meta_image = soup.find('meta', property='og:image')
        if meta_image and meta_image.get('content'):
            return meta_image['content']
        
        # 方法2: 从 img 标签
        img_tag = soup.find('img', class_='rich_media_cover_img')
        if img_tag and img_tag.get('src'):
            return img_tag['src']
        
        return None
    
    @staticmethod
    def _extract_content(soup: BeautifulSoup) -> tuple[str, str]:
        """提取正文内容（HTML 和纯文本）"""
        # 查找正文容器
        content_div = soup.find('div', class_='rich_media_content') or soup.find('div', id='js_content')
        
        if not content_div:
            return "", ""
        
        # 移除不需要的元素
        for tag in content_div.find_all(['script', 'style', 'iframe']):
            tag.decompose()
        
        # 提取 HTML
        content_html = str(content_div)
        
        # 提取纯文本
        content_text = clean_text(content_div.get_text())
        
        return content_html, content_text
    
    @staticmethod
    def _extract_stats(soup: BeautifulSoup) -> tuple[Optional[int], Optional[int]]:
        """提取阅读量和点赞数"""
        read_count = None
        like_count = None
        
        # 查找阅读量
        read_elem = soup.find('span', class_='read_num') or soup.find(id='readNum')
        if read_elem:
            read_text = read_elem.get_text()
            try:
                read_count = int(''.join(filter(str.isdigit, read_text)))
            except ValueError:
                pass
        
        # 查找点赞数
        like_elem = soup.find('span', class_='like_num') or soup.find(id='likeNum')
        if like_elem:
            like_text = like_elem.get_text()
            try:
                like_count = int(''.join(filter(str.isdigit, like_text)))
            except ValueError:
                pass
        
        return read_count, like_count
