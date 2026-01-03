# editor/editor.py

from typing import Tuple
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor


class Editor:
    """
    封裝文字編輯區，提供統一 API：
    - get_text / set_text
    - insert_text
    - replace_range
    - cursor 位置取得與設定
    - 未來可掛 AST / DocumentModel / AI 操作
    """

    def __init__(self, text_widget: QTextEdit) -> None:
        """
        text_widget: 目前實際畫面上的 QTextEdit 實例
        """
        self._text_widget = text_widget

        # 將來如果要加：
        # self._document_model = None
        # self._ast = None
        # 都可以掛在這裡

    # ---------- 基本文字操作 ----------

    def get_text(self) -> str:
        """取得目前全文字內容。"""
        return self._text_widget.toPlainText()

    def set_text(self, text: str) -> None:
        """覆寫全文字內容。"""
        self._text_widget.setPlainText(text)

    def insert_text(self, text: str) -> None:
        """在目前游標位置插入文字。"""
        cursor = self._text_widget.textCursor()
        cursor.insertText(text)
        self._text_widget.setTextCursor(cursor)

    def clear(self) -> None:
        """清除所有內容。"""
        self._text_widget.clear()

    # ---------- 範圍操作（未來 AI patch 用） ----------

    def replace_range(self, start: int, end: int, new_text: str) -> None:
        """
        以字元 index [start, end) 取代成 new_text。
        注意：這裡使用「整份文件」的線性 index。
        """
        doc_text = self.get_text()
        start = max(0, min(start, len(doc_text)))
        end = max(start, min(end, len(doc_text)))

        updated = doc_text[:start] + new_text + doc_text[end:]
        self.set_text(updated)

        # 將游標移到新插入文字的結尾
        cursor = self._text_widget.textCursor()
        cursor.setPosition(start + len(new_text))
        self._text_widget.setTextCursor(cursor)

    # ---------- 游標相關 ----------

    def get_cursor_position(self) -> int:
        """回傳游標在全文中的字元位置（0-based）。"""
        cursor = self._text_widget.textCursor()
        return cursor.position()

    def set_cursor_position(self, pos: int) -> None:
        """設定游標在全文中的字元位置。"""
        text_length = len(self.get_text())
        pos = max(0, min(pos, text_length))

        cursor = self._text_widget.textCursor()
        cursor.setPosition(pos)
        self._text_widget.setTextCursor(cursor)

    def get_cursor_line_column(self) -> Tuple[int, int]:
        """
        回傳 (line, column)，0-based。
        這在未來 AI 想說「請在第 10 行插入一段」會很有用。
        """
        cursor = self._text_widget.textCursor()
        pos = cursor.position()

        text = self.get_text()
        line = text.count("\n", 0, pos)
        # 找該行起點
        last_newline_index = text.rfind("\n", 0, pos)
        if last_newline_index == -1:
            col = pos
        else:
            col = pos - last_newline_index - 1

        return line, col

    # ---------- 將來預留的 hook ----------

    def get_qtextedit(self) -> QTextEdit:
        """
        回傳底層的 QTextEdit。
        在需要存取 Qt 原生 API（例如 shortcut、highlight）時使用。
        """
        return self._text_widget

    # 將來可加：
    # def bind_document_model(self, model: DocumentModel): ...
    # def sync_to_model(self): ...
    # def sync_from_model(self): ...
