FROM python:3.8-buster

####################################################################
# Add a suffix to all end-point so more than one microservice of one
# type can coexist in same cluster
ENV ENDPOINT_SUFFIX=""
ENV HASH_SALT="pumpwood-auth"
####################################################################

ENV CLOUD="TRUE"
ENV PYTHONUNBUFFERED="1"

# Database
ENV PGSSLMODE="allow"
ENV DB_DATABASE="pumpwood"
ENV DB_USERNAME="pumpwood"
ENV DB_PASSWORD="pumpwood"
ENV DB_HOST="test-db-pumpwood-auth"
ENV DB_PORT="5432"
ENV N_WORKERS="20"
ENV SIGNUP = "FALSE"

# Microservice
ENV MICROSERVICE_NAME='microservice-auth'
ENV MICROSERVICE_NOLOGIN_NAME="microservice-auth_nologin"
ENV MICROSERVICE_URL="http://load-balancer:8000/"
ENV MICROSERVICE_USERNAME='microservice-auth'
ENV MICROSERVICE_PASSWORD='microservice-auth'
ENV MICROSERVICE_SSL='False'

# RabbitMQ
ENV RABBITMQ_USERNAME="pumpwood"
ENV RABBITMQ_PASSWORD="pumpwood"
ENV RABBITMQ_HOST="rabbitmq-main"
ENV RABBITMQ_PORT="5672"

# Cloud
ENV SERVICE_URL="http://pumpwood-auth-app:5000/"
ENV API_GATEWAY_URL="http://load-balancer:8001/"
ENV AUTH_STATIC_SERVICE="http://pumpwood-auth-admin-static:5000/"
ENV TEST_RELOADDB_SERVICE="http://test-db-pumpwood-auth:5000/"

# Storage
ENV GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/key-storage.json
ENV STORAGE_TYPE="local"
ENV STORAGE_BASE_PATH="pumpwood-auth-app"
ENV STORAGE_LOCAL_PATH="media/"
ENV PYTHONUNBUFFERED="1"

COPY requirements/requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN apt-get update
RUN apt-get install -y postgresql-client

COPY codes /codes
WORKDIR /codes/

CMD ["bash", "/codes/start_server.sh"]
