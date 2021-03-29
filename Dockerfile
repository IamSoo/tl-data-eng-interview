FROM puckel/docker-airflow:1.10.9
USER root
RUN mkdir -p /usr/local/app/data
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN pip install requests
RUN pip install pandas
RUN pip install SQLAlchemy
RUN pip install numpy
COPY airflow_jobs/data/movies_metadata.csv /usr/local/app/data/movies_metadata.csv
