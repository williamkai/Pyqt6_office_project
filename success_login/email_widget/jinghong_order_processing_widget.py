#jinghong_order_processing_widget.py
import imaplib
import email
import quopri
import urllib.parse
import re
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
                             QListWidgetItem,
                             QFileDialog)
from PyQt6.QtCore import QDateTime,Qt,QDate, QTime, QEvent

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
        self.keyword_input.setText("訂單")  # 預設關鍵字
        self.keyword_input_layout.addWidget( self.keyword_label)
        self.keyword_input_layout.addWidget( self.keyword_input)
        self.email_search_layout.addLayout(self.keyword_input_layout)
        
        # 添加選擇資料夾按鈕及顯示資料夾路徑的標籤
        self.folder_label = QLabel("選擇保存資料夾:", self)
        self.folder_path_display = QLineEdit(self)
        self.folder_path_display.setFixedWidth(200)
        self.folder_path_display.setReadOnly(True)

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

    def order_search(self):
        folder_path=self.folder_path_display.text()
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
        keyword = self.keyword_input.text()  # 取得輸入框中的關鍵詞
        orders = {'大榮': {}, '通盈': {}}
        for mail_id, email_message in mail_data:
            # subject = email_message['Subject']
            subject = email_message.get('Subject', '(無標題)')
            subject = self.decode_mime_header(subject) if subject else "(無標題)"
            from_ = email_message['From']
             # 檢查標題是否包含關鍵詞
            if keyword.lower() in subject.lower():
                item = QListWidgetItem(f"信件代號/標題:{mail_id}/{subject}")  # - {from_}
                item.setData(Qt.ItemDataRole.UserRole, email_message)
                self.email_list.addItem(item)

                # 擷取郵件內容
                email_content = self.extract_order_details(email_message)  # 使用 extract_order_details 方法

                # 按內容分類
                if '大榮' in email_content:
                    order_details = self.parse_order_content(email_content)

                    orders['大榮'][mail_id] = order_details
                elif '通盈' in email_content:

                    orders['通盈'][mail_id] = self.extract_order_details(email_message)
        
        print(f"加入後的orders{orders}")

    def display_email_content(self):
        selected_item = self.email_list.currentItem()
        if selected_item:
            email_message = selected_item.data(Qt.ItemDataRole.UserRole)
            email_content = self.extract_order_details(email_message)  # 使用 extract_order_details 方法

            # 取得郵件主題並解碼
            subject_header = email_message.get('Subject', '')
            subject = self.decode_mime_header(subject_header)
            print(f"郵件主題: {subject}")

            # 取得接收時間
            date_header = email_message.get('Date', '')
            print(f"接收時間: {date_header}")

            # 如果有附件，將附件訊息添加到郵件內容中
            attachment_info = []
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get('Content-Disposition') is not None:
                        filename = part.get_filename()
                        if filename:
                            decoded_filename = self.decode_mime_header(filename)
                            attachment_info.append(decoded_filename)
            
            if attachment_info:
                email_content += "\n\n附件:\n"
                for attachment in attachment_info:
                    email_content += f"- {attachment}\n"
            
            # 添加接收時間到郵件內容中
            if date_header:
                email_content = f"接收時間: {date_header}\n\n{email_content}"

            self.email_display.setPlainText(email_content)

    def extract_order_details(self, email_message):
        email_content = ""

        # 解析郵件內容
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                charset = part.get_content_charset()
                
                # 處理內文內容
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

        # 清理郵件內容，去掉 "Subject:" 行及其以上的部分
        email_content = self.clean_email_content(email_content)

        return email_content
    
    def decode_mime_header(self, header):
        decoded_parts = decode_header(header)
        decoded_string = ""
        for part, encoding in decoded_parts:
            if encoding is not None:
                decoded_string += part.decode(encoding)
            else:
                decoded_string += part.decode('utf-8', errors='replace')
        return decoded_string

    def open_folder_dialog(self):
        """ 打開選擇資料夾對話框 """
        folder_path = QFileDialog.getExistingDirectory(self, "選擇資料夾")
        if folder_path:
            self.folder_path_display.setText(folder_path)
            print(f"選擇的資料夾: {folder_path}")

    def clean_email_content(self,content):
        # 查找并删除从 "Subject:" 行到邮件开头的部分
        pattern = r'Subject:.*\n.*\n'
        match = re.search(pattern, content)
        if match:
            # 找到 "Subject:" 行的位置，删除其以上内容
            content = content[match.end():].strip()
        return content
    
    def parse_order_content(self, email_content):
        # 初始化訂單標題和商品訊息
        order_title = ""
        items = {}

        # 定位“取貨明細如下：”的位置
        detail_marker = '取貨明細如下：'
        detail_index = email_content.find(detail_marker)
        
        if detail_index != -1:
            # 擷取“取貨明細如下：”之前的內容
            pre_detail_content = email_content[:detail_index].strip()

            # 找到日期後的標題
            # 日期的正則算式
            date_pattern = r'(\d{1,2}/\d{1,2})'
            # 搜尋日期
            date_match = re.search(date_pattern, pre_detail_content)
            
            if date_match:
                date_str = date_match.group(0)
                # 擷取日期後的標題內容
                title_start = date_match.end()
                title_content = pre_detail_content[title_start:].strip()
                
                # 去掉可能的首碼（例如“大榮-”或“通盈-”）
                title_parts = title_content.split(' ')
                if len(title_parts) > 1:
                    # 處理標題內容中的首碼部分
                    order_title = ' '.join(title_parts[1:]).strip()
                else:
                    order_title = title_content.strip()

            # 擷取“取貨明細如下：”之後到“以上”之前的內容
            post_detail_content = email_content[detail_index + len(detail_marker):]
            end_marker = '以上'
            end_index = post_detail_content.find(end_marker)
            
            if end_index != -1:
                detail_content = post_detail_content[:end_index].strip()
            else:
                detail_content = post_detail_content.strip()

            # 使用正則算式擷取商品代號和數量
            item_matches = re.findall(r'([A-Z0-9-]+)\s*…\s*(\d+)箱', detail_content)
            for item_code, quantity in item_matches:
                items[item_code] = int(quantity)

        return {
            'title': order_title,
            'items': items
        }

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