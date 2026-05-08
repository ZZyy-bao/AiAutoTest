import time
import functools
from core.logger import logger

def timing(func):
    """
    性能监控装饰器
    打印函数执行的耗时
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 高精度计时
        logger.debug(f"⏳ 开始执行: {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info(f"✅ {func.__name__} 执行完成，耗时: {duration:.2f}秒")
    
    return wrapper