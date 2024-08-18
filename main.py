import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtCore import pyqtSignal
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
    close_signal = pyqtSignal()
    
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

        # 建立登入class的訊號
        self.login_widget.login_success.connect(self.show_main_window)

        # 初始化變數儲存位子(資料庫、跟使用者)
        self.database = None
        self.current_user = None

    def show_main_window(self, user_email):
        self.current_user = user_email  # 這個是用來暫存帳號，之後要來創建個別帳號的資料庫用，這樣才可以針對每個帳號有不同商品資料庫等等
        # 移除登入畫面物件
        self.layout.removeWidget(self.login_widget) # 這個是把顯示在登入畫面的物件移除掉，但是這邊的移除，只是顯示上移除，這個物件還是儲存在記憶體中，所以當名子重複layout..或其他因素，會造成顯示錯誤
        self.login_widget.deleteLater() # 這個才是把之前創建出來的登入顯示元件徹底從記憶體中刪除。

        # 創建主視窗並添加到佈局
        self.main_window = MainWindow(self, self.current_user)
        self.layout.addWidget(self.main_window)
        # 連接主視窗的登出信號到處理槽
        self.main_window.logout_signal.connect(self.show_login_widget)
         # 將主視窗的關閉訊號與登錄成功後視窗的清理操作連接
        self.close_signal.connect(self.main_window.handle_main_window_close)


    def show_login_widget(self):
        # 移除主視窗物件
        self.layout.removeWidget(self.main_window)
        self.main_window.deleteLater()

        # 創建登入畫面並添加到佈局
        self.login_widget = LoginWidget(self)
        self.layout.addWidget(self.login_widget)
        # 連接登入畫面的登入信號到處理槽
        self.login_widget.login_success.connect(self.show_main_window)

    def closeEvent(self, event):
        # 發射關閉訊號，通知其他視窗進行清理
        self.close_signal.emit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec())
