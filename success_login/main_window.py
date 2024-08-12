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
         
from success_login.user_information_widget import UserInformationWidget
from success_login.database_widget.database_widget import DatabaseWidget
from data_access_object.user_database import UserDatabase  # 引入用戶專屬的資料庫類
from success_login.email_widget.email_widget import EmailWidget
class MainWindow(QWidget):
    
    logout_signal = pyqtSignal()
    
    def __init__(self, parent=None, user_email=None):
        super(MainWindow, self).__init__(parent) 
        self.database =  UserDatabase(user_email)   # 這邊或創建登入成功使用者的資料庫、跟第一層的帳戶資料

        self.user_email = user_email
        self.database_window=None
        self.account_window = None 
        self.email_window = None
        self.database.product_list_dao.create_product_list_table()
        self.database.inventory_dao.create_inventory_table()

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
        if self.email_window is None:
            self.email_window = EmailWidget(self)
            self.email_window.closed.connect(self.on_email_window_closed)
            self.email_window.show()
        else:
            QMessageBox.information(self, "阿肥之力", "信箱處理功能視窗已經開啟了喔！")

    def on_email_window_closed(self):
        self.email_window = None


    def open_database_window(self):
        if self.database_window is None:
            self.database_window = DatabaseWidget(None, database=self.database)
            self.database_window.closed.connect(self.on_database_window_closed)  # 連接窗口關閉訊號
            self.database_window.show()
        else:
            QMessageBox.information(self, "阿肥之力", "資料庫功能已經開啟了喔！")
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
        # 檢查並關閉資料庫視窗
        if self.database_window is not None:
            self.database_window.close()
            self.database_window = None

        # 檢查並關閉帳戶設定視窗
        if self.account_window is not None:
            self.account_window.close()
            self.account_window = None
        
        if self.email_window is not None:  # 關閉信箱視窗
            self.email_window.close()
            self.email_window = None
        
        # 關閉資料庫連接
        if self.database.connection is not None:
            self.database.cursor.close()  # 關閉cursor
            self.database.connection.close()  # 關閉資料庫連接
            print("資料庫連接已關閉")

        # 在這裡你可以加入其他需要關閉的視窗(之後其他功能視窗就要加進來)
        QMessageBox.information(self, "登出", "已登出")
        self.logout_signal.emit()  # 發射登出信號
    def handle_main_window_close(self):
        # 關閉所有打開的子視窗
        if self.database_window is not None:
            self.database_window.close()
            self.database_window = None

        if self.account_window is not None:
            self.account_window.close()
            self.account_window = None
        
        if self.email_window is not None:  # 關閉信箱視窗
            self.email_window.close()
            self.email_window = None

        # 關閉資料庫連接
        if self.database.connection is not None:
            self.database.cursor.close()
            self.database.connection.close()
            print("資料庫連接已關閉")
