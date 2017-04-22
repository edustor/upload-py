import json
import uuid
from datetime import datetime

import pika
from gridfs import GridFSBucket

from upload import mongo, pika_connection_manager

gridfs = GridFSBucket(mongo['edustor-files'])


def handle_upload(uploader_id, data):
    upload_id = str(uuid.uuid4())

    event = {
        "uuid": upload_id,
        "userId": uploader_id,
        "timestamp": int(datetime.now().timestamp()),
        "targetLessonId": None
    }

    event_json = json.dumps(event)
    channel = pika_connection_manager.get_channel()

    gridfs.upload_from_stream("upload-{}.pdf".format(upload_id), data)
    channel.basic_publish(exchange="internal.edustor",
                          routing_key="uploaded.pdf.pages.processing",
                          body=event_json,
                          properties=pika.BasicProperties(
                              content_type='application/json'
                          ))
    channel.close()

    return event
