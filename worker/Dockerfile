# Dockerfile
FROM python:3.9.10-alpine
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install mongoengine
COPY . /code
CMD [ "python", "worker.py" ]