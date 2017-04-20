import json
import uuid

from flask import Flask, request, abort
from gridfs import GridFSBucket
from pymongo import MongoClient
from datetime import datetime
import pika
import os

from commons_auth import requires_scope, auth

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 ** 2

mongo = MongoClient(os.environ["edustor.mongo.uri"])
gridfs = GridFSBucket(mongo['edustor-files'])

rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ["edustor.rabbit.host"]))
rabbit_channel = rabbit_connection.channel()


@app.route("/api/v1/upload/pages", methods=["POST"])
@requires_scope("upload")
def upload_pages():
    if "file" not in request.files:
        abort(400, "No file field in request")
    file = request.files["file"]
    upload_id = str(uuid.uuid4())
    gridfs.upload_from_stream("upload-{}.pdf".format(upload_id), file.stream)

    event = {
        "uuid": upload_id,
        "userId": auth.account_id,
        "timestamp": int(datetime.now().timestamp()),
        "targetLessonId": None
    }

    event_json = json.dumps(event)
    rabbit_channel.basic_publish(exchange="internal.edustor",
                                 routing_key="uploaded.pdf.pages.processing",
                                 body=event_json,
                                 properties=pika.BasicProperties(
                                     content_type='application/json'
                                 ))

    return event_json
