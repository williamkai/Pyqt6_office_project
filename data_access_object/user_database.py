import os
import sys
import mysql.connector
import pickle
import configparser

from data_access_object.product_list_dao import ProductListDao
from data_access_object.inventory_dao import InventoryDao
from data_access_object.customer_dao import CustomerInformationDao
from data_access_object.User_basic_information_dao import UserBasicInformationDAO
from data_access_object.sales_order_dao import SalesOrderDao

class UserDatabase:
    '''
    主要連接我第二階段的資料庫
    也就是使用者帳戶的資料庫
    
    ''' 
    def __init__(self,user_email):
        self.connection = None
        self.cursor = None
        self.username=user_email
        self.initialize()
        self.product_list_dao=ProductListDao(self.connection,self.cursor)
        self.inventory_dao=InventoryDao(self.connection,self.cursor)
        self.customer_dao=CustomerInformationDao(self.connection,self.cursor)
        self.User_basic_information_dao=UserBasicInformationDAO(self.connection,self.cursor)
        self.sales_order_dao=SalesOrderDao(self.connection,self.cursor)

    def initialize(self):
        if self.connection is not None and self.cursor is not None:
            return
        
        # 判断是否為封裝状态，决定如何取得 config.pickle 的路径
        if getattr(sys, 'frozen', False):
            # 如果是封裝狀態（也就是打包成 exe），則使用 sys.executable 的目錄(也就是此exe檔案的目錄)
            exe_dir = os.path.dirname(sys.executable)
            config_path = os.path.join(exe_dir, 'config.pickle')
        else:
            # 如果不是封裝狀態，使用目前文件所在目錄的上一層目錄下的 login 文件夾中的 config.pickle
            config_path = os.path.join(os.path.dirname(__file__), '..', 'login', 'config.pickle')

        # 確認配置文件路徑是否存在
        if not os.path.exists(config_path):
            raise Exception(f"配置文件不存在或不完整: {config_path}")

        try:
            # 讀取配置文件
            with open(config_path, 'rb') as f:
                config = pickle.load(f)

            # 確認配置的完整性
            db_config = {
                'host': config.get('host', 'localhost'),
                'user': config.get('user', ''),
                'password': config.get('password', '')
            }

            if not all(db_config.values()):
                raise Exception("配置文件中缺少 'host', 'user' 或 'password'")

            # 連接到資料庫
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()  # 這是我除bug用到的東西，太久沒用忘記這啥了，dictionary=True

            # 創建個別帳戶使用的資料庫
            db_name = f"user_{self.username}"
            self.create_database(db_name)

            # 使用新創建的資料庫或者說個別帳號的資料庫
            self.connection.database = f'{db_name}'



        except mysql.connector.Error as err:
            raise Exception(f"無法連接資料庫: {err}")

    # 創建實例時候會先執行這句話，判斷有無這個資料庫，沒有就創建
    def create_database(self,db_name):
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        self.cursor.execute(create_database_query)

    def close(self):
        try:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing the database connection: {err}")
