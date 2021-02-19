FROM python:3.7.3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


ENV PYTHONPATH=/usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

CMD [ "sh", "-c", "python -m kafka_streamprocessor"]
