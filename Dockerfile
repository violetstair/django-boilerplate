FROM python:3.8

ENV PYTHONUNBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update && apt-get -y install \
    libpq-dev \
    postgresql

RUN mkdir /code
WORKDIR /code
COPY pyproject.toml poetry.lock ./

RUN pip install -U pip && pip install poetry && poetry config virtualenvs.create false --local
RUN poetry install

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh .
RUN chmod 755 wait-for-it.sh

ENTRYPOINT [ "tail", "-f" ]
