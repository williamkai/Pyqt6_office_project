import mysql.connector

class CustomerInformationDao:

    def __init__(self, connection=None, cursor=None):
        self.connection = connection
        self.cursor = cursor

    def create_customer_information_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INT AUTO_INCREMENT PRIMARY KEY,
                CompanyName VARCHAR(255) UNIQUE NOT NULL,
                Abbreviation VARCHAR(255),
                PersonInCharge VARCHAR(255),
                ContactPerson VARCHAR(255),
                VATNumber VARCHAR(50),
                Phone1 VARCHAR(50),
                Phone2 VARCHAR(50),
                Fax VARCHAR(50),
                MobilePhone VARCHAR(50),
                Email VARCHAR(255),
                CompanyAddress TEXT,
                FactoryAddress TEXT,
                Website VARCHAR(255),
                LINEID VARCHAR(50),
                Notes TEXT
            )
        """
        #公司ID、公司名稱、簡稱、負責人、聯絡人、統一編號、電話1、電話2
        #傳真、行動電話、電子信箱、公司地址、工廠地址、網址、LINE ID、備註
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error creating CustomerInformation table: {err}")

    def get_customer_list(self):
        query = """
            SELECT Abbreviation, CompanyName, ContactPerson, 
                Phone1, MobilePhone, CompanyAddress
            FROM Customers
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_customer_by_company_name(self, company_name):
        query = """
            SELECT CustomerID AS id, Abbreviation AS short_name, CompanyName AS company_name,
                PersonInCharge AS manager, ContactPerson AS contact_person, VATNumber AS vat_number,
                Phone1 AS phone, Phone2 AS phone2, Fax AS fax, MobilePhone AS mobile,
                Email AS email, CompanyAddress AS company_address, FactoryAddress AS factory_address,
                Website AS website, LINEID AS line_id, Notes AS notes
            FROM Customers
            WHERE CompanyName = %s
        """
        self.cursor.execute(query, (company_name,))
        return self.cursor.fetchone()

    def delete_customer(self, customer_short_name):
        delete_query = "DELETE FROM CustomerInformation WHERE customer_short_name = %s"
        try:
            self.cursor.execute(delete_query, (customer_short_name,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error deleting from CustomerInformation table: {err}")

    def check_company_name_exist(self, company_name):
        query = "SELECT COUNT(*) FROM Customers WHERE CompanyName = %s"
        self.cursor.execute(query, (company_name,))
        result = self.cursor.fetchone()
        if result and result[0] > 0:
            return True
        else:
            return False

    def insert_customer(
                self,short_name,company_name,invoice_title,manager,contact_person, 
                phone1, phone2,fax,mobile,email,company_address,factory_address,website, 
                line_id,notes
                        ):
        insert_query = """
        INSERT INTO Customers (Abbreviation, CompanyName, Invoice_Title, Manager,
                               ContactPerson, Phone1, Phone2, Fax, MobilePhone, 
                               Email, CompanyAddress, FactoryAddress, 
                               Website, LINEID, Notes)
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(insert_query, (short_name,  company_name, invoice_title, manager,
                                            contact_person, phone1, phone2, fax, mobile, 
                                            email, company_address, factory_address, 
                                            website, line_id, notes))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Error inserting into Customers table: {err}")

    def update_customer(self, customer_id, short_name,company_name, invoice_title, manager,
                    contact_person, phone, phone2, fax, mobile, email, company_address, factory_address,
                    website, line_id, notes):
        # Check if the new company_name conflicts with existing records (excluding current customer_id)
        check_query = "SELECT CustomerID FROM Customers WHERE CompanyName = %s AND CustomerID != %s"
        self.cursor.execute(check_query, (company_name, customer_id))
        conflicting_customer = self.cursor.fetchone()

        if conflicting_customer:
            # There is a conflict with another customer's company_name
            return False  # Return False to indicate the update was not successful

        # Update the customer record
        update_query = """
            UPDATE Customers
            SET Abbreviation = %s, CompanyName = %s, CompanyFullName = %s, InvoiceTitle = %s, PersonInCharge = %s,
                ContactPerson = %s, Phone1 = %s, Phone2 = %s, Fax = %s, MobilePhone = %s,
                Email = %s, CompanyAddress = %s, FactoryAddress = %s, Website = %s, LINEID = %s, Notes = %s
            WHERE CustomerID = %s
        """
        values = (
            short_name, company_name, invoice_title, manager, contact_person,
            phone, phone2, fax, mobile, email, company_address, factory_address,
            website, line_id, notes, customer_id
        )
        self.cursor.execute(update_query, values)
        self.connection.commit()

        return True  # Return True to indicate the update was successful