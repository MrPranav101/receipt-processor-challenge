FROM python:3.11-slim-buster

LABEL maintainer="Pranav Bhasin <pranav.bhasin07@gmail.com>"

ENV PYTHONUNBUFFERED=1

WORKDIR /source

RUN mkdir /source/receipt_processor

ADD . /source/receipt_processor


RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /source/receipt_processor/requirements.txt


CMD [ "uvicorn", "receipt_processor.api.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]