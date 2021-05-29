FROM python:3.8-slim

ENV PROJECT_DIR ml-api-fastapi
WORKDIR /${PROJECT_DIR}
ADD requirements_prod.txt /${PROJECT_DIR}/
ADD .env /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install apt-utils gcc libopencv-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements_prod.txt

COPY ./app/ /${PROJECT_DIR}/app/
COPY ./models/ /${PROJECT_DIR}/models/


ENV LOG_LEVEL DEBUG
ENV LOG_FORMAT TEXT

COPY ./run.sh /${PROJECT_DIR}/run.sh
RUN chmod +x /${PROJECT_DIR}/run.sh
CMD [ "./run.sh" ]