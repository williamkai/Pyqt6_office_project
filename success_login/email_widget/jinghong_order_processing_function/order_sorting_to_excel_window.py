# order_sorting_window.py   
import os
from PyQt6.QtCore import pyqtSignal
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QWidget, QTabWidget, QDialog, QTextEdit, QPushButton, QListWidget,
    QListWidgetItem, QMessageBox, QProgressBar, QApplication
    )
import xlwings as xw  # 確保已經安裝 xlwings

class OrderSortingToExcelWindow(QWidget):
    START_ROW = 7
    SHEET_NAME = '工作表1'  # 可以根據實際情況修改

    closed = pyqtSignal()

    def __init__(self, parent=None, order_all_data=None, folder_path=None):
        super().__init__(parent)
        self.order_all_data = order_all_data
        self.folder_path = folder_path
        self.order_table = None
        self.stats = None
        self.setWindowTitle("銷貨明細處理視窗")
        self.setMinimumSize(300, 400)
        self.resize(500, 600)
        self.FILE_NAME = self.generate_file_name()
        self.initialize_ui()
        self.create_table()

    def generate_file_name(self):
        now = datetime.now()
        year = now.year - 1911  # 假設你需要的年份是民國年份
        month = now.month
        return f"{year}年{month}月久富餘對帳明細表-菁弘(含退貨).xlsx"

    def initialize_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)
        self.but_layout = QHBoxLayout()

        self.order_table = QTableWidget(self)
        self.display_layout.addWidget(self.order_table, 5)

        self.input_button = QPushButton("輸入到 Excel", self)
        self.input_button.setFixedWidth(150)
        self.input_button.clicked.connect(self.input_table_to_excel)
        self.but_layout.addWidget(self.input_button)

        # 添加 QProgressBar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(100)  # 假設最大值是 100%
        self.progress_bar.setValue(0)  # 初始值
        self.progress_bar.setFixedWidth(100)
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 2px solid #000;
                text-align: center;
                background: #aaa;
                color: #fff;
                height: 15px;
                border-radius: 8px;
                width: 150px;
            }
            QProgressBar::chunk {
                background: #333;
                width: 1px;
            }
        ''')
        self.but_layout.addWidget(self.progress_bar)

        self.display_layout.addLayout(self.but_layout)
        self.main_layout.addWidget(self.display_area)

    def create_table(self):
        self.order_table.setRowCount(0)
        self.order_table.setColumnCount(6)
        self.order_table.setHorizontalHeaderLabels(['物流', '訂單來源', '出貨單號', '商品代號', '數量', '單位'])

        if "通盈" in self.order_all_data["訂單資料"]:
            self.fill_order_data("通盈", self.order_all_data["訂單資料"]["通盈"])

        if "大榮" in self.order_all_data["訂單資料"]:
            self.fill_order_data("大榮", self.order_all_data["訂單資料"]["大榮"])

        self.order_table.resizeColumnsToContents()
        self.order_table.resizeRowsToContents()

    def fill_order_data(self, logistics_name, order_all_data):
        logistics_filled = False
        for key, order in order_all_data.items():
            order_source_filled = False
            for i, item in enumerate(order['items']):
                self.order_table.insertRow(self.order_table.rowCount())

                if not logistics_filled:
                    self.order_table.setItem(self.order_table.rowCount() - 1, 0, QTableWidgetItem(logistics_name))
                    logistics_filled = True
                else:
                    self.order_table.setItem(self.order_table.rowCount() - 1, 0, QTableWidgetItem(""))

                if not order_source_filled:
                    self.order_table.setItem(self.order_table.rowCount() - 1, 1, QTableWidgetItem(order['title']))
                    order_source_filled = True
                else:
                    self.order_table.setItem(self.order_table.rowCount() - 1, 1, QTableWidgetItem(""))

                self.order_table.setItem(self.order_table.rowCount() - 1, 3, QTableWidgetItem(item['product_code']))
                self.order_table.setItem(self.order_table.rowCount() - 1, 4, QTableWidgetItem(item['quantity']))
                self.order_table.setItem(self.order_table.rowCount() - 1, 5, QTableWidgetItem("箱"))

    def input_table_to_excel(self):
        # 確保表格有行資料
        if self.order_table.rowCount() == 0:
            print("表格沒有資料")
            return

        input_row_data = self.get_table_data()
        # 如果 get_table_data 返回空列表，顯示警告並終止
        if not input_row_data:
            QMessageBox.warning(self, "輸入錯誤", "請填入出貨單號")
            return

        folder_path = os.path.join(self.folder_path, "菁弘明細")
        file_path = os.path.join(folder_path, self.FILE_NAME)

        try:
            # 建立一個隱藏的 Excel 應用程式實例
            app = xw.App(visible=False)
            wb = app.books.open(file_path)
            ws = wb.sheets[self.SHEET_NAME]  # 使用常數 SHEET_NAME
        except Exception as e:
            print(f"無法打開文件: {e}")
            QMessageBox.warning(self, "錯誤", str(e))
            return

        # 從 START_ROW 開始搜尋空行
        first_empty_row = None
        for row in range(self.START_ROW, ws.api.UsedRange.Rows.Count + 1):
            if ws.range((row, 4)).value is None:  # 檢查 D 列（列索引 4）
                first_empty_row = row
                break

        # 檢查是否已經有相同資料
        last_data_value = input_row_data[-1][1] if input_row_data else None
        if first_empty_row is None:
            QMessageBox.warning(self, "錯誤", "無法找到空行")
            wb.close()
            app.quit()
            return

        last_row_index = first_empty_row - 1
        last_row_c_value = ws.range((last_row_index, 3)).value
        last_row_c_value = str(last_row_c_value)
        if '.' in last_row_c_value:
            last_row_c_value = last_row_c_value.split('.')[0]
        if str(last_row_c_value) == str(last_data_value):
            print("資料已經存在，無需再次寫入")
            wb.close()
            app.quit()
            QMessageBox.warning(self, "警告", "已有此次訂單資料")
            return

        # 插入新行並複製格式
        num_rows = len(input_row_data)
        self.progress_bar.setMaximum(num_rows)
        
        for i in range(num_rows):
            row_index = first_empty_row + i
            ws.api.Rows(row_index).Insert()  # 插入新行

            # 確保目標範圍有效
            if row_index + 1 <= ws.api.UsedRange.Rows.Count:
                source_range = ws.range((row_index + 1, 1), (row_index + 1, 14))
                target_range = ws.range((row_index, 1), (row_index, 14))
                
                # 複製源範圍
                source_range.copy()  # 使用 xlwings 的 copy 方法，將內容、格式和公式複製到剪貼板
                
                # 黏貼到目標範圍
                target_range.paste()  # 黏貼剪貼板內容到目標範圍
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()  # 確保界面更新

        # 寫入資料
        for i, row_data in enumerate(input_row_data):
            row_index = first_empty_row + i

            if row_data[0]:  # 如果第一列資料非空
                ws.range((row_index, 1)).value = datetime.now().strftime("%Y/%m/%d")
            if len(row_data) > 0 and row_data[0] != '':
                ws.range((row_index, 2)).value = row_data[0]
            if len(row_data) > 1:
                cell_value = row_data[1]
                if cell_value.isdigit():  # 檢查是否為數字
                    ws.range((row_index, 3)).value = int(cell_value)  # 存儲為整數
                elif cell_value:  # 檢查是否為非空文本
                    ws.range((row_index, 3)).value = cell_value  # 存儲為文本
                else:
                    ws.range((row_index, 3)).value = None  # 為空
            if len(row_data) > 2:
                ws.range((row_index, 4)).value = row_data[2]
            if len(row_data) > 3:
                # 同樣檢查 row_data[3] 非空且為數字
                if row_data[3].isdigit():
                    ws.range((row_index, 7)).value = int(row_data[3])
                else:
                    ws.range((row_index, 7)).value = None  # 如果不是數字，設置為空或其他處理
            
            self.progress_bar.setValue(i + 1)
            QApplication.processEvents()  # 確保界面更新

        try:
            wb.save(file_path)
            print("資料已成功寫入 Excel 文件")
            QMessageBox.information(self, "成功", "資料已成功寫入 Excel 文件")
        except Exception as e:
            print(f"無法保存文件: {e}")
            QMessageBox.warning(self, "錯誤", f"無法保存文件: {e}")
        finally:
            wb.close()
            app.quit()  # 關閉 Excel 應用程式

    def get_table_data(self):
        input_row_data = []
        temp_value = ""
        resuper = ["JFS303001-01", "JTS101010-01", "JTS102004-01", "JTS151205-01", "TTS151406-01", "JTS151206-01"]

        for row in range(self.order_table.rowCount()):
            row_data = []
            for col in range(4):
                actual_col = col + 1
                item = self.order_table.item(row, actual_col)
                cell_text = item.text() if item else ""

                if actual_col == 2:
                    if row == 0:  # Only check the first row's 出貨單號
                        if not cell_text:
                            return []  # 返回空列表中斷處理
                    if cell_text:
                        temp_value = cell_text
                    row_data.append(temp_value)
                elif actual_col == 3:
                    if cell_text in resuper:
                        cell_text += '.'
                    row_data.append(cell_text)
                else:
                    row_data.append(cell_text)

            input_row_data.append(row_data)
        return input_row_data

    def closeEvent(self, event):
        self.closed.emit()  # 當視窗關閉時發出訊號
        super().closeEvent(event)
