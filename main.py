# main.py
import sys
from PyQt5.QtWidgets import QApplication

from ui.ui_mainwindow import SmartMathNote
from editor import Editor


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 建立主視窗
    win = SmartMathNote()

    # ★ 新增：建立 Editor 抽象層
    #   win.text_input 是 SmartMathNote 裡的 QTextEdit
    win.editor = Editor(win.text_input)

    win.show()
    sys.exit(app.exec_())
