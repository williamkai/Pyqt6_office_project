import mysql.connector

class CustomerInformationDao:

    def __init__(self, connection=None, cursor=None):
        self.connection = connection
        self.cursor = cursor

    def create_customer_information_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS CustomerInformation (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_short_name VARCHAR(255),
                customer_name VARCHAR(255) NOT NULL,
                company_name VARCHAR(255),
                invoice_title VARCHAR(255),
                manager VARCHAR(255),
                contact_person VARCHAR(255),
                phone VARCHAR(20),
                mobile_phone VARCHAR(20),
                company_address VARCHAR(255),
                email VARCHAR(255)
            )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating CustomerInformation table: {err}")

    def get_customer_list(self):
        query = "SELECT * FROM CustomerInformation"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def delete_customer(self, customer_short_name):
        delete_query = "DELETE FROM CustomerInformation WHERE customer_short_name = %s"
        try:
            self.cursor.execute(delete_query, (customer_short_name,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting from CustomerInformation table: {err}")

    def insert_customer(self, 
                        customer_short_name, 
                        customer_name, 
                        company_name, 
                        invoice_title, 
                        manager, 
                        contact_person, 
                        phone, 
                        mobile_phone, 
                        company_address, 
                        email):
        insert_query = """
            INSERT INTO CustomerInformation (customer_short_name, customer_name, company_name, invoice_title, manager, contact_person, phone, mobile_phone, company_address, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (customer_short_name, customer_name, company_name, invoice_title, manager, contact_person, phone, mobile_phone, company_address, email))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting into CustomerInformation table: {err}")

    def update_customer(self, customer_id, customer_short_name, customer_name, company_name, invoice_title, manager, contact_person, phone, mobile_phone, company_address, email):
        update_query = """
            UPDATE CustomerInformation
            SET customer_short_name = %s, customer_name = %s, company_name = %s, invoice_title = %s, manager = %s, contact_person = %s, phone = %s, mobile_phone = %s, company_address = %s,  email = %s
            WHERE customer_id = %s
        """
        try:
            self.cursor.execute(update_query, (customer_short_name, customer_name, company_name, invoice_title, manager, contact_person, phone, mobile_phone, company_address,  email, customer_id))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error updating CustomerInformation table: {err}")
