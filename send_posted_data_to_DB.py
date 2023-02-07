#!/usr/bin/python3
import time
import cgi
import datetime
import sqlite3

DATABASE = "URL of DB"
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

form = cgi.FieldStorage()
temperature = form.getvalue("temperature")
humidity = form.getvalue("humidity")

#----起動時DB作成---
cur.execute("CREATE TABLE IF NOT EXISTS data (id,date, temp, humi)")
#----起動時のDBの行数を取得---
cur.execute("SELECT COUNT(*) FROM data")
numOfRecords = cur.fetchall() #numOfRecordsに現在のレコード数を代入
id = numOfRecords[0][0] + 1 #次にインサートする時のid番号を設定
now = datetime.datetime.now()

try:
        #----DBの行数を取得---
        cur.execute("SELECT COUNT(*) FROM data")
        numOfRecords = cur.fetchall() #numOfRecordsに現在のレコード数を代入
        if numOfRecords[0][0] < 720: #-----行数が720未満だったらデータをインサート-----
                cur.execute("INSERT INTO data VALUES (?, ?, ?, ?)", [id, now.strftime("%H:%M"), temperature, humidity])
                id = id + 1
                conn.commit()
        else: #----既に行数が720ある場合---
                id = 720
                cur.execute("DELETE FROM data WHERE id=1") #idが１の行を削除
                for i in range(1,720): #-----idを前に詰める----
                        cur.execute("UPDATE data SET id = ? WHERE id= ?", [i, i+1])
                cur.execute("INSERT INTO data VALUES (?, ?, ?, ?)", [id, now.strftime("%H:%M"), temperature, humidity])
                conn.commit()
except:
        pass

conn.close()

print("Content-type: text/plain\n")
print("hello")