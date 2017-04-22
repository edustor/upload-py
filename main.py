import logging

logging.basicConfig(level=logging.WARN, format='{asctime} {levelname} --- {name:<30} : {message}', style="{")

for logger_name in ["edustor_upload", "werkzeug"]:
    logging.getLogger(logger_name).setLevel(logging.INFO)

if __name__ == '__main__':
    from edustor_upload.web import app
    app.run(host="0.0.0.0")
