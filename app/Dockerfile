FROM python:3.8.3-slim-buster
COPY . /app
WORKDIR /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "flask", "run", "--host=0.0.0.0"]