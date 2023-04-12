#!/usr/bin/env bash

# Switch to PostgreSQL
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://postgres:postgres@postgres:5432/airflow

# Initialize Airflow database
# airflow db init
airflow upgradedb

# Create admin user in Airflow with password admin
airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start Airflow scheduler and webserver
airflow scheduler & airflow webserver
