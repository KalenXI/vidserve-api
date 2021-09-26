FROM tiangolo/uvicorn-gunicorn-fastapi:latest

COPY . /app

RUN pip install -r /app/requirements.txt
RUN apt update
RUN apt install ffmpeg -y