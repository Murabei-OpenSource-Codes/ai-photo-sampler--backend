import os

# Os servidores locais são os end points, servem as
# aplicações que não precisam de outros servidores
django_db_name = os.environ.get('DB_DATABASE')
django_db_username = os.environ.get('DB_USERNAME')
django_db_pass = os.environ.get('DB_PASSWORD')
django_db_host = os.environ.get('DB_HOST')
django_db_port = os.environ.get('DB_PORT')

DEBUG = os.environ.get('DEBUG', 'TRUE') == 'TRUE'
ADMINS = (
)

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # Or path to database file if using sqlite3.
        'NAME': django_db_name,
        # Not used with sqlite3.
        'USER': django_db_username,
        # Not used with sqlite3.
        'PASSWORD': django_db_pass,
        # Set to empty string for localhost. Not used with sqlite3.
        'HOST': django_db_host,
        # Set to empty string for default. Not used with sqlite3.
        'PORT': django_db_port,
    }
}
ALLOWED_HOSTS = ('*')

# Storage Config.
storage_type = os.environ.get('STORAGE_TYPE')
if storage_type == "aws_s3":
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIAFILES_LOCATION = ''

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = (
        '{aws_storage_bucket_name}.s3.amazonaws.com').format(
            aws_storage_bucket_name=AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"
elif storage_type == "google_bucket":
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.environ.get('STORAGE_BUCKET_NAME')
