import pytest
import allure


@allure.feature("AI 自动化回归测试 (Excel驱动)")
def test_ai_executor(case_data):
    import run

    if not hasattr(run, 'testai_bot') or not hasattr(run, 'judge_bot'):
        pytest.fail("模型未初始化，请检查 run.py 是否正常执行")

    testai_bot = run.testai_bot
    judge_bot = run.judge_bot

    user_input = case_data['用户输入']
    expected_criteria = case_data['期望结果描述']
    system_prompt = case_data.get('系统提示词', "你是一个助手")

    with allure.step("🤖 执行 AI 问答"):
        try:
            actual_output = testai_bot.chat(user_input, system_content=system_prompt)
            allure.attach(actual_output, name="AI 实际回答", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            error_msg = str(e)
            allure.attach(error_msg, name="调用异常", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"AI 调用失败: {error_msg}")

    with allure.step("⚖️ AI 裁判评分"):
        judge_task = judge_bot.judge(user_input, actual_output, expected_criteria)
        allure.attach(str(judge_task), name="裁判评价", attachment_type=allure.attachment_type.TEXT)

    with allure.step("📝 最终结果判定"):
        if judge_task["sucess"]:
            if not judge_task["result"].get("result"):
                reason = judge_task["result"].get("reason", "未知原因")
                pytest.fail(f"测试未通过: {reason}")
        else:
            pytest.fail(f"judge模型输出内容格式不对：{judge_task['result']}")
