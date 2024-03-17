FROM python:3.8-slim


RUN pip3 install shiny  numpy gunicorn faicons shared  seaborn pandas

WORKDIR /app

EXPOSE 8000

COPY ./app.py .
COPY ./shared.py .
COPY ./styles.css .
COPY ./inflation.csv .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
