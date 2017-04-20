import os

import pika
from pymongo import MongoClient

mongo = MongoClient(os.environ["edustor.mongo.uri"])

rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["edustor.rabbit.host"]))
rabbit_channel = rabbit_connection.channel()
