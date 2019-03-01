import temp
from time import time, sleep
from datetime import datetime
import mysql.connector

sensor1 = temp.init_sensor_software(24)
sensor2 = temp.init_sensor_software(12)
sensor3 = temp.init_sensor_software(21)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="R3v0lv3r!"
)

mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE brewtemps")
except mysql.connector.errors.DatabaseError:
    print("Database Exists")


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="R3v0lv3r!",
  database="brewtemps"
)

mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE TABLE temperatures (timestamp DATE, hlt FLOAT(5,2), mlt FLOAT(5,2),"
                 " bk FLOAT(5,2), internal FLOAT(5,2))")
except mysql.connector.errors.ProgrammingError:
    print("Table Exists")

while True:
    hlt = temp.read_sensor_temp(sensor1)
    mlt = temp.read_sensor_temp(sensor2)
    bk = temp.read_sensor_temp(sensor3)
    internal = temp.read_internal_temp(sensor1)
    sql = "INSERT INTO temperatures (timestamp, hlt, mlt, bk, internal) VALUES (%s, %s, %s, %s, %s)"
    val = (datetime.now(), hlt, mlt, bk, internal)
    print("Values are: ", val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, " was inserted.")
    sleep(1)
