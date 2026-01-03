# executor/python_executor.py

import sys
import traceback
from io import StringIO


class PythonExecutor:
    def __init__(self):
        self.env = {}   # ★ 共享 namespace

    #def run(self, code: str) -> str:
    #    local_env = self.env


    @staticmethod
    def run(code: str) -> str:
        """
        在獨立乾淨的 namespace 執行 Python code。
        回傳 stdout + stderr + exception 結果。
        """

        # 乾淨的環境（每段 code block 都是不相關的）
        local_env = {}

        # 捕捉 stdout / stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        try:
            exec(code, {}, local_env)   # ★ 乾淨 sandbox：global={}, local=local_env
        except Exception:
            err = traceback.format_exc()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            return f"Error:\n{err}"

        # 聚合輸出
        out = sys.stdout.getvalue() + sys.stderr.getvalue()

        # 還原
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        return out if out.strip() else "(no output)"
