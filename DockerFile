FROM python:3-alpine

ADD dst.py /

RUN pip install docker

VOLUME [ "/data" ]

CMD [ "python", "./dst.py" ]