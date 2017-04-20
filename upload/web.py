import json
import uuid

from flask import Flask, request, abort
from gridfs import GridFSBucket
from pymongo import MongoClient
from datetime import datetime
import pika

from commons_auth.decorator import requires_scope

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 ** 2

mongo = MongoClient()
gridfs = GridFSBucket(mongo['edustor-files'], bucket_name="pages-uploads")

rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters())
rabbit_channel = rabbit_connection.channel()


@app.route("/api/v1/upload/pages", methods=["POST"])
@requires_scope("upload")
def upload_pages():
    if "file" not in request.files:
        abort(400, "No file field in request")
    file = request.files["file"]
    upload_id = str(uuid.uuid4())
    # gridfs.upload_from_stream("upload-{}.pdf".format(upload_id), file.stream)

    event = {
        "upload_id": upload_id,
        "uploader_id": "",
        "timestamp": int(datetime.now().timestamp()),
        "targetLessonId": None
    }

    rabbit_channel.basic_publish("internal.edustor", "uploaded.pdf.pages.processing", json.dumps(event))

    return json.dumps({
        "upload_id": upload_id
    })
