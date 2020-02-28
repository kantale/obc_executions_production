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

COPY * /code/

RUN mkdir generated_dags
#RUN mkdir generated_dags/wf
#RUN mkdir generated_dags/tool
RUN mkdir compressed_logs

CMD ["flask", "run"]
