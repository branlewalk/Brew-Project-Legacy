import os
import sys
import pika
import mysql.connector
from datetime import datetime

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
    mycursor.execute("CREATE TABLE temperatures (timestamp DATE, hlt FLOAT(5,2), mlt FLOAT(5,2), bk FLOAT(5,2))")
except mysql.connector.errors.ProgrammingError:
    print("Table Exists")

mycursor.close()
mydb.close()

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.queue_declare(queue='temps')
channel.queue_bind(queue='temps', exchange='temps')

on_off = False
for method_frame, properties, body in channel.consume('temps'):
    print(body)
    message_type = properties.headers.get('type')
    if message_type == 'command':
        on_off = body == 'true'
        if on_off:
            print("Connecting...")
            mydb = mysql.connector.connect(
                host="db",
                user="root",
                #  passwd="R3v0lv3r!",
                database="sessions"
            )
            mycursor = mydb.cursor()
        else:
            print("Disconnecting...")
            mycursor.close()
            mydb.close()
    else:
        if on_off:
            sql = "INSERT INTO temperatures (timestamp, hlt, mlt, bk) VALUES (%s, %s, %s, %s)"
            val = (datetime.now(), body[0], body[1], body[2])
            mycursor.execute(sql, val)
            mydb.commit()
            print("Persisted : " + str(val))
    channel.basic_ack(method_frame.delivery_tag)

# channel.close()
# connection.close()



