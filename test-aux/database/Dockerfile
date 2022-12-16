FROM andrebaceti/regen-timescale-db:0.4-1.7.5-pg12

ENV POSTGRES_PASSWORD pumpwood
ENV POSTGRES_USER pumpwood
ENV POSTGRES_DB pumpwood
ENV APP_NAME pumpwood-auth-app
ENV POSTGRES_EXTRA_ARGS="-c max_connections=1000 -c work_mem=50MB -c shared_buffers=4GB -c maintenance_work_mem=2GB -c max_locks_per_transaction=500 -c max_locks_per_transaction=500 -c synchronous_commit=off -c max_wal_size=20GB -c min_wal_size=80MB -c effective_io_concurrency=200 -c max_worker_processes=50"

EXPOSE 8540:5432

COPY db_dump/database.sql /docker-entrypoint-initdb.d/AAA__database.sql
RUN chmod 777 -R /docker-entrypoint-initdb.d/
