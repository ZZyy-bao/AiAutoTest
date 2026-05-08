项目框架：
基于Python+pytest+allure
项目结构：
ai_automation_test/
├── config/                 # 配置层：集中管理所有配置
│   ├── settings.yaml       # 全局配置（如项目名、日志级别）
│   └── env/                # 多环境配置，实现环境与代码分离
│       ├── dev.yaml        # 开发环境 (base_url, db_host等)
│       ├── test.yaml       # 测试环境
│       └── prod.yaml       # 生产环境
├── core/                   # 核心层：框架的基础设施，与具体业务无关
│   ├── __init__.py
│   ├── config_loader.py    # 配置加载器，动态读取不同环境配置
│   ├── http_client.py      # HTTP请求封装，统一处理请求/响应/异常
│   └── logger.py           # 日志模块，提供统一的日志记录接口
├── api/                    # 接口层：按业务模块封装API，实现PO模式思想
│   ├── __init__.py
│   ├── base_api.py         # API基类，定义通用方法
│   ├── user_api.py         # 用户模块接口（登录、注册等）
│   └── order_api.py        # 订单模块接口（创建、查询等）
├── testcases/              # 测试用例层：纯粹的测试业务逻辑
│   ├── __init__.py
│   ├── conftest.py         # 全局Fixture，如登录获取Token
│   ├── user/               # 按模块组织用例，结构清晰
│   │   ├── test_login.py
│   │   └── test_register.py
│   └── order/
│       └── test_create_order.py
├── testdata/               # 数据层：测试数据与代码分离，便于维护
│   ├── user_data.yaml      # 用户模块测试数据
│   └── order_data.yaml     # 订单模块测试数据
├── utils/                  # 工具层：通用工具函数，提高代码复用率
│   ├── __init__.py
│   ├── data_utils.py       # 数据处理工具（如YAML/JSON读写）
│   ├── assert_utils.py     # 自定义断言工具，封装复杂断言逻辑
│   └── encrypt.py          # 加密工具（如MD5、AES）
├── reports/                # 报告层：存放测试报告
│   ├── allure-results/     # Allure执行的中间结果
│   └── allure-report/      # 生成的最终HTML报告
├── logs/                   # 日志层：存放运行日志
├── conftest.py             # 项目根级Fixture，可定义全局共享的资源
├── pytest.ini              # Pytest配置文件，定义执行规则
├── run.py                  # 一键执行入口，可集成命令行参数
└── requirements.txt        # 项目依赖清单
配置层 (config/)
目的：将环境相关的配置（如API地址、数据库连接）从代码中剥离，实现“一次编写，多处运行”。
实现：通过 config_loader.py 根据启动参数（如 --env test）动态加载 env/test.yaml 等文件，使切换测试环境变得非常简单。
核心层 (core/)
目的：封装框架最底层、最通用的能力，是整个框架的基石。
实现：
http_client.py：基于 requests 库进行二次封装，统一处理请求头、超时、Token注入、日志记录和异常抛出。测试用例只需调用简单的方法，无需关心HTTP细节。
logger.py：封装日志库，提供统一的日志格式和输出方式（控制台+文件）。
接口层 (api/)
目的：采用页面对象模型（Page Object Model, POM）的设计思想，将每个接口或一组相关接口封装成一个类或方法。
优势：测试用例层 (testcases/) 不再直接调用 http_client，而是调用 api/ 层封装好的方法。当接口发生变化时（如URL路径改变），只需修改 api/ 层的代码，所有引用它的测试用例都无需改动，极大地提高了可维护性。
测试用例层 (testcases/)
目的：只关注测试业务逻辑，即“调用哪个接口，传入什么数据，期望什么结果”。
实现：利用 pytest 的强大功能。
Fixture：在 conftest.py 中定义 @pytest.fixture，可以方便地处理测试前置（如登录获取Token）和后置（如清理数据）操作。yield 关键字可以清晰地将前置和后置逻辑分离。
参数化：结合 @pytest.mark.parametrize 和 testdata/ 中的数据，可以轻松实现数据驱动测试，用一套代码测试多组数据，减少代码冗余。
数据层 (testdata/)
目的：实现测试数据与测试代码的完全分离。
优势：测试数据使用 YAML 或 JSON 等易读的格式存储。测试人员可以独立地增删改测试数据，而无需触碰代码，降低了维护门槛和风险。
工具层 (utils/)
目的：收集和封装项目中可复用的通用函数。
示例：data_utils.py 负责读取 testdata/ 和 config/ 中的文件；assert_utils.py 可以封装复杂的断言，如校验响应JSON中的多个字段、响应时间等。