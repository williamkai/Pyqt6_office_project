# order_data_widget.py
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
                             QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout,
                             QDateTimeEdit, QCompleter, QComboBox)
from PyQt6.QtCore import QDateTime, Qt, QDate, QTimer
from functools import partial


class OrderDataWidget(QWidget):
    def __init__(self, parent=None, database=None):
        super().__init__(parent)
        self.database = database
        self.parent_widget = parent
        self.initialize_ui()


    def initialize_ui(self):
        print("創建UI")