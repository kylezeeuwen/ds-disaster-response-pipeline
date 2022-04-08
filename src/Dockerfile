FROM python:3.9

# System setup
RUN apt-get update \
  && apt-get dist-upgrade -y \
  && apt-get install -y --no-install-recommends \
    git \
    ssh-client \
    software-properties-common \
    make \
    build-essential \
    ca-certificates \
    libpq-dev \
    nodejs \
    npm \
  && apt-get clean \
  && rm -rf \
    /var/lib/apt/lists/* \
    /tmp/* \
    /var/tmp/*

# Env vars
ENV PYTHONIOENCODING=utf-8
ENV LANG=C.UTF-8

# Update python
RUN python -m pip install --upgrade pip setuptools wheel --no-cache-dir

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# predownload the nltk assets
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4

COPY . /usr/app/

# TODO this should be done in a seperate container

#WORKDIR /usr/app/react-web
#RUN npm install
#RUN npm run build
#RUN rm -r /usr/app/react-web/node_modules
#RUN cp -r /usr/app/react-web/build /react-web

# Set docker basics
WORKDIR /usr/app/
ENTRYPOINT ["python", "-u"]
CMD ["main.py"]