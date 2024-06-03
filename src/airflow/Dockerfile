# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV AIRFLOW_HOME=/usr/local/airflow
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        libldap2-dev \
        libsasl2-dev \
        libkrb5-dev \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Airflow with extras
RUN pip install --upgrade pip \
    && pip install 'apache-airflow[docker,redshift]'

# Initialize Airflow database
RUN airflow db init

# Create an Airflow admin user
RUN airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin

# Expose the webserver and scheduler ports
EXPOSE 8080 8793

# Start Airflow
CMD ["bash", "-c", "airflow scheduler & airflow webserver --port 8080"]