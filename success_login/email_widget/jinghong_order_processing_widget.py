#jinghong_order_processing_widget.py
import imaplib
import email
import json
import re
from datetime import datetime
from email import message_from_bytes
from email.header import decode_header
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLineEdit, 
                             QListWidget,
                             QTextEdit,
                             QDateEdit,
                             QTimeEdit,
                             QSpacerItem,
                             QSizePolicy,
                             QCheckBox,
                             QLabel,
                             QGroupBox,
                             QListWidgetItem,
                             QFileDialog,
                             QMessageBox)
from PyQt6.QtCore import QDateTime,Qt,QDate, QTime, QEvent,pyqtSignal

from success_login.email_widget.email_search_thread import EmailSearchThread
from success_login.email_widget.jinghong_order_processing_function.order_sorting import OrderSortingThread
from success_login.email_widget.jinghong_order_processing_function.order_sorting_window import OrderSortingWindow
from success_login.email_widget.jinghong_order_processing_function.order_sorting_to_excel_window import OrderSortingToExcelWindow

class JinghongOrderProcessingWidget(QWidget):

    close_signal = pyqtSignal()

    def __init__(self, parent=None, database=None,email=None,password=None):
        super().__init__(parent)
        self.database = database
        self.parent_widget = parent  # 儲存父部件的引用
        self.email = email
        self.password = password
        self.email_list = None  # 初始化爲 None，表示元件尚未建立
        self.email_display = None  # 初始化爲 None，表示元件尚未建立
        self.email_search_layout = None
        self.mail_data =None #放搜尋結果資料的字典
        
        self.order_sorting_window = None  # 否則初始化為 None
        self.order_all_data=None
        self.order_sorting_to_excel_window=None
        self.initialize_ui() 
        
        self.close_signal.connect(self.handle_close)


    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.jinghong_email_processing_widget()

    def jinghong_email_processing_widget(self):
        self.jinghong_email_processing_group_box = QGroupBox("菁弘訂單處理功能", self)
        # 設定 QGroupBox 的尺寸策略
        self.jinghong_email_processing_group_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.button_layout = QHBoxLayout(self.jinghong_email_processing_group_box)

        self.email_search_button = QPushButton("信件查詢")
        self.email_search_button.clicked.connect(self.email_search)
        self.email_search_button.setFixedWidth(150)
        self.button_layout.addWidget(self.email_search_button)
        
        self.order_sorting_button = QPushButton("訂單整理功能")
        self.order_sorting_button.clicked.connect(self.order_sorting)
        self.order_sorting_button.setFixedWidth(150)
        self.button_layout.addWidget(self.order_sorting_button)

        self.sales_details_writing_button = QPushButton("銷貨明細寫入功能")
        self.sales_details_writing_button.clicked.connect(self.order_sorting_to_excel)
        self.sales_details_writing_button.setFixedWidth(150)
        self.button_layout.addWidget(self.sales_details_writing_button)

        self.inventory_deduction_button = QPushButton("庫存扣除功能")
        self.inventory_deduction_button.clicked.connect(self.email_search)
        self.inventory_deduction_button.setFixedWidth(150)
        self.button_layout.addWidget(self.inventory_deduction_button)

        self.main_layout.addWidget(self.jinghong_email_processing_group_box)

        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)

        self.main_layout.addWidget(self.display_area)



    def email_search(self):
        print("建立信件搜尋的功能視窗")
        
        if self.email_search_layout is None:
            self.create_email_search_input_box()
            
        # 如果 email_list 尚未建立，則建立它
        if self.email_list is None:
            self.email_list = QListWidget(self)
            self.email_list.setMinimumHeight(50)
            self.email_list.itemClicked.connect(self.display_email_content)
            self.display_layout.addWidget(self.email_list, 1)
        
        # 如果 email_display 尚未建立，則建立它
        if self.email_display is None:
            self.email_display = QTextEdit(self)
            self.email_display.setReadOnly(True)
            self.email_display.setMinimumHeight(200)
            self.display_layout.addWidget(self.email_display, 5)

    def create_email_search_input_box(self):
        self.email_search_group_box = QGroupBox("信件搜尋條件", self)
        self.email_search_layout = QVBoxLayout(self.email_search_group_box)
        self.date_time_layout = QHBoxLayout()
        self.from_input_layout=QHBoxLayout()
        self.keyword_input_layout=QHBoxLayout()
        self.order_search_layout=QHBoxLayout()
        print("創建信箱收所限制條件輸入框")

        # 添加日期选择器
        self.date_time_label = QLabel("日期/時間:", self)
        self.date_time_layout.addWidget(self.date_time_label)
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        self.date_edit.setDate(datetime.today())
        self.date_edit.setFixedWidth(120)
        self.date_time_layout.addWidget(self.date_edit)
        # 添加時間選擇器
        self.timeedit = QTimeEdit(self)
        self.timeedit.setDisplayFormat('hh:mm:ss')
        self.time = QTime(7, 0, 0)  # 参数依次是小时、分钟、秒
        self.timeedit.setTime(self.time)
        self.timeedit.setFixedWidth(120)
        self.date_time_layout.addWidget(self.timeedit)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.date_time_layout.addItem(spacer_item)
        # self.email_search_layout.addLayout(self.date_time_layout)

        # 添加结束日期选择器
        self.end_date_edit = QDateEdit(self)
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat("yyyy-MM-dd")
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setFixedWidth(120)
        self.date_time_layout.addWidget(QLabel("结束日期:", self))
        self.date_time_layout.addWidget(self.end_date_edit)
        
        # 添加复选框
        self.use_before_checkbox = QCheckBox("使用结束日期作為限制條件", self)
        self.date_time_layout.addWidget(self.use_before_checkbox)
        
        # 添加间隔
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.date_time_layout.addItem(spacer_item)
        
        self.email_search_layout.addLayout(self.date_time_layout)

        # 添加一个 QLineEdit 用于输入 from 地址
        self.from_input_label = QLabel("寄件人:", self)
        self.from_input_layout.addWidget(self.from_input_label)
        self.from_input = QLineEdit(self)
        self.from_input.setPlaceholderText("输入信箱")
        self.from_input.setFixedWidth(150)
        self.from_input_layout.addWidget(self.from_input)

        # 添加一个复选框来选择是否使用 from 地址作为筛选条件
        self.use_from_checkbox = QCheckBox("使用寄件人做篩選條件", self)
        self.from_input_layout.addWidget(self.use_from_checkbox)
        self.email_search_layout.addLayout(self.from_input_layout)
        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.from_input_layout.addItem(spacer_item)

        # 添加关键词输入框及标签
        self.keyword_label = QLabel("内容關鍵字篩選:", self)
        self.keyword_input = QLineEdit(self)
        self.keyword_input.setFixedWidth(200)
        self.keyword_input.setPlaceholderText("输入郵件關鍵詞")
        self.keyword_input.setText("訂單")  # 預設關鍵字
        self.keyword_input_layout.addWidget( self.keyword_label)
        self.keyword_input_layout.addWidget( self.keyword_input)
        self.email_search_layout.addLayout(self.keyword_input_layout)
        
        # 添加選擇資料夾按鈕及顯示資料夾路徑的標籤
        self.folder_label = QLabel("選擇保存資料夾:", self)
        self.folder_path_display = QLineEdit(self)
        self.folder_path_display.setFixedWidth(230)
        self.folder_path_display.setReadOnly(True)
        
        folder_path = self.database.User_basic_information_dao.fetch_user_folder_path()
        if folder_path:
            # 假設 folder_path 是一個元組，例如: ('/path/to/folder',)
            self.folder_path_display.setText(folder_path)
        else:
            self.folder_path_display.setText("未設定路徑")


        self.select_folder_button = QPushButton("選擇資料夾", self)
        self.select_folder_button.setFixedWidth(100)
        self.select_folder_button.clicked.connect(self.open_folder_dialog)
        self.keyword_input_layout.addWidget( self.folder_label)
        self.keyword_input_layout.addWidget( self.folder_path_display)
        self.keyword_input_layout.addWidget( self.select_folder_button)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.keyword_input_layout.addItem(spacer_item)

        # 搜索按鈕
        self.order_search_button = QPushButton("訂單搜索功能", self)
        self.order_search_button.clicked.connect(self.order_search)
        self.order_search_button.setFixedWidth(600)
        self.order_search_layout.addWidget(self.order_search_button)
        self.email_search_layout.addLayout(self.order_search_layout)
        
        # 將 QGroupBox 添加到 display_layout
        self.display_layout.addWidget(self.email_search_group_box, 1)


    """
    這個是信件搜索功能的函式
    是用多線程跑的，這樣可以避免信件還在處理
    但有其他地方的code，同時也需要運行，產生錯誤。
    主要分成第一個是把資訊傳到信件搜索的多線呈去處理
    再傳回兩種資料，一個是信件為一ID，一個是信件的內容(已經轉為文字)，包含標題跟內文
    """
    def order_search(self):
        # 当前日期      #folder_path=self.folder_path_display.text()
        today_date = QDate.currentDate().toString("dd-MMM-yyyy")
        date_str = self.date_edit.date().toString("dd-MMM-yyyy")
        end_date = self.end_date_edit.date().toString("dd-MMM-yyyy")
        keyword = self.keyword_input.text()  # 取得輸入框中的關鍵詞
        from_address = self.from_input.text()
        search_criteria=f'SINCE "{date_str}"'
        # 如果需要使用 BEFORE 条件，添加 BEFORE
        if self.use_before_checkbox.isChecked() and end_date <= today_date:
            search_criteria += f' BEFORE "{self.end_date_edit.date().toString("dd-MMM-yyyy")}"'
        
        # 如果有寄件人地址且复选框选中，添加寄件人条件
        if from_address and self.use_from_checkbox.isChecked():
            search_criteria += f' FROM "{from_address}"'
        
        self.search_thread = EmailSearchThread(
            self.email, self.password,search_criteria,keyword
        )
        self.search_thread.search_finished.connect(self.handle_search_results)
        self.search_thread.start()

    def handle_search_results(self, displayed_items, mail_data):    
        self.email_list.clear()  # 清空之前的郵件列表
        self.mail_data = mail_data  # 將郵件資料儲存在類別層級的字典中

        for mail_id, subject in displayed_items:
            item = QListWidgetItem(subject)
            item.setData(Qt.ItemDataRole.UserRole, mail_id)  # 只儲存 mail_id
            self.email_list.addItem(item)

    def display_email_content(self):
        selected_item = self.email_list.currentItem()
        if selected_item:
            mail_id = selected_item.data(Qt.ItemDataRole.UserRole)
            email_content = self.mail_data.get(mail_id, "(未能取得內容)")
            self.email_display.setPlainText(email_content)  # 顯示內容的函式


    """
    這是訂單處理功能，主要是我需要把訂單整理成word印下來
    因為公司就是這樣的程序，我只能寫這個功能幫助我....
    哈哈哈....TˇT
    主要是主裡訂單信件裡的文字，把每筆訂單的來源跟商品數量處理起來
    主要就是文字處理，去判斷那些文字是我要的，最後整理成字典
    到這邊還需要顯一些函式，把這些整理好的資料轉成表格或是其他形式
    顯示出來讓我們看這些資訊對不對...，哭欸思考到這邊發現這樣到這函數的多線呈
    我是不是不該傳儲存路徑，因為要先確認儲存成word，還是我就直接儲存成word?
    哭欸
    """
    def order_sorting(self):
        if self.order_sorting_window is not None:
            QMessageBox.warning(self, "阿肥之力", "訂單整理視窗已經開打")
            return
        if not self.mail_data:  # 檢查 mail_data 是否為空
            QMessageBox.warning(self, "阿肥之力", "還沒有搜索信件，請先搜索")
            return  # 如果為空，提前結束函式
        self.sorting_thread = OrderSortingThread(self.mail_data, self.folder_path_display.text())
        self.sorting_thread.sorting_finished.connect(self.handle_sorting_results)
        self.sorting_thread.start()


    def handle_sorting_results(self,processed_data):
        folder_path=self.folder_path_display.text() 
        print(f"路徑是啥:{folder_path}")
        # 打開新視窗並顯示結果 
        self.order_sorting_window = OrderSortingWindow(None,processed_data,folder_path)
        self.order_sorting_window.data_changed.connect(self.order_data_and_total_data)
        self.order_sorting_window.closed.connect(self.on_order_sorting_window_closed)
        # self.order_sorting_window.show() 

    def on_order_sorting_window_closed(self):
        self.order_sorting_window = None
        print("訂單整理視窗已經關閉")

    def order_data_and_total_data(self,data):
        self.order_all_data=data
        print(f"哭ㄟ{self.order_all_data}")

    def order_sorting_to_excel(self):
        if self.order_all_data is None:
            QMessageBox.warning(self, "阿肥之力", "請先使用...訂單整理功能")
            return
        if self.order_sorting_to_excel_window is not None:
            QMessageBox.warning(self, "阿肥之力", "銷貨明細功能視窗已經開打")
            return
        folder_path=self.folder_path_display.text() 
        print(f"路徑是啥:{folder_path}")
        self.order_sorting_to_excel_window = OrderSortingToExcelWindow(None,self.order_all_data,folder_path)
        self.order_sorting_to_excel_window.closed.connect(self.on_order_sorting_to_excel_window_closed)
        self.order_sorting_to_excel_window.show() 
        
    def on_order_sorting_to_excel_window_closed(self):
        self.order_sorting_to_excel_window =None
        print("銷貨寫入功能視窗已關閉")


    def open_folder_dialog(self):
        """ 打開選擇資料夾對話框 """
        folder_path = QFileDialog.getExistingDirectory(self, "選擇資料夾")
        if folder_path:
            self.folder_path_display.setText(folder_path)
            print(f"選擇的資料夾: {folder_path}")
            try:
                self.database.User_basic_information_dao.update_user_folder_path(folder_path)
            except Exception as e:
                print(f"更新路徑到資料庫時發生錯誤: {e}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.display_email_content()
        else:
            super().keyPressEvent(event)

    def clear_layout(self):
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def handle_close(self):
        if self.order_sorting_window is not None:
            self.order_sorting_window.close()
            self.order_sorting_window= None

        if self.order_sorting_to_excel_window is not None:
            self.order_sorting_to_excel_window.close()
            self.order_sorting_to_excel_window= None

    def closeEvent(self, event):
        self.close_signal.emit() # 發射關閉訊號
        event.accept()