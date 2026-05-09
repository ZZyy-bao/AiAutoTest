import pandas as pd
from pathlib import Path
from core.logger import logger

class TestCaseLoader:
    @staticmethod
    def load_cases(folder_path):
        """
        读取指定文件夹下的所有 Excel 文件 (.xlsx, .xls) 并合并为一个字典列表
        """
        folder = Path(folder_path)
        
        if not folder.exists():
            raise FileNotFoundError(f"文件夹不存在: {folder_path}")

        all_cases = []
        files_processed = 0

        excel_files = list(folder.rglob("*.xlsx")) + list(folder.rglob("*.xls"))

        valid_files = [f for f in excel_files if not f.name.startswith('~$') and not f.name.startswith('.')]

        if not valid_files:
            logger.info(f"⚠️ 在文件夹中未找到任何 Excel 文件: {folder_path}")
            return []

        logger.info(f"🔍 发现 {len(valid_files)} 个 Excel 文件，开始读取...")

        for file_path in valid_files:
            try:
                df = pd.read_excel(file_path)
                df = df.fillna("")
                cases = df.to_dict(orient='records')
                all_cases.extend(cases)
                
                files_processed += 1
                
            except Exception as e:
                logger.info(f"  ❌ 读取文件失败 {file_path.name}: {e}")

        logger.info(f"✅ 成功加载完成！共处理 {files_processed} 个文件，累计 {len(all_cases)} 条测试用例。")
        return all_cases