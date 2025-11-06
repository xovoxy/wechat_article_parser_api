"""Playwright 爬虫模块"""
import asyncio
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
from app.config import settings
from app.utils import random_delay


class WeChatCrawler:
    """微信公众号文章爬虫"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
    
    async def start(self):
        """启动浏览器"""
        if self.browser is None:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=settings.PLAYWRIGHT_HEADLESS,
                args=['--disable-blink-features=AutomationControlled']
            )
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    
    async def fetch_article(self, url: str) -> Optional[str]:
        """抓取文章HTML内容"""
        if not self.browser:
            await self.start()
        
        page: Page = await self.browser.new_page()
        
        try:
            # 设置 User-Agent
            await page.set_extra_http_headers({
                'User-Agent': settings.USER_AGENT
            })
            
            # 访问页面
            await page.goto(
                url,
                wait_until='networkidle',
                timeout=settings.PLAYWRIGHT_TIMEOUT
            )
            
            # 等待页面加载完成（微信公众号文章可能需要时间渲染）
            await asyncio.sleep(2)
            
            # 获取完整HTML
            html = await page.content()
            
            return html
        
        except PlaywrightTimeoutError:
            print(f"Timeout error when fetching: {url}")
            return None
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        finally:
            await page.close()
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()


# 全局爬虫实例（单例模式）
_crawler_instance: Optional[WeChatCrawler] = None


async def get_crawler() -> WeChatCrawler:
    """获取爬虫实例（单例）"""
    global _crawler_instance
    if _crawler_instance is None:
        _crawler_instance = WeChatCrawler()
        await _crawler_instance.start()
    return _crawler_instance


async def close_crawler():
    """关闭爬虫实例"""
    global _crawler_instance
    if _crawler_instance:
        await _crawler_instance.close()
        _crawler_instance = None
