import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget

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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("努力減肥阿凱寫的程式~嗄~~~哈!!!!")
        self.setMinimumSize(800, 600)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # 初始化登入畫面
        self.login_widget = LoginWidget()
        self.layout.addWidget(self.login_widget)

        # 連接登入成功的畫面
        self.login_widget.login_success.connect(self.show_main_window)

        # 初始化資料庫
        self.database = None
        self.current_user = None

    def show_main_window(self, user_email):
        # 移除登入畫面物件
        self.database=self.login_widget.database
        self.current_user = user_email

        self.layout.removeWidget(self.login_widget)
        self.login_widget.deleteLater()

        # 創建登入成功的Class跟轉換畫面
        self.main_window = MainWindow(self, self.database, self.current_user)
        self.layout.addWidget(self.main_window)
         # 连接主窗口的登出信号到处理槽
        # self.main_window.logout_signal.connect(self.show_login_widget)

    def show_login_widget(self):
        # 移除主窗口对象
        self.layout.removeWidget(self.main_window)
        self.main_window.deleteLater()

        # 重新添加登录界面对象
        self.login_widget = LoginWidget()
        self.layout.addWidget(self.login_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec())
