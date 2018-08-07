FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY Pipfile Pipfile
RUN pipenv install --system -d --skip-lock
COPY . /code
