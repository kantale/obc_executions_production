FROM python:3.7-alpine


COPY . /usr/local
WORKDIR /usr/local

RUN pip install -r requirements.txt
ENV FLASK_ENV=development
ENV FLASK_APP=client.py
EXPOSE 5000
CMD flask run