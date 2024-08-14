#jinghong_order_processing_widget.py
import imaplib
import email
import quopri
import urllib.parse
from datetime import datetime
from email import message_from_bytes
from email.charset import Charset
from email.header import decode_header
from PyQt6.QtWidgets import (QWidget, 
                             QVBoxLayout, 
                             QHBoxLayout, 
                             QPushButton, 
                             QLineEdit, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QMessageBox, QDialog, 
                             QFormLayout,
                             QDateTimeEdit, 
                             QCompleter, 
                             QComboBox,
                             QListWidget,
                             QTextEdit,
                             QDateEdit,
                             QTimeEdit,
                             QSpacerItem,
                             QSizePolicy,
                             QCheckBox,
                             QLabel,
                             QGroupBox,
                             QListWidgetItem)

from PyQt6.QtCore import QDateTime,Qt,QDate, QTime

from success_login.email_widget.email_search_thread import EmailSearchThread
class JinghongOrderProcessingWidget(QWidget):
    
    def __init__(self, parent=None, database=None,email=None,password=None):
        super().__init__(parent)
        self.database = database
        self.parent_widget = parent  # 儲存父部件的引用
        self.email = email
        self.password = password
        self.email_list = None  # 初始化爲 None，表示元件尚未建立
        self.email_display = None  # 初始化爲 None，表示元件尚未建立
        self.email_search_layout = None
        
        self.initialize_ui() 

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
        self.order_sorting_button.clicked.connect(self.email_search)
        self.order_sorting_button.setFixedWidth(150)
        self.button_layout.addWidget(self.order_sorting_button)

        self.sales_details_writing_button = QPushButton("銷貨明細寫入功能")
        self.sales_details_writing_button.clicked.connect(self.email_search)
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
            self.display_layout.addWidget(self.email_display, 4)

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
        self.date_edit.setFixedWidth(150)
        self.date_time_layout.addWidget(self.date_edit)
        #添加時間選擇器
        self.timeedit = QTimeEdit(self)
        self.timeedit.setDisplayFormat('hh:mm:ss')
        self.time = QTime(7, 0, 0)  # 参数依次是小时、分钟、秒
        self.timeedit.setTime(self.time)
        self.timeedit.setFixedWidth(150)
        self.date_time_layout.addWidget(self.timeedit)

        spacer_item = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.date_time_layout.addItem(spacer_item)
        self.email_search_layout.addLayout(self.date_time_layout)

        # 添加一个 QLineEdit 用于输入 from 地址
        self.from_input_label = QLabel("寄件人:", self)
        self.from_input_layout.addWidget(self.from_input_label)
        self.from_input = QLineEdit(self)
        self.from_input.setPlaceholderText("输入寄件人郵箱地址")
        self.from_input.setFixedWidth(200)
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
        self.keyword_input.setText("久富餘-菁弘")  # 預設關鍵字
        self.keyword_input_layout.addWidget( self.keyword_label)
        self.keyword_input_layout.addWidget( self.keyword_input)
        self.email_search_layout.addLayout(self.keyword_input_layout)
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

    def order_search(self):
        date_str = self.date_edit.date().toString("dd-MMM-yyyy")
        from_address = self.from_input.text()
        keyword = self.keyword_input.text()

        self.search_thread = EmailSearchThread(
            self.email, self.password, date_str, from_address, keyword
        )
        self.search_thread.search_finished.connect(self.handle_search_results)
        self.search_thread.start()
    
    def handle_search_results(self, mail_data):    
        self.email_list.clear()  # 清空之前的郵件列表
        for mail_id, email_message in mail_data:
            subject = email_message['Subject']
            print(f"無轉碼前的標題:{subject}")
            subject = self.decode_mime_header(subject) if subject else "(無標題)"
            from_ = email_message['From']

            item = QListWidgetItem(f"{subject} - {from_}")
            item.setData(Qt.ItemDataRole.UserRole, email_message)
            self.email_list.addItem(item)
 
            
    def display_email_content(self):
        selected_item = self.email_list.currentItem()
        if selected_item:
            email_message = selected_item.data(Qt.ItemDataRole.UserRole)
            email_content = ""

            # 取得郵件主題並解碼
            subject_header = email_message.get('Subject', '')
            subject =self.decode_mime_header(subject_header)
            print(f"郵件主題: {subject}")

            # 解析郵件內容
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    charset = part.get_content_charset()
                    if content_type == "text/plain":
                        try:
                            payload = part.get_payload(decode=True)
                            if charset:
                                email_content += payload.decode(charset)
                            else:
                                email_content += payload.decode('utf-8', errors='replace')
                        except (UnicodeDecodeError, TypeError) as e:
                            print(f"解碼錯誤: {e}")
            else:
                charset = email_message.get_content_charset()
                try:
                    payload = email_message.get_payload(decode=True)
                    if charset:
                        email_content = payload.decode(charset)
                    else:
                        email_content = payload.decode('utf-8', errors='replace')
                except (UnicodeDecodeError, TypeError) as e:
                    print(f"解碼錯誤: {e}")

            self.email_display.setPlainText(email_content)

    def utf7_encode(self,text):
        return text.encode('utf-7')
    
    def decode_mime_header(self, header):
        decoded_parts = decode_header(header)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if encoding is not None:
                decoded_string += part.decode(encoding)
            else:
                decoded_string += part.decode('utf-8', errors='replace')
        return decoded_string

    def clear_layout(self):
        while self.main_layout.count() > 0:
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()