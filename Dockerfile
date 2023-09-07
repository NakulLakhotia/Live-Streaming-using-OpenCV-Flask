FROM python:latest

WORKDIR /service

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

EXPOSE 8200

CMD ["python", "app.py"]