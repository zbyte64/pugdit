FROM python:3.6

# install nodejs
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install binutils postgresql-client libevent-dev curl

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -yqq nodejs
RUN apt-get clean -y

# install project deps
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install pipenv
COPY Pipfile Pipfile
RUN pipenv install --system -d --skip-lock

COPY . /code

# compile client
WORKDIR /code/pugboat
RUN npm install -g yarn
RUN yarn install
RUN yarn build

WORKDIR /code
# RUN ./manage.py collectstatic --noinput

EXPOSE 8000
