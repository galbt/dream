import boto3
import pandas as pd
import re
import os
import logging
import json

"""
This script emitates an AWS Glue job.
Since it runs without any AWS account, I have decided to use pandas as my data manipulation tool instead of AWS Glue/Spark.
When running on AWS, it can be easily integrated into Glue/Spark.
"""

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def concat_address(address):
    return f"{address['city']}, {address['street']}, {address['suite']}, {address['zipcode']}"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

minio_endpoint = "http://minio:6000"

s3_client = boto3.client('s3', endpoint_url=minio_endpoint, aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')
logger.info("S3 client successfully established")

bucket_name = "dream-data"
target_bucket = 'target'
file = "raw_data.json"

response = s3_client.get_object(Bucket=bucket_name, Key=file)
json_data = response['Body'].read().decode('utf-8')
df = pd.read_json(json_data)
logger.info("Source data retrieved successfully. Starting data transformations.")

#Check if email address is in a valid format and filter out invalid email addresses
df['is_email_valid'] = df['email'].apply(lambda x: is_valid_email(x))
df = df[df['is_email_valid']==True].drop(columns='is_email_valid')

#Convert id column to string
df['id'] = df['id'].astype(str)

#Extract domain from email address
df['email_domain'] = df['email'].str.extract(r'@(.+?)\.')

###### Data Transformation ######

#Aggregate the data by company name and count number of members
df['company_name'] = pd.json_normalize(df['company'])['name']
companies_count = df.groupby('company_name').agg({'id':'count'})
companies_count = companies_count.rename({"id": "count"}, axis=1)
df['members_in_company'] = df.merge(companies_count, how='inner', on='company_name')['count']
df = df.drop(columns='company_name', axis=1)

#Concatenate address properties from nested json into single column
df['full_address'] = df['address'].apply(lambda x: concat_address(x))

#Filter out users with less than 5 characters in their username
df = df[df.username.str.len()>=5]

logger.info(f"Finished data transformation. Dropping data to S3 on bucket {target_bucket}")

#Write df to S3 as parquet
df.to_parquet('data')
target_file = 'data.parquet'
s3_client.upload_file(Filename='data',Bucket=target_bucket, Key=target_file)
logger.info("Enriched data successfully loaded to bucket.")


