"""Define singletons objects for django app."""
import os
from pumpwood_communication.microservices import PumpWoodMicroService
from pumpwood_kong.kong import KongManagement
from pumpwood_flaskmisc.storage import PumpWoodStorage
from pumpwood_flaskmisc.rabbitmq import PumpWoodRabbitMQ

###############################
# Microsservice configuration #
MICROSERVICE_NAME = os.environ.get("MICROSERVICE_NAME")
MICROSERVICE_URL = os.environ.get("MICROSERVICE_URL")
MICROSERVICE_USERNAME = os.environ.get("MICROSERVICE_USERNAME")
MICROSERVICE_PASSWORD = os.environ.get("MICROSERVICE_PASSWORD")
microservice = PumpWoodMicroService(
    name=MICROSERVICE_NAME, server_url=MICROSERVICE_URL,
    username=MICROSERVICE_USERNAME, password=MICROSERVICE_PASSWORD,
    verify_ssl=False)
microservice__no_login = PumpWoodMicroService(
    name=MICROSERVICE_NAME, server_url=MICROSERVICE_URL,
    verify_ssl=False)

##########################
# RabbitMQ configuration #
username = os.getenv('RABBITMQ_USERNAME')
password = os.getenv('RABBITMQ_PASSWORD')
host = os.getenv('RABBITMQ_HOST')
port = int(os.getenv('RABBITMQ_PORT'))
# rabbitmq_api = PumpWoodRabbitMQ(
#     queue="ncr-app--dataloader",
#     username=username, password=password,
#     host=host, port=port)

##################
# Storage Object #
storage_type = os.environ.get('STORAGE_TYPE')
bucket_name = os.environ.get('STORAGE_BUCKET_NAME')
base_path = os.environ.get('STORAGE_BASE_PATH')
folder_path = os.environ.get('STORAGE_LOCAL_PATH')
storage_object = PumpWoodStorage(
    storage_type=storage_type, bucket_name=bucket_name,
    base_path=base_path, folder_path=folder_path)
