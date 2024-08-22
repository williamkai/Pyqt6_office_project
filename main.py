import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import pyqtSignal
from login.login_widget import LoginWidget 
from success_login.main_window import MainWindow

'''
我寫的第一支GUI程式，希望可以做好，這邊是運行的主程式
各種功能都是載入到這邊執行，這樣試算物件導向嗎?吧?
畢竟我是門外漢，都是自己蝦亂研究的，連code的整潔也是慢慢研究
不知道這樣寫的行不行；另外感謝GPT哈哈哈。

這邊程序主要就是載入登入的class，讓畫面變成登入畫面。
登入的畫面邏輯跟布局我就寫在等入的clss了
'''
class MainApplication(QMainWindow):
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("努力減肥阿凱寫的程式~嗄~~~哈!!!!")
        self.setMinimumSize(400, 300)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # 初始化登入畫面
        self.login_widget = LoginWidget()
        self.layout.addWidget(self.login_widget)

        # 建立登入class的訊號
        self.login_widget.login_success.connect(self.show_main_window)

        # 初始化變數儲存位子(資料庫、跟使用者)
        self.database = None
        self.current_user = None
        self.main_window = None  # 初始化 main_window 為 None

    def switch_widget(self, old_widget, new_widget):
        """切換顯示的 widget"""
        if old_widget:
            self.layout.removeWidget(old_widget)
            old_widget.deleteLater()
        self.layout.addWidget(new_widget)

    def show_main_window(self, user_email):
        self.current_user = user_email
        self.main_window = MainWindow(self, self.current_user)  # 初始化 main_window
        self.main_window.logout_signal.connect(self.show_login_widget)  # 連接登出信號
        self.switch_widget(self.login_widget, self.main_window)

    def show_login_widget(self):
        self.login_widget = LoginWidget(self)  # 確保創建新的 LoginWidget
        self.login_widget.login_success.connect(self.show_main_window)  # 連接信號
        self.switch_widget(self.main_window, self.login_widget)  # 使用 self.main_window

    def closeEvent(self, event):
        self.close_signal.emit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec())
