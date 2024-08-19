# order_sorting_window.py
import os
from PyQt6.QtCore import pyqtSignal
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.shared import RGBColor
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, 
                             QTableWidget, 
                             QTableWidgetItem, 
                             QVBoxLayout,
                             QHBoxLayout, 
                             QWidget, 
                             QTabWidget, 
                             QDialog, 
                             QVBoxLayout, 
                             QTextEdit,
                             QPushButton,
                             QListWidget,
                             QListWidgetItem)

class OrderSortingWindow(QWidget):
    closed = pyqtSignal()
    data_changed = pyqtSignal(dict)

    def __init__(self, parent=None, processed_data=None,folder_path=None):
        super().__init__(parent)  # 僅傳遞 parent 參數給 QWidget
        self.processed_data = processed_data  # 儲存 processed_data
        self.folder_path=folder_path
        self.order_list = None
        self.order_table = None
        self.stats=None
        self.setWindowTitle("訂單處理結果")
        self.setMinimumSize(300, 400)
        self.resize(400, 700)
        self.initialize_ui()
        self.create_order_list()
        self.calculate_statistics()

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.but_layout =QHBoxLayout()
        
        # 如果 order_list 尚未建立，則建立它
        if self.order_list is None:
            self.order_list = QListWidget(self)
            self.order_list.setMinimumHeight(50)
            self.order_list.itemClicked.connect(self.display_order_table)
            self.display_layout.addWidget(self.order_list, 1)
                
        # 建立表格
        if self.order_table is None:
            self.order_table = QTableWidget(self)
            self.display_layout.addWidget(self.order_table, 5)
        
        self.save_button = QPushButton("Save to Word", self)
        self.save_button.clicked.connect(self.save_table_to_word)  # 連結按鈕點擊事件到儲存功能
        self.but_layout.addWidget(self.save_button)
        self.display_layout.addLayout(self.but_layout)  # 將按鈕添加到佈局中
        
        self.main_layout.addWidget(self.display_area)

    def create_order_list(self):
        self.order_list.clear()  # 清空之前的郵件列表
        order_list_title = ["大榮", "通盈","大榮商品總數","通盈商品總數"]
        for title in order_list_title:
            item = QListWidgetItem(title)  # 使用 title 替代 "tilte"
            self.order_list.addItem(item)

    def calculate_statistics(self):
        # 初始化字典來存儲統計結果
        self.stats = {'大榮': {},'通盈': {}}
        # 遍歷 '大榮' 和 '通盈' 分類
        for category in ['大榮', '通盈']:
            # 獲取當前分類的數據
            category_data = self.processed_data[category]  
            # 遍歷該分類中的每個訂單
            for order_id, order_details in category_data.items():
                # 遍歷每個訂單中的商品
                for item in order_details['items']:
                    product_code = item['product_code']
                    quantity = int(item['quantity'])
                    # 更新統計數據
                    if product_code in self.stats[category]:
                        self.stats[category][product_code] += quantity
                    else:
                        self.stats[category][product_code] = quantity

    def display_order_table(self):
        # 清空表格
        self.order_table.clear()
        # 取得選中的列表項
        selected_item = self.order_list.currentItem()
        if not selected_item:
            return
        # 根據選中的項的文本來取得相應的資料
        selected_key = selected_item.text()
        print(f"{selected_key}")

        if selected_key in ["大榮商品總數", "通盈商品總數"]:
            cleaned_key =selected_key.replace("商品總數", "")
            print(f"{cleaned_key}")
            print(f"這個不應該去掉商品總數{selected_key}")
            self.create_order_total_table(cleaned_key)
        else:
            data_to_display = self.processed_data.get(selected_key, {})
            # 顯示表格
            self.create_order_table(data_to_display)

    def create_order_table(self, data):
        # 轉換鍵爲字串
        data = self.convert_keys_to_str(data)
        # 清空表格
        self.order_table.setRowCount(0)
        # 設定表頭
        self.order_table.setColumnCount(4)
        self.order_table.setHorizontalHeaderLabels(['訂單來源', '商品代號', '數量', '單位'])
        # 填充資料
        row_count = 0
        for key, order in data.items():
            for i, item in enumerate(order['items']):
                self.order_table.insertRow(row_count)
                if i == 0:
                    self.order_table.setItem(row_count, 0, QTableWidgetItem(order['title']))
                self.order_table.setItem(row_count, 1, QTableWidgetItem(item['product_code']))
                self.order_table.setItem(row_count, 2, QTableWidgetItem(item['quantity']))
                self.order_table.setItem(row_count, 3, QTableWidgetItem('箱'))
                row_count += 1
        # 調整表格顯示
        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()

    def create_order_total_table(self,cleaned_key):
        # 轉換鍵爲字串        
        data_to_display = self.stats.get(cleaned_key, {})        
        # 清空表格
        self.order_table.setRowCount(0)
        # 設定表頭
        self.order_table.setColumnCount(3)
        self.order_table.setHorizontalHeaderLabels(['商品代號', '數量', '單位'])
        # 填充資料
        row_count = 0
        for code, total_quantity in self.stats[cleaned_key].items():
            self.order_table.insertRow(row_count)
            self.order_table.setItem(row_count, 0, QTableWidgetItem(code))
            self.order_table.setItem(row_count, 1, QTableWidgetItem(str(total_quantity)))
            self.order_table.setItem(row_count, 2, QTableWidgetItem('箱'))
            row_count += 1
        # 调整表格显示
        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()

    def convert_keys_to_str(self, data):
        if isinstance(data, dict):
            return {k.decode('utf-8') if isinstance(k, bytes) else k: self.convert_keys_to_str(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.convert_keys_to_str(i) for i in data]
        else:
            return data

    def save_table_to_word(self):
        selected_item = self.order_list.currentItem()
        if not selected_item:
            return  # 如果沒有選擇的項目，則不進行任何操作

        selected_key = selected_item.text()

        if selected_key in ["大榮商品總數", "通盈商品總數"]:
            self.handle_total_statistics()
        else:
            self.handle_order_details(selected_item)
        
        
    def handle_order_details(self, selected_item):
        # 確保 folder_path 使用適當的分隔符
        if not self.folder_path.endswith(os.path.sep):
            self.folder_path += os.path.sep
        # 建立 Word 文件
        doc = Document()
        # 擷取表格資料
        row_count = self.order_table.rowCount()
        previous_title = None
        selected_item_1=selected_item.text()

        for row in range(row_count):
            title = self.order_table.item(row, 0).text() if self.order_table.item(row, 0) else ''
            product_code = self.order_table.item(row, 1).text() if self.order_table.item(row, 1) else ''
            quantity = self.order_table.item(row, 2).text() if self.order_table.item(row, 2) else ''
            unit = self.order_table.item(row, 3).text() if self.order_table.item(row, 3) else ''
            # 如果第一欄有值，添加到 Word 文件中
            if title: 
                # if previous_title:
                #     doc.add_paragraph()  # 空一行

                # 根據選擇的項目添加段落
                if selected_item_1 == '大榮': 
                    paragraph = doc.add_paragraph(f"{title} 大榮-久富餘-菁弘")
                elif selected_item_1 == "通盈":
                    paragraph = doc.add_paragraph(f"{title} 通盈-久富餘-菁弘")

                 # 設定文字大小和字體
                for run in paragraph.runs:
                    run.font.size = Pt(14)
                    run.font.name = '標楷體'
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')  # 設定東亞字體
                
                previous_title = title
            # 添加商品資料
            paragraph = doc.add_paragraph(f"{product_code}……{quantity}{unit}")

             # 設定文字大小和字體
            for run in paragraph.runs:
                run.font.size = Pt(14)
                run.font.name = '標楷體'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')  # 設定東亞字體

        # 取得當前日期
        today_date = datetime.now().strftime('%m%d')
        year = int(datetime.now().strftime('%Y'))
        year_TW = year - 1911
        today_date_tw=f"{year_TW}{today_date}"

        file_name = f'{today_date_tw}{selected_item.text()}.docx'
        file_path = os.path.join(self.folder_path, file_name)
        doc.save(file_path)
        print(f"File saved to {file_path}")


    def handle_total_statistics(self):
        # 確保 folder_path 使用適當的分隔符
        print(f"{self.stats}")
        if not self.folder_path.endswith(os.path.sep):
            self.folder_path += os.path.sep
        # 建立 Word 文件
        doc = Document()

        for key, data in self.stats.items():
            # 新增標題
            heading = doc.add_heading(key, level=1)
            for run in heading.runs:
                run.font.size = Pt(26)
                run.bold = True
                run.font.name = '標楷體'
                run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')  # 設定東亞字體
            
            # 新增表格
            table = doc.add_table(rows=1, cols=2)
            table.style ="Light Shading Accent 5" #"Normal Table"#'Table Grid'
            
            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '商品代號'
            hdr_cells[1].text = '總箱數'
            
            for cell in hdr_cells:
                for run in cell.paragraphs[0].runs:
                    run.font.size = Pt(22)
                    run.font.name = '標楷體'
                    run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')  # 設定東亞字體
                    run.font.color.rgb = RGBColor(0, 0, 0)  # 設定字體顏色為黑色
            # 添加每一行資料
            for item_code, quantity in data.items():
                row_cells = table.add_row().cells
                row_cells[0].text = item_code
                row_cells[1].text = f'{quantity}'
                
                for cell in row_cells:
                    for run in cell.paragraphs[0].runs:
                        run.font.size = Pt(18)
                        run.font.name = '標楷體'
                        run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')  # 設定東亞字體
                        run.font.color.rgb = RGBColor(0, 0, 0) 

        # 取得當前日期
        today_date = datetime.now().strftime('%m%d')
        year = int(datetime.now().strftime('%Y'))
        year_TW = year - 1911
        today_date_tw=f"{year_TW}{today_date}"

        file_name = f'{today_date_tw}統計數量.docx'
        file_path = os.path.join(self.folder_path, file_name)
        doc.save(file_path)
        print(f"File saved to {file_path}")
        

    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)