FROM python:3.6
WORKDIR /code

ADD requirements.txt /code
RUN pip3 install -r requirements.txt

ADD . /code

CMD uwsgi --http :9090 --wsgi-file main.py --callable app --master --stats :9191