import os

import pika.channel
import pika.exceptions


class PikaConnectionManager:
    _pika_connection = None

    def __init__(self):
        self._connect()
        channel = self.get_channel()

        channel.exchange_declare(exchange="internal.edustor",
                                 exchange_type="topic",
                                 durable=True)
        channel.close()

    def get_channel(self):
        try:
            channel = self._pika_connection.channel()
        except pika.exceptions.ConnectionClosed:
            self._connect()
            channel = self._pika_connection.channel()

        return channel

    def _connect(self):
        if self._pika_connection is not None:
            # noinspection PyBroadException
            try:
                self._pika_connection.close()
            except:
                pass
        self._pika_connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["edustor.rabbit.host"]))
