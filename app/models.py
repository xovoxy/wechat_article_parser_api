"""数据模型"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl, Field


class ArticleResponse(BaseModel):
    """文章解析响应模型"""
    title: str = Field(..., description="文章标题")
    author: Optional[str] = Field(None, description="作者")
    publish_time: Optional[str] = Field(None, description="发布时间")
    cover: Optional[str] = Field(None, description="封面图URL")
    content_html: str = Field(..., description="HTML格式正文")
    content_text: str = Field(..., description="纯文本格式正文")
    read_count: Optional[int] = Field(None, description="阅读量")
    like_count: Optional[int] = Field(None, description="点赞数")
    url: str = Field(..., description="文章URL")
    parsed_at: str = Field(..., description="解析时间（ISO格式）")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "深度学习的三个阶段",
                "author": "AI小站",
                "publish_time": "2025-10-20 08:30",
                "cover": "https://mmbiz.qpic.cn/xyz.jpg",
                "content_html": "<p>近年来，深度学习...</p>",
                "content_text": "近年来，深度学习的发展经历了三个阶段...",
                "read_count": 12345,
                "like_count": 678,
                "url": "https://mp.weixin.qq.com/s/abcd1234",
                "parsed_at": "2025-11-04T21:35:12Z"
            }
        }


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    uptime: Optional[str] = Field(None, description="运行时长（秒）")
