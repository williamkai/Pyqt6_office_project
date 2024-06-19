from PyQt6.QtCore import (Qt,
                          pyqtSignal
                          )
from PyQt6.QtWidgets import (
                            QMainWindow, 
                            QVBoxLayout, 
                            QPushButton, 
                            QWidget, 
                            QMessageBox
                            )          
         
from user_information_widget import UserInformationWidget
from database_widget import DatabaseWidget

class MainWindow(QWidget):
    
    logout_signal = pyqtSignal(str)
    
    def __init__(self, parent=None, database=None, user_email=None):
        super().__init__(parent)   
        self.database = database

        self.user_email = user_email
        self.database_window=None
        self.account_window = None 

        # 設定布局
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 設定本來窗口的標題
        if parent:
            parent.setWindowTitle("成功登入啦!!!肥之凱凱的程式")

        # 創立按鈕
        self.create_buttons()

    def create_buttons(self):
        self.email_button = QPushButton("信箱處理功能", self)
        self.email_button.setFixedSize(200, 40)
        self.email_button.clicked.connect(self.open_email_window)
        self.layout.addWidget(self.email_button)

        self.database_button = QPushButton("庫存資料庫功能", self)
        self.database_button.setFixedSize(200, 40)
        self.database_button.clicked.connect(self.open_database_window)
        self.layout.addWidget(self.database_button)

        self.account_button = QPushButton("設定帳戶資料", self)
        self.account_button.setFixedSize(200, 40)
        self.account_button.clicked.connect(self.open_account_window)
        self.layout.addWidget(self.account_button)

        self.logout_button = QPushButton("登出", self)
        self.logout_button.setFixedSize(200, 40)
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

    def open_email_window(self):
        QMessageBox.information(self, "信箱處理功能", "打开信箱處理功能窗口")


    def open_database_window(self):
        if self.database_window is None:
            self.database_window = DatabaseWidget(None, database=self.database)
            self.database_window.closed.connect(self.on_database_window_closed)  # 连接窗口关闭信号
            self.database_window.show()
        else:
            print("資料庫功能視窗已經開啟")

    def on_database_window_closed(self):
        self.database_window = None
        print("資料庫功能視窗已經關閉")

    def open_account_window(self):
        if self.account_window is None:
            self.account_window = UserInformationWidget(self)
            self.account_window.finished.connect(self.on_account_window_closed)
            self.account_window.show()
        else:
            QMessageBox.information(self, "阿肥之力", "帳戶資料視窗已經開啟了喔！")

    def on_account_window_closed(self):
        self.account_window = None

    def logout(self):
        QMessageBox.information(self, "登出", "已登出")
        self.logout_signal.emit()  # 发射登出信号