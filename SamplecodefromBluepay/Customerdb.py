import sqlite3


conn=sqlite3.connect('customer_information.db')
c=conn.cursor()
def create_table():
       c.execute("CREATE TABLE if not EXISTS customerdetails(date TEXT, Trans_ID REAL, Account TEXT , Mode TEXT , Amount REAL ,Cradtype TEXT ,Status TEXT")
print (c.fetchall())

conn.close()


def select_all_userid(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM customerdetails ")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))
    rows = cur.fetchall()
    for row in rows:
        print(row)


