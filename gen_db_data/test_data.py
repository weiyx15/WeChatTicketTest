"""
insert test data into database for unit test and function test
"""

import MySQLdb


db = MySQLdb.connect('127.0.0.1', 'root', 'o443W586A2', 'wechat_ticket')

cursor = db.cursor()

sql = """INSERT INTO wechat_user(open_id, to_active) VALUES ('weiyx', 1)"""

try:
    cursor.execute(sql)
    db.commit()
    print('success~~')
except:
    db.rollback()
    print('fail~~')

db.close()
