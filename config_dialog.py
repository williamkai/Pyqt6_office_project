import configparser
from PyQt6.QtWidgets import (
                            QDialog,
                            QVBoxLayout, 
                            QLabel, 
                            QLineEdit, 
                            QPushButton, 
                            QMessageBox
                            )

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
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'database' in config:
            self.host_input.setText(config.get('database', 'host', fallback='localhost'))
            self.user_input.setText(config.get('database', 'user', fallback=''))
            self.password_input.setText(config.get('database', 'password', fallback=''))
        else:
            self.host_input.setText('localhost')

    def save_config(self):
        host = self.host_input.text()
        user = self.user_input.text()
        password = self.password_input.text()

        if not host or not user or not password:
            QMessageBox.warning(self, "警告", "所有字段都需要填写")
            return

        config = configparser.ConfigParser()
        config['database'] = {
            'host': host,
            'user': user,
            'password': password,
        }
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        QMessageBox.information(self, "成功", "配置已保存")
        self.accept()

