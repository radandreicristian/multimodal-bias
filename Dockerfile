FROM python:3.11.4

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install poetry==1.5.1 && \
    poetry config virtualenvs.create false && poetry install --without lint,test \

COPY src src
COPY run.sh run.sh

RUN chmod +x run.sh

CMD  ["./run.sh"]