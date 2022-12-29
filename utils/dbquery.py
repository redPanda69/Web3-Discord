import mysql.connector as conector
import os
con = conector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "project"
)
cursor = con.cursor()
def add_details(_id,result,bet):
    cursor.execute(f"INSERT INTO gamehistory VALUES ({bet},'{_id}','{result}')")
    con.commit()

def request_profile(_id,result):
    cursor.execute(f"SELECT COUNT(*) FROM gamehistory WHERE usrID = '{_id}' AND result = '{result}'")
    res = cursor.fetchall()[0][0]
    return res