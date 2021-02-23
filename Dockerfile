# Use an official Python runtime based on Debian 10 "buster" as a parent image.
FROM python:3.8.1-slim-buster

# NOTE this Dockerfile borrowed from a Wagtail project.

# Add user that will be used in the container.
RUN useradd ginkgo

# Ports used by this container to serve HTTP.
EXPOSE 80
EXPOSE 443

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
ENV PYTHONUNBUFFERED=1 \
    PORT=80

# Install system packages.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    nginx \
    procps \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install -U uwsgi
RUN mkdir /run/uwsgi
RUN chown ginkgo:ginkgo /run/uwsgi

ADD deployment/favicon.ico /srv/favicon.ico
ADD deployment/robots.txt /srv/robots.txt

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

COPY deployment/docker-entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# Set this directory to be owned by the "ginkgo" user. This Ginkgo project
# uses SQLite, the folder needs to be owned by the user that
# will be writing to the database file.
RUN chown ginkgo:ginkgo /app

# Copy the source code of the project into the container.
COPY --chown=ginkgo:ginkgo . .

# Use user "ginkgo" to run the build commands below and the server itself.
USER ginkgo

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

USER root

CMD ["uwsgi", "--socket", "/run/uwsgi/uwsgi.sock", "--module", "conf.wsgi", "--chmod-socket=600", "--uid=ginkgo", "--master"]

COPY deployment/nginx.conf /etc/nginx/nginx.conf
