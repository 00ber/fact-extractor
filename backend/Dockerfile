FROM python:3.11.9-slim-bullseye

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src/* ./

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

