import os
import sys
from time import sleep
import json
from thermo import read_sensor
import pika

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbit', 5672, '/'))
channel = connection.channel()
channel.exchange_declare(exchange='temps', exchange_type='fanout')


def publish(temp):
    channel.basic_publish(exchange='temps', routing_key='', body=json.dumps(temp))


while True:
    all_temps = read_sensor()
    hlt = all_temps[0][1]
    mlt = all_temps[1][1]
    bk = all_temps[2][1]
    val = (hlt, mlt, bk)
    print("Values are: " + json.dumps(val))
    publish(val)
    print("Sent to Rabbit")
    sleep(1)

