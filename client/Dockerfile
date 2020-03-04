FROM python:3.7-alpine
ADD VERSION .

EXPOSE 5000

WORKDIR /code

ENV FLASK_APP client.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV development
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY client.py /code/
COPY REPORTS/ /code/
COPY generated_dags/ /code/
#COPY compressed_logs/ /code/

#RUN mkdir generated_dags
#RUN mkdir compressed_logs
CMD ["flask", "run"]
