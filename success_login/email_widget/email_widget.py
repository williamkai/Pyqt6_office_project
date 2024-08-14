import imaplib
import shutil
import email
import os

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from datetime import datetime
from email.header import decode_header, make_header
from PyQt6.QtWidgets import (
                            QWidget, 
                            QVBoxLayout, 
                            QHBoxLayout, 
                            QPushButton,
                            QLabel,
                            QMessageBox,
                            QDateEdit,
                            QTextEdit,
                            QLineEdit,
                            QCheckBox,
                            QListWidget, 
                            QSpacerItem, 
                            QSizePolicy,
                            QDialogButtonBox, 
                            QTextBrowser, 
                            QListWidgetItem,
                            QDialog,
                            QTimeEdit)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QThread, pyqtSignal,Qt, QTime
from PyQt6 import QtCore 

from success_login.email_widget.jinghong_order_processing_widget import JinghongOrderProcessingWidget



class EmailWidget(QWidget):

    closed = pyqtSignal()

    def __init__(self, parent=None, database=None,email=None,password=None):
        super().__init__(parent)
        self.database=database
        self.setWindowTitle("信箱功能")
        self.setMinimumSize(900, 600)
        self.email=email
        self.password=password
        self.main_layout = QVBoxLayout(self) #垂直布局
        self.initialize_ui()


    def initialize_ui(self):
        # 創建水平布局
        self.button_layout = QHBoxLayout()
 
        self.Jinghong_order_processing_button = QPushButton("菁弘訂單處理", self)
        self.Jinghong_order_processing_button.clicked.connect(self.Jinghong_order_processing)
        self.Jinghong_order_processing_button.setFixedWidth(200)
        self.button_layout.addWidget(self.Jinghong_order_processing_button)
        #order_toword_button
        self.APP_email_processing_button = QPushButton("APP信件處理功能", self)
        self.APP_email_processing_button.clicked.connect(self.APP_email_processing)
        self.APP_email_processing_button.setFixedWidth(200)
        self.button_layout.addWidget(self.APP_email_processing_button)
         #order_toword_button
        self.Daily_report_processing_button = QPushButton("每日報表處理to_APP", self)
        self.Daily_report_processing_button.clicked.connect(self.Daily_report_processing)
        self.Daily_report_processing_button.setFixedWidth(200)
        self.button_layout.addWidget(self.Daily_report_processing_button)

        self.main_layout.addLayout(self.button_layout)

        self.display_area = QWidget()
        self.display_layout = QVBoxLayout(self.display_area)

        self.main_layout.addWidget(self.display_area)
        # self.grid_layout = None
 
    def Jinghong_order_processing(self):
        self.clear_display_area()
        self.Jinghong_order_processing = JinghongOrderProcessingWidget(parent=self,database=self.database,email=self.email,password=self.password)
        self.display_layout.addWidget(self.Jinghong_order_processing)
        print("測試測試-訂單功能")
        print(f"使用的邮箱: {self.email}")

        
    def APP_email_processing(self):
        print("還沒做。待訂功能")

    def Daily_report_processing(self):
        print("彰濱廠每日報表處理")

    def clear_display_area(self):
        print("清空顯示區")
        # 清空顯示區域
        while self.display_layout.count() > 0:
            item = self.display_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 清空GridLayout对象及其中的部件
        # if self.grid_layout:
        #     while self.grid_layout.count() > 0:
        #         item = self.grid_layout.takeAt(0)
        #         widget = item.widget()
        #         if widget:
        #             widget.deleteLater()

        #     # 將布局管理器置空，以便重新使用
        #     self.grid_layout = None

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()
