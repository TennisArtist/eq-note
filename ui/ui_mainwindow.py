# ui/ui_mainwindow.py
if __name__ == "__main__":
    raise RuntimeError("請執行 main.py，而不是 ui_mainwindow.py")


from executor.python_executor import PythonExecutor
from document.element import PythonElement
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
    QWidget, QTextEdit, QPushButton, QFileDialog, QMessageBox, QMenu,
    QSplitter, QShortcut
)
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
import sys
import os
from ui.formula_menu_standard import create_formula_menu
from renderer.html_renderer import HtmlRenderer  # ★ 新增：統一處理 Markdown + LaTeX + Plot 渲染
from document.controller import DocumentController
from PyQt5.QtWebChannel import QWebChannel
from ui.web_bridge import WebBridge   # 你需要新增這個檔案

class SmartMathNote(QMainWindow):
    """
    EQ-Note v2：精簡版主視窗

    重要變化：
    - 不再在 UI 內部處理 LaTeX 預處理與 plot_* 指令解析
    - 將「文字 → HTML」與各種繪圖指令轉換，統一交給 HtmlRenderer
    - UI 只負責：
        * 建立元件與布局
        * 處理按鈕 / 快捷鍵事件
        * 檔案開啟 / 儲存 / PDF 匯出
        * 切換主題
    """

    def __init__(self):
        super().__init__()

        # === 視窗基本設定 ===
        self.setWindowTitle("新筆記 - EQ-Note　by Cheng Yung-Yin")
        self.setWindowIcon(QIcon("icon_eqnote8.png"))
        self.resize(1200, 700)
        self.current_file = None
        self.is_dark = True

        # === 渲染器（負責 Markdown + LaTeX + Plot → HTML） ===
        self.html_renderer = HtmlRenderer(dark_mode=self.is_dark)

        # 注意：真正的 editor 由 main.py 注入
        # self.editor = None

        # ======================================================
        # ① 先建立「左側所有元件」（一定要先有）
        # ======================================================

        # --- 文字輸入區 ---
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText(
            "輸入 Markdown + LaTeX，例如：\n\n"
            "$$\n"
            "\\vec{a}\\times\\vec{b} = "
            "\\begin{bmatrix}"
            "a_y b_z - a_z b_y\\\\\\ "
            "a_z b_x - a_x b_z\\\\\\ "
            "a_x b_y - a_y b_x"
            "\\end{bmatrix}\n"
            "$$"
        )
        self._apply_textedit_theme()

        # Controller
        self.document_controller = DocumentController(self.html_renderer)

        # --- 按鈕 ---
        self.btn_new = QPushButton("🆕")
        self.btn_open = QPushButton("📂")
        self.btn_save = QPushButton("💾")
        self.btn_save_as = QPushButton("📝")
        self.btn_export_pdf = QPushButton("🖨")
        self.btn_insert_formula = QPushButton("🧮")
        self.btn_insert_greek = QPushButton("Ω")
        self.btn_insert_img = QPushButton("📷")
        self.btn_toggle_theme = QPushButton("🌙")
        self.btn_refresh = QPushButton("🔄")

        all_buttons = [
            self.btn_new, self.btn_open, self.btn_save, self.btn_save_as,
            self.btn_export_pdf,
            self.btn_insert_formula, self.btn_insert_greek, self.btn_insert_img,
            self.btn_toggle_theme, self.btn_refresh
        ]

        for btn in all_buttons:
            btn.setFixedWidth(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #222;
                    color: #ccc;
                    border: 1px solid #555;
                    font-size: 14pt;
                    padding: 4px;
                }
                QPushButton:hover {
                    background-color: #333;
                    color: white;
                }
            """)

        button_row = QHBoxLayout()
        button_row.addStretch()
        for btn in all_buttons:
            button_row.addWidget(btn)

        # ======================================================
        # ② 右側預覽區（也要先建立）
        # ======================================================

        self.preview = QWebEngineView()

        self.channel = QWebChannel(self.preview.page())
        self.bridge = WebBridge(self.document_controller)
        self.channel.registerObject("bridge", self.bridge)
        self.preview.page().setWebChannel(self.channel)

        # ======================================================
        # ③ 左側 widget（把 text_input + button_row 組起來）
        # ======================================================

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.addWidget(self.text_input, 1)
        left_layout.addLayout(button_row, 0)

        # ======================================================
        # ④ Splitter（關鍵）
        # ======================================================

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(left_widget)
        self.splitter.addWidget(self.preview)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)

        self.setCentralWidget(self.splitter)

        # ======================================================
        # ⑤ 功能綁定
        # ======================================================

        self.btn_new.clicked.connect(self.new_note)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_save_as.clicked.connect(self.save_as_file)
        self.btn_export_pdf.clicked.connect(self.export_pdf)
        self.btn_insert_formula.clicked.connect(self.insert_formula_menu)
        self.btn_insert_greek.clicked.connect(self.insert_greek_symbol)
        self.btn_insert_img.clicked.connect(self.insert_image)
        self.btn_toggle_theme.clicked.connect(self.toggle_theme)
        self.btn_refresh.clicked.connect(self.update_preview)

        # === 快捷鍵：Ctrl+R 更新預覽 ===
        self.text_input.setFocus()
        self.text_input.installEventFilter(self)

        # === Tooltip ===
        self.btn_new.setToolTip("建立新筆記")
        self.btn_open.setToolTip("開啟筆記")
        self.btn_save.setToolTip("儲存筆記")
        self.btn_save_as.setToolTip("另存新檔")
        self.btn_export_pdf.setToolTip("匯出為 PDF")
        self.btn_insert_formula.setToolTip("插入公式選單")
        self.btn_insert_greek.setToolTip("插入希臘符號")
        self.btn_insert_img.setToolTip("插入圖片")
        self.btn_toggle_theme.setToolTip("切換黑/白主題")
        self.btn_refresh.setToolTip("手動重新整理預覽")

        # ======================================================
        # ⑥ Reading mode 狀態 + 快捷鍵
        # ======================================================

        self.reading_mode = False
        self._editor_width_backup = None

        QShortcut(
            QKeySequence("Ctrl+\\"),
            self,
            activated=self.toggleReadingMode
        )

        # 在 __init__ 最後（QMessageBox 之後或之前都可）
        self.update_preview()

        # === 啟動訊息 ===
        QMessageBox.information(
            self,
            "EQ-Note 啟動",
            "本軟體由 Cheng Yung-Yin 開發。\n© 2025 All rights reserved."
        )

    # ------------------------------------------------------------------
    #  主題 / 外觀
    # ------------------------------------------------------------------

    def toggleReadingMode(self):
        self.reading_mode = not self.reading_mode

        left = self.splitter.widget(0)
        right = self.splitter.widget(1)

        if self.reading_mode:
            self._editor_width_backup = self.splitter.sizes()[0]
            self._was_maximized = self.isMaximized()  # 記住原本是否最大化

            left.hide()
            self.splitter.setSizes([0, 1])

            # 可選：進入閱讀模式時自動最大化視窗（很多人愛）
            # self.showMaximized()

            self.preview.setFocus()
            self.setWindowTitle(self.windowTitle() + "  [閱讀模式]")

        else:
            left.show()

            total = self.splitter.width()
            editor_w = self._editor_width_backup or total // 2
            preview_w = max(200, total - editor_w)

            self.splitter.setSizes([editor_w, preview_w])

            # 如果原本不是最大化，恢復正常大小（視需求）
            # if not self._was_maximized:
            #     self.showNormal()

            self.text_input.setFocus()
            # 移除 [閱讀模式] 標籤
            title = self.windowTitle().replace("  [閱讀模式]", "")
            self.setWindowTitle(title)

    def _apply_textedit_theme(self):
        """依照 self.is_dark 套用輸入區樣式。"""
        if self.is_dark:
            self.text_input.setStyleSheet("""
                QTextEdit {
                    background-color: #111;
                    color: #EEE;
                    font-family: Consolas, monospace;
                    font-size: 14pt;
                    border: none;
                    padding: 10px;
                }
            """)
        else:
            self.text_input.setStyleSheet("""
                QTextEdit {
                    background-color: #fff;
                    color: #000;
                    font-family: Consolas, monospace;
                    font-size: 14pt;
                    border: none;
                    padding: 10px;
                }
            """)

    def toggle_theme(self):
        """切換黑/白主題，並通知 HtmlRenderer 更新樣式。"""
        self.is_dark = not self.is_dark
        self.btn_toggle_theme.setText("☀️" if not self.is_dark else "🌙")
        self._apply_textedit_theme()

        # 通知渲染器更新主題狀態
        self.html_renderer.dark_mode = self.is_dark
        self.html_renderer.plot_renderer.dark_mode = self.is_dark

        # 重新渲染預覽
        self.update_preview()

    # ------------------------------------------------------------------
    #  預覽渲染
    # ------------------------------------------------------------------

    def update_preview(self):
        # 1. 從 Editor 取得文字
        # raw_text = self.editor.get_text()
        raw_text = self.text_input.toPlainText()

        # print("PREVIEW: start")

        # 2. 先交給 Parser → DocumentModel
        doc_model = self.document_controller.parse_text(raw_text)
        # print("PREVIEW: after parse")

        # 3. 渲染器 + 執行 python block 都交給 controller
        html, base_url = self.document_controller.render_with_execution(doc_model)
        # print("PREVIEW: after render_with_execution")

        # 4. 顯示
        self.preview.setHtml(html, base_url)
        # print("PREVIEW: after setHtml")

    # ------------------------------------------------------------------
    #  插入/選單相關
    # ------------------------------------------------------------------

    def insert_formula_menu(self):
        """顯示公式選單，回呼 insert_formula_text 插入選擇的 LaTeX 字串。"""
        menu = create_formula_menu(self, self.insert_formula_text)
        menu.exec_(self.btn_insert_formula.mapToGlobal(self.btn_insert_formula.rect().bottomLeft()))

    def insert_formula_text(self, latex_str: str):
        """由公式選單回呼，將 LaTeX 字串插入文字區。"""
        self.text_input.insertPlainText(latex_str + "\n")
        self.update_preview()

    def insert_greek_symbol(self):
        """顯示希臘字母選單。"""
        menu = QMenu(self)
        greek = [
            ("α", "\\alpha"), ("β", "\\beta"), ("γ", "\\gamma"),
            ("δ", "\\delta"), ("ε", "\\epsilon"), ("θ", "\\theta"),
            ("λ", "\\lambda"), ("μ", "\\mu"), ("π", "\\pi"),
            ("σ", "\\sigma"), ("φ", "\\phi"), ("ω", "\\omega")
        ]
        for symbol, code in greek:
            menu.addAction(f"{symbol}   ({code})", lambda c=code: self.insert_symbol(c))
        menu.exec_(self.btn_insert_greek.mapToGlobal(self.btn_insert_greek.rect().bottomLeft()))

    def insert_symbol(self, code: str):
        """把 \\alpha 類的符號插入為 $\\alpha$ 型式。"""
        self.text_input.insertPlainText(f"${code}$")
        self.update_preview()

    def insert_image(self):
        """插入 <img src="..."> 標籤（相對路徑）。"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "選擇圖片",
            "",
            "Images (*.png *.jpg *.jpeg *.gif)"
        )
        if path:
            rel_path = os.path.relpath(path, os.getcwd()).replace("\\", "/")
            self.text_input.insertPlainText(f"<img src=\"{rel_path}\" width=\"400\">\n")
            self.update_preview()

    # ------------------------------------------------------------------
    #  檔案相關
    # ------------------------------------------------------------------

    def new_note(self):
        """建立新筆記，重設狀態。"""
        confirm = QMessageBox.question(
            self,
            "建立新筆記",
            "確定要建立新筆記嗎？未儲存的內容將會遺失。",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        self.current_file = None
        self.text_input.clear()
        self.setWindowTitle("新筆記 - EQ-Note　by Cheng Yung-Yin")

        template = "# 新筆記\n\n輸入 Markdown + LaTeX，例如：\n\n$$E = mc^2$$"
        self.text_input.setPlainText(template)
        self.update_preview()

    def save_file(self):
        """儲存目前檔案，若尚未有路徑則詢問儲存位置。"""
        if not self.current_file:
            path, _ = QFileDialog.getSaveFileName(
                self,
                "儲存筆記",
                "",
                "Markdown (*.md);;Text Files (*.txt)"
            )
            if not path:
                return
            self.current_file = path

        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(self.text_input.toPlainText())

        self.setWindowTitle(f"{os.path.basename(self.current_file)} - EQ-Note　by Cheng Yung-Yin")
        QMessageBox.information(self, "已儲存", f"已存檔至：\n{self.current_file}")

    def save_as_file(self):
        """另存新檔，並將檔名自動加為標題（若原文沒有 # 開頭）。"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "另存新檔",
            "",
            "Markdown (*.md);;Text Files (*.txt)"
        )
        if not path:
            return

        self.current_file = path
        filename = os.path.basename(path)
        title = os.path.splitext(filename)[0]

        text = self.text_input.toPlainText().strip()
        if not text.startswith("#"):
            text = f"# {title}\n\n" + text

        with open(self.current_file, "w", encoding="utf-8") as f:
            f.write(text)

        self.text_input.setPlainText(text)
        self.setWindowTitle(f"{filename} - EQ-Note　by Cheng Yung-Yin")
        QMessageBox.information(self, "另存成功", f"已另存至：\n{self.current_file}")

    def open_file(self):
        """開啟現有 Markdown / 文字檔。"""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "開啟筆記",
            "",
            "Markdown (*.md);;Text Files (*.txt)"
        )
        if not path:
            return

        with open(path, "r", encoding="utf-8") as f:
            self.text_input.setPlainText(f.read())

        self.current_file = path
        self.setWindowTitle(f"{os.path.basename(self.current_file)} - EQ-Note　by Cheng Yung-Yin")
        self.update_preview()

    def export_pdf(self):
        """將右側 WebEngineView 內容匯出為 PDF。"""
        path, _ = QFileDialog.getSaveFileName(
            self,
            "匯出 PDF",
            "",
            "PDF Files (*.pdf)"
        )
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"

        self.preview.page().printToPdf(path)
        QMessageBox.information(self, "匯出成功", f"PDF 已輸出至：\n{path}")

    # ------------------------------------------------------------------
    #  事件過濾（快捷鍵）
    # ------------------------------------------------------------------

    def eventFilter(self, obj, event):
        """攔截 Ctrl+R，做為『更新預覽』快捷鍵。"""
        if obj == self.text_input and event.type() == event.KeyPress:
            if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_R:
                self.update_preview()
                QMessageBox.information(self, "已更新", "手動更新預覽完成。")
                return True  # 阻止事件繼續傳遞

        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SmartMathNote()
    win.show()
    sys.exit(app.exec_())
