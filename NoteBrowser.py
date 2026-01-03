import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("簡單瀏覽器")
        self.setGeometry(100, 100, 1200, 800)

        # 創建網頁視圖
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  # 默認載入首頁

        # 設置主窗口的中心部件
        self.setCentralWidget(self.browser)

        # 創建工具欄
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 後退按鈕
        back_btn = QAction("←", self)
        back_btn.setStatusTip("後退")
        back_btn.triggered.connect(self.browser.back)
        toolbar.addAction(back_btn)

        # 前進按鈕
        forward_btn = QAction("→", self)
        forward_btn.setStatusTip("前進")
        forward_btn.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_btn)

        # 重新載入按鈕
        reload_btn = QAction("↻", self)
        reload_btn.setStatusTip("重新載入")
        reload_btn.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_btn)

        # URL 輸入欄
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("輸入網址並按 Enter")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        # 更新 URL 欄當網頁載入完成
        self.browser.urlChanged.connect(self.update_url_bar)

        # 顯示狀態欄
        self.show()

    def navigate_to_url(self):
        url = self.url_bar.text()
        # 確保 URL 有協議頭
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.browser.setUrl(QUrl(url))

    def update_url_bar(self, qurl):
        self.url_bar.setText(qurl.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    sys.exit(app.exec_())