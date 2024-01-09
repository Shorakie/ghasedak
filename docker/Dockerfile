# Pull official base image
FROM python:3.10-slim as base

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional

# Install dependencies
COPY ./requirements ./requirements
RUN pip install --upgrade pip

# Copy entrypoint.sh
COPY ./docker/entrypoint /entrypoint
RUN chmod +x /entrypoint

COPY . /app/

FROM base as Prod
RUN pip install -r ./requirements/prod.txt
ENV ENVIRONMENT prod
ENTRYPOINT [ "/app/entrypoint" ]

FROM base as dev
ENV ENVIRONMENT dev
RUN pip install -r ./requirements/dev.txt
