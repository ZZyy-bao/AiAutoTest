from core.commom.ai_model import *
from core.logger import logger
from config.config import JUDGE_SYSTEM_CONTENT
import json

class AiJudge:
    def __init__(self):
        self.judge_system_content = JUDGE_SYSTEM_CONTENT
        self.judge_task_list = []
        self.set_judge_model

    def set_judge_model(self):
        if JUDGE_MODEL == "kimi":
            self.judge_model = AiKimi()
        else:
            self.judge_model = AiDeepseek()
            
    def judge(self,user_input,ai_output,target_content):
        content = f"这是用户输入：{user_input},这是期望的AI回答：{target_content},这是AI实际的输出：{ai_output}"
        response_content = self.judge_model.chat(
            user_content=content,
            system_content=self.judge_system_content
            )
        judge_success = False
        try:
            response_content = json.loads(response_content)
            judge_success = True
        except:
            logger.error(f"判断模型输出的结果不是期望的格式：{response_content}")
        logger.info(f"模型判断的结果为{response_content}")
        judge_task = {
            "sucess":judge_success,
            "result":response_content
        }
        self.judge_task_list.append(judge_task)
        return judge_task
    
        