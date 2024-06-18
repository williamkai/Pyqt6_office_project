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


class MainWindow(QWidget):
    
    logout_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # 設定布局
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 設定本來窗口的標題
        if parent:
            parent.setWindowTitle("成功鄧入啦!!!肥之凱凱的程式")

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
        QMessageBox.information(self, "庫存資料庫功能", "打开庫存資料庫功能窗口")

    def open_account_window(self):
        QMessageBox.information(self, "設定帳戶資料", "打开設定帳戶資料窗口")

    def logout(self):
        QMessageBox.information(self, "登出", "已登出")
        self.logout_signal.emit()  # 发射登出信号