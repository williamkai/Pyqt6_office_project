# longin_widget.py

# 標準庫導入
import sys
import os
import pickle

# 第三方庫導入
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

# 本地模塊導入
from data_access_object.database import Database
from login.register_widget import RegisterWidgetWindow
from login.config_dialog import ConfigDialog

class LoginWidget(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.database = Database()
        self.register_window = None  # 追蹤註冊帳號窗口

        # 初始化視窗和創建元件
        self.init_window()
        self.create_widgets()

    def init_window(self):
        """初始化視窗屬性"""
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_widgets(self):
        """建立並配置視窗中的元件"""
        self.create_login_form()      # 建立登入畫面的標籤、輸入框、按鈕
        self.create_register_button()  # 建立註冊按鈕
        self.create_config_button()    # 建立資料庫設定按鈕

    def create_login_form(self):
        """建立登入表單"""
        self.user_label = QLabel(self)
        self.set_label_properties(self.user_label, "", 12)

        email_label = QLabel(self)
        self.set_label_properties(email_label, "帳號:", 12)

        self.email_input = QLineEdit(self)
        self.email_input.setFixedSize(200, 30)
        self.layout.addWidget(self.email_input)
        self.email_input.textChanged.connect(self.check_username)

        password_label = QLabel(self)
        self.set_label_properties(password_label, "密碼:", 12)

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

    def set_label_properties(self, label, text, font_size):
        """設置標籤的文字、字體大小和對齊方式"""
        label.setText(text)
        font = label.font()
        font.setPointSize(font_size)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(label)

    def create_register_button(self):
        """建立註冊按鈕"""
        self.register_button = QPushButton("註冊帳戶", self)
        self.register_button.clicked.connect(self.open_register_window)
        self.register_button.setFixedSize(200, 40)
        self.layout.addWidget(self.register_button)

    def create_config_button(self):
        """建立資料庫設定按鈕"""
        self.config_button = QPushButton("設定資料庫", self)
        self.config_button.clicked.connect(self.open_config_window)
        self.config_button.setFixedSize(200, 40)
        self.layout.addWidget(self.config_button)

    def is_config_valid(self):
        """檢查資料庫配置是否有效"""
        exe_dir = (
            os.path.dirname(sys.executable) if getattr(sys, 'frozen', False)
            else os.path.dirname(__file__)
        )
        config_path = os.path.join(exe_dir, 'config.pickle')

        if not os.path.exists(config_path):
            return False

        try:
            with open(config_path, 'rb') as f:
                config = pickle.load(f)
                return all(key in config and config[key] for key in ['host', 'user', 'password'])
        except (pickle.UnpicklingError, FileNotFoundError, EOFError, KeyError):
            return False

    def check_username(self):
        """檢查使用者名稱是否有效"""
        username = self.email_input.text()
        if username:
            if not self.is_config_valid():
                print("設定檔不存在或不完整")
                return
            if self.database.connection is None or self.database.cursor is None:
                self.database.initialize()
            query = "SELECT name FROM users WHERE username = %s"
            self.database.cursor.execute(query, (username,))
            result = self.database.cursor.fetchone()
            self.user_label.setText(result[0] if result else "")
        else:
            self.user_label.setText("")

    def login(self):
        """執行登入操作"""
        if not self.is_config_valid():
            QMessageBox.warning(self, "警告", "請先設定資料庫")
            return

        email = self.email_input.text()
        password = self.password_input.text()

        if self.database.connection is None or self.database.cursor is None:
            self.database.initialize()

        result = self.database.validate_user(email, password)
        if isinstance(result, bool):
            QMessageBox.information(self, "肥肥力量", "登入成功")
            self.login_success.emit(email)
        else:
            QMessageBox.warning(self, "肥肥力量", result)

        self.database.close()

    def open_register_window(self):
        """開啟註冊視窗"""
        if not self.is_config_valid():
            QMessageBox.warning(self, "警告", "請先設定資料庫資料")
            return

        if self.register_window is None:
            self.register_window = RegisterWidgetWindow(self)
            self.register_window.finished.connect(self.on_register_window_closed)
            self.register_window.show()
        else:
            QMessageBox.information(self, "阿肥之力", "註冊視窗已經開啟了喔！")

    def on_register_window_closed(self):
        """註冊視窗關閉時的處理"""
        self.register_window = None

    def open_config_window(self):
        """開啟設定視窗"""
        config_dialog = ConfigDialog(self)
        config_dialog.exec()

