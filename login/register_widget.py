from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog, 
                             QLabel, 
                             QLineEdit, 
                             QPushButton, 
                             QMessageBox)


class RegisterWidgetWindow(QDialog):
    """
    感覺寫得不好，但又說不上來
    我這邊我會引用到父那邊創建的class_database
    所以這邊就不會再__init__創建資料庫的class
    這樣也可以避免我在初始化資料庫會再跑一次程序
    這樣可能可以提升效率?
    總之感覺怪怪的又覺得這樣可以。
    
    主要就是創建註冊帳號的視窗
    讓使用者輸入資料然後確認資料無誤
    就寫進資料庫
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.database = parent.database
        self.database.initialize()  # 初始化資料庫連接
        self.setWindowTitle("註冊帳戶")
        self.setFixedSize(400, 300)  # 設定固定大小            
        self.init_ui()  # 使用絕對佈局

    def init_ui(self):
        # 創建標籤和輸入框
        labels = ("使用者名稱:", "帳號:", "密碼:", "再次確認密碼:")
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
        self.register_button = QPushButton("註冊", self)
        self.register_button.setGeometry(150, 230, 100, 40)  # 設定按鈕的固定位置和大小 (x, y, width, height)
        self.register_button.clicked.connect(self.register)

    def register(self):
        name = self.inputs["使用者名稱:"].text()
        username = self.inputs["帳號:"].text()
        password = self.inputs["密碼:"].text()
        confirm_password = self.inputs["再次確認密碼:"].text()

        # 檢查是否有空值
        if not name or not username or not password or not confirm_password:
            QMessageBox.warning(self, "錯誤", "請輸入註冊資料！")
            return
        
        # 檢查用帳號是否已存在
        if self.database.check_username_exists(username):
            QMessageBox.warning(self, "錯誤", "帳號已存在！")
            return

        # 檢查密碼是否匹配
        if password != confirm_password:
            QMessageBox.warning(self, "錯誤", "兩次輸入的密碼不一致！")
            return

        # 將資料寫進資料庫
        if self.database.insert_user(name, username, password):
            QMessageBox.information(self, "成功", "註冊成功！")
            self.close()
        else:
            QMessageBox.warning(self, "錯誤", "註冊失敗！")

    def closeEvent(self, event):
        super().closeEvent(event)
