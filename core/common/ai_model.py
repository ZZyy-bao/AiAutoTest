from openai import OpenAI,APIError, RateLimitError
import os
from dotenv import load_dotenv
from config.config import *
from core.logger import logger
from datetime import datetime
load_dotenv()

class AiChat:
    def __init__(self,api_key,base_url,model_name):
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        self.chat_messages_list = []
    
    def chat(self,user_content,system_content = DEFAULT_SYSTEM_CONTENT,context=""):
        messages = []
        try:
            if hasattr(context,list) and context:
                messages.append(context)
            else:
                logger.info(f"context为空或者不为表格：{context}")
            start_time = datetime.now().strftime("%H%M%S")
            messages.append([
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": user_content}
                ])
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            end_time = datetime.now().strftime("%H%M%S")
            response_content = completion.choices[0].message.content
            logger.info(f"[{self.model_name}] 请求成功 | 耗时: {start_time}-{end_time} | 输出长度: {len(response_content)}")
            chat_message = {
                "model_name":self.model_name,
                "system_content": system_content,
                "user_content": user_content,
                "response_content": response_content,
                "response_start_time":start_time,
                "response_end_time":end_time
            }
            
            self.chat_messages_list.append(chat_message)
            return response_content
            
        except RateLimitError as e:
            logger.error(f"触发限流 (RateLimit): {e}")
        except APIError as e:
            logger.error(f"OpenAI API 错误: {e}")
        except Exception as e:
            logger.error(f"未知错误: {e}")
        return None
    
class AiKimi(AiChat):
    def __init__(self):
        api_key_kimi = os.getenv("apikey_kimi")
        if not api_key_kimi:
            logger.error("环境变量 apikey_kimi 未设置")

        base_url = "https://api.moonshot.cn/v1"
        super().__init__(
            api_key=api_key_kimi, 
            base_url=base_url,
            model_name=USING_MODEL_KIMI
        )
        logger.info(f"AiKimi 初始化完成, model={USING_MODEL_KIMI}")

class AiDeepseek(AiChat):
    def __init__(self):
        api_key_deepseek = os.getenv("apikey_deepseek")
        if not api_key_deepseek:
            logger.error("环境变量 apikey_deepseek 未设置")

        base_url = "https://api.deepseek.com"
        super().__init__(
            api_key=api_key_deepseek, 
            base_url=base_url,
            model_name=USING_MODEL_DEEPSEEK
        )
        logger.info(f"AiDeepseek 初始化完成, model={USING_MODEL_DEEPSEEK}")

