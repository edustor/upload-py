import os

import pika.channel
from pika.adapters.blocking_connection import BlockingChannel
from pymongo import MongoClient

mongo = MongoClient(os.environ["edustor.mongo.uri"])

rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["edustor.rabbit.host"]))
rabbit_channel = rabbit_connection.channel()

assert isinstance(rabbit_channel, BlockingChannel)
rabbit_channel.exchange_declare(exchange="internal.edustor",
                                exchange_type="topic",
                                durable=True)
