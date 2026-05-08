import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
PROJECT_NAME = "AI TEST"
START_TIME = datetime.now().strftime("%Y%m%d-%H%M%S")
TEST_REPORT_DIR = f"test_report/{START_TIME}"
os.makedirs(TEST_REPORT_DIR,exist_ok=True)

BASE_MODEL_LLM_APIKEY = os.getenv("apikey_deepseek")    #用来判断文字输出AI好坏的基础模型
BASE_MODEL_LLM_BASEURL = "https://api.deepseek.com"
BASE_MODEL_LLM_MODEL = "deepseek-v4-flash"

DEFAULT_SYSTEM_CONTENT = "你是一个AI助手"
#kimi
USING_MODEL_KIMI = "kimi-k2.6"

#deepseek
USING_MODEL_DEEPSEEK = "deepseek-v4-flash"   #deepseek-v4-pro

#日志模块
LOG_DIR = os.path.join(TEST_REPORT_DIR,"logs")
LOG_NAME = "TestFramework"

