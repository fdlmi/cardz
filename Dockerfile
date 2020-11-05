FROM python:alpine

RUN mkdir /app
RUN mkdir /app/cardz
COPY cardz_api.py requirements.txt setup.py /app/
COPY cardz /app/cardz
WORKDIR /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "cardz_api:app", "-b:8080"]
