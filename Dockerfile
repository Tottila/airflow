# Base image
FROM python:3.7

# Airflow global variables
ARG AIRFLOW_VERSION=1.10.14
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Install airflow
RUN pip install apache-airflow[postgres,password]==${AIRFLOW_VERSION}
RUN pip install SQLAlchemy==1.3.23
RUN pip install markupsafe==2.0.1
RUN pip install wtforms==2.3.3
RUN pip install --upgrade setuptools

# Create directory for scripts
RUN mkdir /project

# Copy scripts and config file
COPY script/ /project/scripts/
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# Set permissions for the script
RUN chmod +x /project/scripts/init.sh

# Set entry point
ENTRYPOINT ["/project/scripts/init.sh"]

