"""
Database manager
inspiration : https://stackoverflow.com/questions/4610791/can-i-put-my-sqlite-connection-and-cursor-in-a-function
"""
import sqlite3

#Create Customer Database with customer id ,full name ,transaction type ,amount ,status and transation id to store information locally.
class Database(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS transaction_information (cust_id INTEGER PRIMARY KEY, full_name TEXT, trans_type TEXT, amount REAL, status TEXT, trans_id INTEGER)")
        self.conn.commit()

    def __del__(self):
        self.conn.close()
#Add customer details
    def insert(self, full_name, trans_type, amount, status, trans_id):
        self.cur.execute("INSERT INTO transaction_information VALUES (NULL, ?, ?, ?, ?, ?)", (full_name, trans_type, amount, status, trans_id))
        self.conn.commit()
#Dispaly all transactions
    def view(self):
        self.cur.execute("SELECT * FROM transaction_information")
        rows = self.cur.fetchall()
        return rows
#Search Customer Information by Full name, amount,status APPROVED or DECLINED ,transaction ID
    def search(self, full_name="", trans_type="", amount="", status="", trans_id=""):
        self.cur.execute("SELECT * FROM transaction_information WHERE full_name=? OR trans_type=? OR amount=? OR status=? OR trans_id=?", (full_name, amount, status, trans_id))
        rows = self.cur.fetchall()
        return rows
#Delete Transaction information
    def delete(self, cust_id):
        self.cur.execute("DELETE from transaction_information WHERE cust_id=?", (cust_id,))
        self.conn.commit()
#Update Customer Transction information
    def update(self, cust_id, full_name, trans_type, amount, status, trans_id):
        self.cur.execute("UPDATE transaction_information SET full_name=?, trans_type=?, amount=?, status=?, trans_id=? WHERE cust_id=?", (full_name, trans_type, amount, status, trans_id, cust_id))
        self.conn.commit()