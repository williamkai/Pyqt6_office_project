import sys
import os
import pickle
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
                            QWidget, 
                            QVBoxLayout, 
                            QLabel,  
                            QLineEdit, 
                            QPushButton,
                            QMessageBox
                            )

from database.database import Database
from login.register_widget import RegisterWidgetWindow
from login.config_dialog import ConfigDialog

 
'''
主要來處理第一步驟的畫面，就是登入畫面
有帳號密碼、登入跟註冊
邏輯上就是創建class時候，把畫面上顯示的原件都創出來，然後設定布局
在__init__中有一個追蹤註冊帳戶窗口的
目的是因為我打開註冊窗口後，避免重複打開註冊視窗

'''

class LoginWidget(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        self.database=Database()
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.register_window = None  # 追蹤註冊帳戶窗口
        self.create_login_form()
        self.create_register_button()
        self.create_config_button()  # 创建配置按钮

    def create_login_form(self):
        self.user_label = QLabel("", self)
        font = self.user_label.font()
        font.setPointSize(12)
        self.user_label.setFont(font)
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.user_label)

        email_label = QLabel("帳號:", self)
        font = email_label.font()
        font.setPointSize(12)
        email_label.setFont(font)
        email_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(email_label)

        self.email_input = QLineEdit(self)
        self.email_input.setFixedSize(200, 30)
        self.layout.addWidget(self.email_input)

        self.email_input.textChanged.connect(self.check_username)

        password_label = QLabel("密碼:", self)
        font = password_label.font()
        font.setPointSize(12)
        password_label.setFont(font)
        password_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedSize(200, 30)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("登入", self)
        self.login_button.clicked.connect(self.login)
        self.login_button.setDefault(True)
        self.login_button.setFixedSize(200, 40)
        self.layout.addWidget(self.login_button)
        
        self.email_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def create_register_button(self):
        self.register_button = QPushButton("註冊帳戶", self)
        self.register_button.clicked.connect(self.open_register_window)
        self.register_button.setFixedSize(200, 40)
        self.layout.addWidget(self.register_button)

    def create_config_button(self):
        self.config_button = QPushButton("設定資料庫", self)
        self.config_button.clicked.connect(self.open_config_window)
        self.config_button.setFixedSize(200, 40)
        self.layout.addWidget(self.config_button)

    def is_config_valid(self):
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        config_path = os.path.join(exe_dir, 'config.pickle')

        if not os.path.exists(config_path):
            return False

        try:
            with open(config_path, 'rb') as f:
                config = pickle.load(f)
                if 'host' not in config or not config['host']:
                    return False
                if 'user' not in config or not config['user']:
                    return False
                if 'password' not in config or not config['password']:
                    return False
        except (pickle.UnpicklingError, FileNotFoundError, EOFError, KeyError):
            return False

        return True

    def check_username(self):
        username = self.email_input.text()
        if username:
            if not self.is_config_valid():
                print("配置文件不存在或不完整")
                return
            else:
                # 檢查 Database 物件的 connection 和 cursor
                if self.database.connection is None or self.database.cursor is None:
                    self.database.initialize()
                query = "SELECT name FROM users WHERE username = %s"
                self.database.cursor.execute(query, (username,))
                result = self.database.cursor.fetchone()
                if result:
                    self.user_label.setText(f"{result[0]}")
                else:
                    self.user_label.setText("")
        else:
            self.user_label.setText("")

    def login(self):
        if not self.is_config_valid():
            QMessageBox.warning(self, "警告", "請先設定資料庫")
            return
        email = self.email_input.text()
        password = self.password_input.text()

         # 只有在連接和游標為 None 時才初始化
        if self.database.connection is None or self.database.cursor is None:
            self.database.initialize()

        # 从数据库验证用户凭据
        result = self.database.validate_user(email, password)
        if isinstance(result, bool):
            if result:
                print("登入成功")
                # 登录成功后关闭数据库连接
                self.database.close()
                QMessageBox.warning(self, "肥肥力量", "登入成功")
                self.login_success.emit(email)  # 發送登入成功的訊號
            else:
                QMessageBox.warning(self, "肥肥力量", "密碼錯誤")
                print("密碼錯誤")
        else:
            QMessageBox.warning(self, "肥肥力量", result)
            print(result)

    def open_register_window(self):
        if not self.is_config_valid():
            QMessageBox.warning(self, "警告", "請先設定資料庫")
            return
        
        if self.register_window is None:
            self.register_window = RegisterWidgetWindow(self)
            self.register_window.finished.connect(self.on_register_window_closed)
            self.register_window.show()
        else:
            QMessageBox.information(self, "阿肥之力", "註冊視窗已經開啟了喔！")

    def on_register_window_closed(self):
        self.register_window = None

    def open_config_window(self):
        config_dialog = ConfigDialog(self)
        config_dialog.exec()
