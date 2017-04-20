import json

from flask import Flask, request, abort

from commons_auth import requires_scope, auth
from upload.internal import handle_upload

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 ** 2


@app.route("/api/v1/upload/pages", methods=["POST"])
@requires_scope("upload")
def upload_pages():
    if "file" not in request.files:
        abort(400, "No file field in request")
    file = request.files["file"]
    event = handle_upload(auth.account_id, file)
    return json.dumps(event)
