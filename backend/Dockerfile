FROM python:3.10-slim

RUN apt update && \
    apt install -y libpq-dev python3-dev build-essential && \
    pip install psycopg2 && \
    apt purge -y python3-dev build-essential --autoremove

COPY requirements.txt /

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY plants_api/ /plants_api/

RUN echo "cd plants_api/db" > /entrypoint.sh && \
    echo "alembic upgrade head" >> /entrypoint.sh && \
    echo "if [ $? = 0 ]; then echo 'Database schema syncronized'; else echo 'alembic upgrade has failed, database state is not determined'; exit 1; fi" >> /entrypoint.sh && \
    echo "cd /" >> /entrypoint.sh && \
    echo "python3 -m plants_api" >> /entrypoint.sh

ENTRYPOINT ["/bin/sh"]
CMD ["/entrypoint.sh"]
