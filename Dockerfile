ARG dbt_project_name=dbt_works

FROM python:3.10-alpine

WORKDIR dbt_project_name

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV DBT_DIR $dbt_project_name/case_study
ENV DBT_PROFILES_DIR=/dbt/$dbt_project_name/profiles/
ENV GOOGLE_APPLICATION_CREDENTIALS=/usr/app/auth/gcp-service-account.json
ENV PORT 8080

WORKDIR dbt_project_name/dbt_rest_api

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]