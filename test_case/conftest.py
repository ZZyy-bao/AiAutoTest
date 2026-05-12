import json
import os
import pytest
import allure


def pytest_generate_tests(metafunc):
    if "case_data" in metafunc.fixturenames:
        cases_json = os.environ.get("TEST_CASES_JSON")
        if cases_json:
            test_data = json.loads(cases_json)
        else:
            import run
            test_data = run.TEST_DATA
        metafunc.parametrize(
            "case_data",
            test_data,
            ids=lambda x: f"[{x.get('用例ID', 'Unknown')}]"
        )


def pytest_runtest_call(item):
    import run
    if "case_data" in item.funcargs and hasattr(run, 'TEST_DATA'):
        case = item.funcargs["case_data"]
        case_id = case.get('用例ID', 'Unknown')
        input_text = str(case.get('用户输入', ''))[:30]
        allure.dynamic.title(f"{case_id}: {input_text}...")
        allure.dynamic.description(f"模块: {case.get('模块')}\n验收标准: {case.get('期望结果描述')}")
