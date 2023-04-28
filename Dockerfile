ARG dbt_project_name=case_study

FROM python:3.10-alpine

RUN adduser --disabled-password dbt &&\
    mkdir /dbt &&\
    chown dbt:dbt /dbt

USER dbt

RUN pip3 install --upgrade pip
RUN pip3 install dbt-bigquery
RUN pip3 install flask

ENV DBT_DIR /dbt
ENV DBT_PROFILES_DIR=/dbt/$dbt_project_name/profiles/
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/app/auth/gcp-service-account.json???
ENV PORT 8080

COPY ./$dbt_project_name /dbt

WORKDIR $DBT_DIR/dbt_rest_api

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]