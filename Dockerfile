FROM python:3-alpine

WORKDIR /usr/src/app

COPY . .

CMD python ./py-offline.py