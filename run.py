import json
import os
from config.config import *
from utils.testcase_loader import TestCaseLoader
from core.logger import logger
import pytest
import sys
import subprocess
from core.common.ai_model import *
from core.common.judge import AiJudge

loader = TestCaseLoader()
TEST_DATA = loader.load_cases(TESTCASE_PATH)

try:
    if not TEST_DATA:
        logger.error("未加载到任何的测试用例，程序退出")
        sys.exit(1)
except Exception as e:
    logger.error(f"加载测试用例失败，错误信息：{e}")

os.environ["TEST_CASES_JSON"] = json.dumps(TEST_DATA, ensure_ascii=False)

testai_bot = AiKimi()
judge_bot = AiJudge()


if __name__ == "__main__":
    exit_code = pytest.main([
        TESTCASE_PATH, 
        "-v", 
        f"--alluredir={ALLURE_REPORT_DIR}",
        "--clean-alluredir",
        "-n", str(PARALLEL_WORKERS)
    ])

    try:
        subprocess.run(
            [ALLURE_CLI_PATH, "generate", ALLURE_REPORT_DIR, "-o", ALLURE_HTML_DIR, "--clean"],
            check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Allure 报告生成失败: {e.stderr}")

    allure_html_index = os.path.join(ALLURE_HTML_DIR, "index.html")
    logger.info(f"测试执行完成，HTML 报告已生成: file://{os.path.abspath(allure_html_index)}")

    sys.exit(exit_code)
