#FROM python:3.7-alpine
# RUN mkdir client
# WORKDIR /client
# ENV FLASK_ENV=development
# ENV FLASK_APP=client.py

# RUN pip install pipenv
# RUN pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy
# COPY /entrypoint.sh /entrypoint.sh
# ENTRYPOINT ["/entrypoint.sh"]
# CMD flask run


FROM python:3.7-alpine

WORKDIR /code
#VOLUME /var/run/docker.sock:/var/run/docker.sock
ENV FLASK_APP client.py
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run"]
