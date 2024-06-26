from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QMessageBox)


class UserInformationWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.database = parent.database
        self.setWindowTitle("帳戶基本資料")
        self.setFixedSize(400, 300)  # 設定固定大小            
        self.init_ui()  # 使用絕對佈局
        

    def init_ui(self):
        # 創建標籤和輸入框
        labels = ("信箱功能帳號:", "密碼:", "再次確認密碼:")
        positions = [(50, 30), (50, 80), (50, 130), (50, 180)]  # 固定位置 (x, y)
        self.inputs = {}

        for idx, label_text in enumerate(labels):
            x, y = positions[idx]

            label = QLabel(label_text, self)
            label.setGeometry(x, y, 100, 30)  # 設定標籤的固定位置和大小 (x, y, width, height)
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)

            input_widget = QLineEdit(self)
            input_widget.setGeometry(x + 120, y, 200, 30)  # 設定輸入框的固定位置和大小 (x + offset, y, width, height)
            if "密碼" in label_text:
                input_widget.setEchoMode(QLineEdit.EchoMode.Password)
            self.inputs[label_text] = input_widget

        # 創建註冊按鈕
        self.register_button = QPushButton("設定", self)
        self.register_button.setGeometry(150, 230, 100, 40)  # 設定按鈕的固定位置和大小 (x, y, width, height)
        self.register_button.clicked.connect(self.register)

    def register(self):
        username = self.inputs["信箱功能帳號:"].text()
        password = self.inputs["密碼:"].text()
        confirm_password = self.inputs["再次確認密碼:"].text()

        # 檢查是否有空值
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "錯誤", "請輸入基本資料！")
            return
        
        # 檢查密碼是否匹配
        if password != confirm_password:
            QMessageBox.warning(self, "錯誤", "兩次輸入的密碼不一致！")
            return

        # 將資料寫進資料庫
        if self.database.insert_user_account(username, password):
            QMessageBox.information(self, "成功", "帳戶資料寫入成功！")
            self.close()
        else:
            QMessageBox.warning(self, "錯誤", "資料寫入出錯！")

    def closeEvent(self, event):
        super().closeEvent(event)
