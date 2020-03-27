#It's no longer used
FROM python:3.7-alpine

WORKDIR /code

ENV FLASK_APP client.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add curl
COPY templates/ /code/templates
COPY client.py /code/
COPY REPORTS/ /code/
COPY generated_dags/ /code/

CMD ["flask", "run"]
