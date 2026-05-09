import pytest
import allure


def pytest_generate_tests(metafunc):
    import run
    if hasattr(run, 'TEST_DATA') and "case_data" in metafunc.fixturenames:
        metafunc.parametrize(
            "case_data",
            run.TEST_DATA,
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
