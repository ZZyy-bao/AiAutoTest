import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from config.config import LOG_DIR,LOG_NAME
# 尝试导入 colorlog，如果没有安装则不使用颜色
try:
    import colorlog
    USE_COLOR = True
except ImportError:
    USE_COLOR = False

class LogSetup:
    """
    日志配置管理类
    单例模式，确保整个项目中日志配置只初始化一次
    """
    _instance = None
    _logger = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, name=LOG_NAME, log_dir=LOG_DIR, level=logging.DEBUG):
        if self._logger is not None:
            return

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 1. 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 2. 定义日志格式
        # 标准格式：时间 | 文件名:行号 | 级别 | 消息
        fmt_str = "%(asctime)s | %(filename)s:%(lineno)d | %(levelname)s | %(message)s"
        date_fmt = "%Y-%m-%d %H:%M:%S"

        # 3. 控制台处理器 (StreamHandler)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG) # 控制台通常显示所有级别
        
        if USE_COLOR:
            # 使用 colorlog 配置彩色输出，方便肉眼识别 ERROR/WARNING
            color_fmt = "%(log_color)s" + fmt_str
            console_formatter = colorlog.ColoredFormatter(
                color_fmt,
                datefmt=date_fmt,
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                }
            )
        else:
            console_formatter = logging.Formatter(fmt_str, datefmt=date_fmt)
            
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # 4. 文件处理器 (TimedRotatingFileHandler)
        # 按天切割日志，保留 7 天，使用 UTF-8 编码
        log_file = os.path.join(log_dir, "framework.log")
        file_handler = TimedRotatingFileHandler(
            filename=log_file,
            when="D",       # 按天切割
            interval=1,     # 每隔 1 天
            backupCount=7,  # 保留 7 个文件（即7天）
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(fmt_str, datefmt=date_fmt)
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        self._logger = self.logger

    def get_logger(self):
        return self._logger

# 全局单例获取函数
def get_logger(name="TestFramework"):
    """
    在项目中任何地方调用此函数获取 logger
    """
    # 这里默认配置，实际项目中建议从 config 读取
    return LogSetup(name=name).get_logger()

logger = get_logger()