# email_search_thread.py
from email.header import Header
import re
import imaplib
import email
from PyQt6.QtCore import QThread, pyqtSignal

class EmailSearchThread(QThread):

    search_finished = pyqtSignal(list)  # Emit list of tuples with (mail_id, email_message)

    def __init__(self, email, password,search_criteria):
        super().__init__()
        self.email = email
        self.password = password
        self.search_criteria = search_criteria

    def run(self):
        mail_data = []
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email, self.password)
            mail.select('inbox')

            print(f"搜索條件: {self.search_criteria}")
            result, data = mail.search(None,self.search_criteria)
            if result == 'OK':
                mail_ids = data[0].split()
                print(f"找到的郵件數量: {len(mail_ids)}")
                for mail_id in mail_ids:
                    result, message_data = mail.fetch(mail_id, '(RFC822)')
                    raw_email = message_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    mail_data.append((mail_id, email_message))
                print(f"一開始創的空清單:把所有資訊保存進去:{mail_data}")

            mail.logout()

        except Exception as e:
            print(f"Error: {e}")
        
        self.search_finished.emit(mail_data)

    def encode_keyword_to_mime(self, keyword, charset='big5'):
        try:
            # Create Header object and encode
            header = Header(keyword, charset)
            print(f"{header }")
            # Get encoded bytes
            encoded_bytes = header.encode()
            print(f"{encoded_bytes }")
            mime_encoded_string=encoded_bytes.replace("=?big5_tw?b?","")
            mime_encoded_string=mime_encoded_string.replace("==?=","")
            # Convert bytes to string directly
            print(f"{mime_encoded_string }")
            return mime_encoded_string
        except Exception as e:
            print(f"Error encoding keyword: {e}")
            return ""