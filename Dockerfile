FROM python:3.10-slim-buster

RUN apt-get update -y && apt-get install curl -y

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -U appdynamics==22.10.0.5500 -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["pyagent", "run", "--use-manual-proxy", "gunicorn", "-b", "0.0.0.0:5000", "app:app"]