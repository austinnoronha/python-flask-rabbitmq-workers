# Dockerfile
FROM python:3.9.10-alpine
WORKDIR /code
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code
EXPOSE 5000
COPY . .
CMD [ "python", "main.py" ]