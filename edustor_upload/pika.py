import os

import pika.channel
import pika.exceptions
import logging

_logger = logging.getLogger("edustor_upload.pika")


class PikaConnectionManager:
    _pika_connection = None

    def __init__(self):
        _logger.info("Initializing Pika connection")
        self._connect()
        channel = self.get_channel()

        channel.exchange_declare(exchange="internal.edustor",
                                 exchange_type="topic",
                                 durable=True)
        channel.close()
        _logger.info("Pika initialization finished")

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
        _logger.info("Setting up new pika connection")
        self._pika_connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["edustor.rabbit.host"]))
