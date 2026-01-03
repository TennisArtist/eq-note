# document/controller.py

from document.parser import DocumentParser
from executor.python_executor import PythonExecutor
from document.element import PythonElement


class DocumentController:
    def __init__(self, html_renderer):
        self.parser = DocumentParser()
        self.html_renderer = html_renderer
        self.executor = PythonExecutor()
        self.doc_model = None   # ★ 保存目前的文件模型

    def parse_text(self, raw_text: str):
        self.doc_model = self.parser.parse(raw_text)
        return self.doc_model

    def execute_block(self, elem_id: str) -> str:
        """給 WebChannel 用，只執行一個 block"""
        for elem in self.doc_model.elements:
            if elem.id == elem_id and isinstance(elem, PythonElement):
                out = self.executor.run(elem.code)
                elem.output = out
                return out
        return ""

    # ----------------------------------------------------------
    # ★ 修改重點：先跑完所有 Block，填入 output，再一次 Render
    # ----------------------------------------------------------
    def render_with_execution(self, doc_model):
        """
        1. 遍歷 doc_model，遇到 PythonElement 就執行
        2. 將結果寫入 element.output
        3. 呼叫 render 產生最終 HTML (這時 HTML 就已經包含 output 了)
        """

        # 1) 執行所有 python 區塊
        #    注意：因為我們用同一個 executor，變數狀態會保留 (Jupyter-style)
        for elem in doc_model.elements:
            if isinstance(elem, PythonElement):
                # 執行並獲取字串結果
                result = self.executor.run(elem.code)
                # ★ 存回 element
                elem.output = result if result else "[無輸出]"

        # 2) 轉成 HTML (Render 時會讀取 element.output)
        html, base_url = self.html_renderer.render(doc_model)

        # 3) 不需要再做 replace("</body>") 了，因為結果已經在 inline 裡面
        return html, base_url