FROM python:3.9-slim-bullseye

USER root

WORKDIR /multilingo_ai

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8010

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]