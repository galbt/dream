Instructions for how to set up the ETL pipeline:
1. navigate to src/airflow
2. Run 'docker-compose up'
3. Open Airflow (http://localhost:8080 from outside: http://airflow-webserver:8080)
4. Enter credentials (airflow:airflow)
5. Run DAG 'api_to_redshift'.

FYI
* In this pipline i simulate AWS S3 services using minio image.
* I simulate AWS Redshift services using the official postgres image
  since Redshift services are only available through a real AWS environment.
* I couldn't find a way to dockerize an image of AWS Glue so I used pandas for the data transformations.
* The 1st lambda that fetches data from the API is called api_to_s3_lambda.
* The 2nd lambda that drops the transformed data to Redshift is called s3_to_redshift_lambda.
* The script for the Glue job is in airflow/scripts/glue_job.py.
* I did write unit tests for the lambdas and Glue job but I just didn't have enought time to run them and get them to work 100%.


This is just a basic pipeline which through time could be improved (classes,functions, connectors, etc).

Boaz,
I learned so much while preparing this task (ommiting the amount of hours that took me to complete this),
so even if this pipeline is not 100% of what was expected, I still want to thank you for this opportunity. I truly did my best.

Gal Ben-Tovim