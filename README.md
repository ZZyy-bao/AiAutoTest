# AI 自动化回归测试框架

基于 **Python + pytest + Allure** 的 AI 自动化回归测试框架，支持通过 Excel 管理测试用例，自动调用 AI 模型进行问答测试，并使用 AI 裁判自动评判结果。

---

## 项目结构

```
ai_automation_test/
├── config/                   # 配置层
│   └── config.py             # 全局配置（模型、路径、环境变量）
├── core/                     # 核心层
│   ├── logger.py             # 日志模块（控制台彩色输出 + 文件日志）
│   └── commom/
│       ├── ai_model.py       # AI 模型封装（Kimi / DeepSeek）
│       └── judge.py          # AI 裁判，自动评判测试结果
├── test_case/                # 测试用例层
│   ├── conftest.py           # pytest 参数化配置
│   ├── test_runner.py        # 测试执行入口函数
│   └── *.xlsx                # Excel 测试用例数据
├── utils/
│   └── testcase_loader.py    # Excel 测试用例加载器
├── test_report/              # 报告层（自动按时间戳分目录）
│   └── YYYYMMDD-HHMMSS/
│       ├── allure-results/   # Allure 原始结果
│       ├── allure-report/    # Allure HTML 报告
│       └── logs/             # 运行日志
├── run.py                    # 一键执行入口
├── pytest.ini                # pytest 配置
├── .env                      # API Key 配置（不提交到 git）
└── requirements.txt          # 项目依赖
```

---

## 环境要求

| 组件 | 版本要求 | 说明 |
|------|---------|------|
| Python | >= 3.10 | 推荐使用 Conda 管理环境 |
| JDK | >= 8 | Allure 报告生成需要 |
| Allure CLI | >= 2.24 | 用于生成 HTML 测试报告 |

---

## 安装步骤

### 1. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 JDK（Allure 依赖）

Allure 需要 Java 运行环境。

**方法一：使用 winget 安装**

```bash
winget install -e --id=Microsoft.OpenJDK.17
```

**方法二：手动安装**

1. 下载 JDK 17：https://adoptium.net/
2. 安装完成后，配置环境变量：

```bash
# 验证安装
java -version
```

### 3. 配置 JAVA_HOME

Allure 需要 `JAVA_HOME` 环境变量指向 JDK 安装目录。

**Windows 设置方法：**

找到 JDK 安装路径（通常为 `C:\Program Files\Eclipse Adoptium\jdk-17.0.x.x-hotspot\`），然后：

```bash
# 临时设置（当前终端生效）
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.12.7-hotspot
set PATH=%JAVA_HOME%\bin;%PATH%

# 或通过 PowerShell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.0.12.7-hotspot"
$env:Path += ";$env:JAVA_HOME\bin"
```

永久设置：打开 **系统属性 → 高级 → 环境变量**，新建系统变量 `JAVA_HOME`，值为 JDK 安装路径，然后在 `Path` 中添加 `%JAVA_HOME%\bin`。

验证配置：

```bash
echo %JAVA_HOME%
java -version
```

### 4. 安装 Allure CLI

**方法一：使用 winget 安装**

```bash
winget install -e --id=Allure.Allure
```

**方法二：手动安装**

1. 下载 Allure：https://github.com/allure-framework/allure2/releases
2. 解压到任意目录（如 `D:\WorkFile\allure-2.40.0`）
3. 将该目录下的 `bin` 文件夹路径添加到系统环境变量 `Path` 中
4. 修改 `config/config.py` 中的 `ALLURE_CLI_PATH` 指向实际路径

验证安装：

```bash
allure --version
```

### 5. 配置 API Key

在项目根目录创建 `.env` 文件（已添加到 `.gitignore`，不会被提交）：

```ini
apikey_kimi=your_kimi_api_key_here
apikey_deepseek=your_deepseek_api_key_here
```

---

## 测试用例编写

在 `test_case/` 目录下创建 Excel 文件（`.xlsx`），包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| 用例ID | 用例唯一标识 | TC_MATH_01 |
| 模块 | 所属功能模块 | 数学计算 |
| 用户输入 | 发送给 AI 的问题 | 1+1 等于几？ |
| 期望结果描述 | 期望的 AI 回答标准 | 等于 2 |
| 系统提示词 | （可选）AI 系统提示词 | 你是一个数学助手 |

---

## 运行测试

```bash
# 一键执行所有测试
python run.py
```

运行完成后，在终端会输出报告路径，例如：
```
测试执行完成，HTML 报告已生成: test_report/20260509-172227/allure-report
```

---

## 查看测试报告

### 方法一：使用 Allure CLI（推荐）

```bash
allure open test_report\YYYYMMDD-HHMMSS\allure-report
```

会自动启动 Web 服务并在浏览器打开。

### 方法二：使用 Python HTTP 服务

```bash
cd test_report\YYYYMMDD-HHMMSS
python -m http.server 8080
```

浏览器访问 `http://localhost:8080/allure-report/`

### 方法三：直接打开（不推荐）

直接双击 `allure-report/index.html` 可能因浏览器安全策略显示空白页，建议使用方法一或二。

---

## 框架核心流程

```
Excel 测试用例
    ↓
testcase_loader.py 读取
    ↓
pytest 参数化（conftest.py）
    ↓
test_runner.py 逐条执行
    ├── 🤖 调用被测 AI（Kimi）
    ├── ⚖️ AI 裁判评分（DeepSeek）
    └── 📝 断言判定
    ↓
Allure 报告 + 日志
```

---

## 关键配置说明

`config/config.py` 主要配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `USING_MODEL_KIMI` | 被测 AI 模型 | kimi-k2.6 |
| `USING_MODEL_DEEPSEEK` | 裁判 AI 模型 | deepseek-v4-flash |
| `TESTCASE_PATH` | 测试用例目录 | test_case |
| `ALLURE_CLI_PATH` | allure 可执行文件路径 | 需根据实际安装路径修改 |
