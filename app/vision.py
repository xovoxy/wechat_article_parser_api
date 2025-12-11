"""图片 OCR 模块 - 使用 DashScope qwen3-vl-plus 模型"""
import time
from typing import List, Optional
import dashscope
from dashscope import MultiModalConversation
from app.config import settings


class VisionOCR:
    """使用 DashScope qwen3-vl-plus 模型进行图片 OCR"""
    
    def __init__(self):
        """初始化 OCR 服务"""
        if not settings.DASHSCOPE_API_KEY:
            raise ValueError("DASHSCOPE_API_KEY is not configured. Please set it in environment variables.")
        
        dashscope.api_key = settings.DASHSCOPE_API_KEY
    
    def extract_text_from_images(self, image_urls: List[str]) -> str:
        """
        从多张图片中提取文字内容
        
        Args:
            image_urls: 图片 URL 列表
            
        Returns:
            提取的文字内容（合并后的文本）
        """
        if not image_urls:
            return ""
        
        extracted_texts = []
        
        # 逐张处理图片（避免单次请求过大）
        for idx, image_url in enumerate(image_urls, 1):
            try:
                text = self._extract_text_from_single_image(image_url, idx, len(image_urls))
                if text:
                    extracted_texts.append(text)
                
                # 添加延迟避免限流
                if idx < len(image_urls):
                    time.sleep(0.5)
                    
            except Exception as e:
                print(f"Error extracting text from image {idx} ({image_url}): {e}")
                continue
        
        # 合并所有提取的文字
        return "\n\n".join(extracted_texts) if extracted_texts else ""
    
    def _extract_text_from_single_image(self, image_url: str, image_index: int, total_images: int) -> Optional[str]:
        """
        从单张图片中提取文字
        
        Args:
            image_url: 图片 URL
            image_index: 当前图片索引（从1开始）
            total_images: 总图片数
            
        Returns:
            提取的文字内容
        """
        # 构建消息内容
        content = [
            {"image": image_url},
            {"text": f"请提取这张图片中的所有文字内容。如果图片中有多段文字，请按顺序提取并保持段落结构。图片 {image_index}/{total_images}"}
        ]
        
        messages = [{"role": "user", "content": content}]
        
        try:
            # 调用 qwen3-vl-plus 模型
            response = MultiModalConversation.call(
                model="qwen3-vl-plus",
                messages=messages,
                result_format='message',
                stream=False
            )
            
            # 检查响应状态
            if response.status_code == 200:
                # 提取返回的文字内容
                output_content = response.output.choices[0].message.content
                
                # 处理返回内容（可能是列表或字符串）
                if isinstance(output_content, list):
                    # 查找文本内容
                    text_content = ""
                    for item in output_content:
                        if isinstance(item, dict) and 'text' in item:
                            text_content = item['text']
                            break
                    return text_content if text_content else None
                elif isinstance(output_content, str):
                    return output_content
                else:
                    # 尝试直接获取文本
                    return str(output_content)
            else:
                print(f"API call failed: status_code={response.status_code}, code={response.code}, message={response.message}")
                return None
                
        except Exception as e:
            print(f"Exception when calling DashScope API: {e}")
            return None
    
    def extract_text_from_images_batch(self, image_urls: List[str]) -> str:
        """
        批量处理多张图片（一次性发送所有图片）
        
        Args:
            image_urls: 图片 URL 列表
            
        Returns:
            提取的文字内容
        """
        if not image_urls:
            return ""
        
        # 构建消息内容
        content = [
            {"text": "请提取以下所有图片中的文字内容。如果有多张图片，请按顺序提取每张图片的文字，并在每张图片的文字前标注图片序号。"}
        ]
        
        # 添加所有图片
        for idx, image_url in enumerate(image_urls, 1):
            content.append({"image": image_url})
        
        messages = [{"role": "user", "content": content}]
        
        try:
            # 调用 qwen3-vl-plus 模型
            response = MultiModalConversation.call(
                model="qwen3-vl-plus",
                messages=messages,
                result_format='message',
                stream=False
            )
            
            if response.status_code == 200:
                output_content = response.output.choices[0].message.content
                
                if isinstance(output_content, list):
                    text_content = ""
                    for item in output_content:
                        if isinstance(item, dict) and 'text' in item:
                            text_content = item['text']
                            break
                    return text_content if text_content else ""
                elif isinstance(output_content, str):
                    return output_content
                else:
                    return str(output_content)
            else:
                print(f"Batch API call failed: status_code={response.status_code}, code={response.code}, message={response.message}")
                return ""
                
        except Exception as e:
            print(f"Exception when calling DashScope API (batch): {e}")
            return ""

