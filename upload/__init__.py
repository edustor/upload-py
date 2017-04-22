import os

from pymongo import MongoClient
from .pika import PikaConnectionManager

mongo = MongoClient(os.environ["edustor.mongo.uri"])
pika_connection_manager = PikaConnectionManager()