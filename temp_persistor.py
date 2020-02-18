import json
import os
import sys
import pika
import mysql.connector
from datetime import datetime

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sessionID = 0

mydb = mysql.connector.connect(
    host="db",
    user="root",
    #  passwd="R3v0lv3r!"
)

mycursor = mydb.cursor()
try:
    mycursor.execute("CREATE DATABASE sessions")
except mysql.connector.errors.DatabaseError:
    print("Database Exists")

mydb = mysql.connector.connect(
    host="db",
    user="root",
    # passwd="R3v0lv3r!",
    database="sessions"
)
mycursor = mydb.cursor()
try:
    mycursor.execute("DROP TABLE sessions")
    print("Sessions table dropped")
except mysql.connector.errors.ProgrammingError:
    print("Sessions table not dropped")

try:
    mycursor.execute("DROP TABLE temperatures")
    print("Temperature table dropped")
except mysql.connector.errors.ProgrammingError:
    print("Temperature table not dropped")
try:
    mycursor.execute("CREATE TABLE sessions (ID int AUTO_INCREMENT, name CHAR(25), PRIMARY KEY(ID))")
except mysql.connector.errors.ProgrammingError:
    print("Sessions Table Exists")
try:
    mycursor.execute("CREATE TABLE temperatures (session INT REFERENCES sessions(ID), timestamp TIMESTAMP, "
                     "hlt FLOAT(5,2), mlt FLOAT(5,2), bk FLOAT(5,2))")
except mysql.connector.errors.ProgrammingError:
    print("Temperature Table Exists")

mycursor.close()
mydb.close()

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.queue_declare(queue='temps')
channel.queue_bind(queue='temps', exchange='temps')

on_off = False


def connect():
    global mydb, mycursor
    print("Connecting...")
    mydb = mysql.connector.connect(
        host="db",
        user="root",
        #  passwd="R3v0lv3r!",
        database="sessions"
    )
    mycursor = mydb.cursor()


def disconnect():
    print("Disconnecting...")
    mycursor.close()
    mydb.close()


def create_session():
    connect()
    print("Creating Session...")
    sname = json.loads(body)
    print(sname)
    isql = "INSERT INTO sessions (name) VALUES ('" + sname + "')"
    mycursor.execute(isql)
    mydb.commit()
    mycursor.execute("SELECT ID FROM sessions WHERE name = '" + sname + "'")
    row = mycursor.fetchone()
    s_id = row[0]
    print("Created Session: " + str(body) + ", ID: " + str(s_id))
    disconnect()
    return s_id


for method_frame, properties, body in channel.consume('temps'):
    print(body)
    message_type = properties.headers.get('type')
    if message_type == 'command':
        if sessionID != 0:
            on_off = body == 'true'
            if on_off:
                connect()
            else:
                disconnect()
        else:
            print("Unable to start session with out Session ID")
    elif message_type == "create":
        sessionID = create_session()
    else:
        if on_off:
            sql = "INSERT INTO temperatures (session, timestamp, hlt, mlt, bk) VALUES (%s, %s, %s, %s, %s)"
            tempList = json.loads(body)
            val = (sessionID, datetime.now(), tempList[0], tempList[1], tempList[2])
            mycursor.execute(sql, val)
            mydb.commit()
            print("Persisted : " + str(val))
    channel.basic_ack(method_frame.delivery_tag)

# channel.close()
# connection.close()
