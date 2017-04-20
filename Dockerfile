FROM python:3.6
WORKDIR /code

ADD requirements.txt /code/
ADD commons_auth/requirements.txt /code/commons_auth/

RUN pip3 install -r requirements.txt -r commons_auth/requirements.txt

ADD . /code

CMD uwsgi --http :8080 --wsgi-file main.py --callable app --master --need-app --stats :8081