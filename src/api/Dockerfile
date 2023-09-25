FROM python:3.8-slim-buster

ENV PYENV_SHELL=/bin/bash

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends build-essential git && \
    useradd -ms /bin/bash app -d /home/app -G sudo -u 2000 -p "$(openssl passwd -1 Passw0rd)" && \
    mkdir -p /app && \
    chown app:app /app && \
    pip install --no-cache-dir --upgrade pip && \
    pip install pipenv

EXPOSE 5000

USER app
WORKDIR /app

COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install

COPY . ./

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "pipenv run gunicorn app:app -b 0.0.0.0:5000"]

