import os
import sys
import pickle
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
import mysql.connector

class ConfigDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("資料庫設定")
        self.layout = QVBoxLayout(self)

        self.create_form()
        self.create_buttons()
        self.load_config()

    def create_form(self):
        host_label = QLabel("Host:", self)
        self.layout.addWidget(host_label)

        self.host_input = QLineEdit(self)
        self.host_input.setText("localhost")  # 設置預設文字為 localhost
        self.layout.addWidget(self.host_input)

        user_label = QLabel("User:", self)
        self.layout.addWidget(user_label)

        self.user_input = QLineEdit(self)
        self.layout.addWidget(self.user_input)

        password_label = QLabel("Password:", self)
        self.layout.addWidget(password_label)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.password_input)

    def create_buttons(self):
        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_button)

    def load_config(self):
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        config_path = os.path.join(exe_dir, 'config.pickle')
        if os.path.exists(config_path):
            with open(config_path, 'rb') as f:
                config = pickle.load(f)
                self.host_input.setText(config.get('host', 'localhost'))
                self.user_input.setText(config.get('user', ''))
                self.password_input.setText(config.get('password', ''))

    def save_config(self):
        exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
        config_path = os.path.join(exe_dir, 'config.pickle')

        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()

        if not host or not user or not password:
            QMessageBox.warning(self, "警告", "所有字段都需要填写")
            return
        
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            connection.close()
        except mysql.connector.Error as err:
            QMessageBox.warning(self, "錯誤，帳號密碼錯誤or設定錯誤\n", f"無法連接資料庫: {err}")
            return

        config = {
            'host': host,
            'user': user,
            'password': password,
        }

        with open(config_path, 'wb') as f:
            pickle.dump(config, f)

        if os.path.exists(config_path):
            QMessageBox.information(self, "成功", "配置已保存")
        else:
            QMessageBox.warning(self, "错误", "配置保存失败")

        self.accept()