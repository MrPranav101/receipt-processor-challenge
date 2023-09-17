FROM python:3.9

LABEL maintainer="Pranav Bhasin <pranav.bhasin07@gmail.com>"

ENV PYTHONUNBUFFERED=1

WORKDIR /source

RUN mkdir /source/src

ADD . /source/src


RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /source/src/requirements.txt

RUN rm -rf /root/.ssh/


CMD [ "uvicorn", "receipt_processor.api.app:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]