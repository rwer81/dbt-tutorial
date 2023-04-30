FROM python:3.10-alpine

COPY . /home/dbt_works/

WORKDIR /home/dbt_works/

RUN pip3 install --no-cache-dir -r requirements.txt

ENV DBT_DIR /home/dbt_works/case_study/
ENV DBT_PROFILES_DIR=$DBT_DIR/profiles/

ENV PORT 8080
ENV HOST 0.0.0.0

WORKDIR /home/dbt_works/dbt_rest_api

CMD ["dbt"]
CMD ["python3", "main.py"]