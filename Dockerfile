FROM python:3.12-slim
LABEL authors="James Collings"
LABEL email="james@winkyjames.com"

WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential libsndfile1 \
 && python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install certifi \
 && export SSL_CERT_FILE="$(python -c 'import certifi; print(certifi.where())')" \
 && python -m pip install -r requirements.txt \
 && apt-get remove -y build-essential \
 && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
ENV SSL_CERT_FILE=/usr/local/lib/python3.12/site-packages/certifi/cacert.pem
CMD ["bash", "start.sh"]

ENTRYPOINT ["top", "-b"]