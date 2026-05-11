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
JUDGE_SYSTEM_CONTENT = "你是一位资深的软件测试专家。请分析 AI 的回答是否准确解决了用户的问题，且符合期望结果的语义。请只输出 JSON 格式，不要包含任何其他文字。格式规范：{\"result\": true/false, \"reason\": \"失败原因或空字符串\"}如果回答正确，result为 true，reason为空字符串；如果回答错误，result为 false，并把失败的原因赋值给reason."
JUDGE_MODEL = "deepseek"   #kimi
#kimi
USING_MODEL_KIMI = "kimi-k2.6"

#deepseek
USING_MODEL_DEEPSEEK = "deepseek-v4-flash"   #deepseek-v4-pro

#日志模块
LOG_DIR = os.path.join(TEST_REPORT_DIR,"logs")
LOG_NAME = "TestFramework"

TESTCASE_PATH = "test_case"
ALLURE_REPORT_DIR = os.path.join(TEST_REPORT_DIR, "allure-results")
ALLURE_HTML_DIR = os.path.join(TEST_REPORT_DIR, "allure-report")
ALLURE_CLI_PATH = "D:/WorkFile/Tool/allure-2.40.0/bin/allure.bat"
