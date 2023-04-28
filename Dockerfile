ARG dbt_project_name=case_study

FROM python:3.10-alpine

RUN adduser dbt &&\
RUN mkdir /dbt &&\
RUN mkdir /rest_api &&\
RUN chown dbt:dbt /dbt &&\
RUN chown dbt:dbt /rest_api &&\

USER dbt

RUN pip3 install --upgrade pip
RUN pip3 install dbt-bigquery
RUN pip3 install flask

ENV DBT_DIR /dbt
ENV DBT_PROFILES_DIR=/dbt/$dbt_project_name/profiles/
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/app/auth/gcp-service-account.json???

COPY ./$dbt_project_name /dbt

WORKDIR $DBT_DIR

CMD ["dbt"]