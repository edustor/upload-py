from flask import Flask
from commons_auth.decorator import requires_scope
app = Flask(__name__)


@app.route("/api/v1/upload/pages", methods=["POST"])
@requires_scope("upload2", "internal")
def upload_pages():
    return "OK"
