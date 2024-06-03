import json
import boto3
import pyarrow.parquet as pq
from io import BytesIO
import psycopg2
from sqlalchemy import create_engine
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

source_endpoint = 'http://minio:6000'
s3_client = boto3.client('s3', endpoint_url=source_endpoint, aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')
logger.info("S3 client successfully established")

source_bucket = 'target' #Ironically funny
file_key='data.parquet'

redshift_host = 'redshift'
redshift_port = 5432
redshift_db = 'postgres'
redshift_user = 'admin'
redshift_password = 'admin'

def get_source_data():
    response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
    parquet_bytes = response['Body'].read()
    logger.info("Successfully retrieved source data")
    
    # Load Parquet file into pandas DataFrame
    parquet_file = BytesIO(parquet_bytes)
    return pq.read_table(parquet_file).to_pandas()

def prepare_data(data):
    try:
        df = data
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, dict)).all():
                df[col] = df[col].apply(json.dumps)
        logger.info("Successfully prepared data to load to S3")
    except Exception as e:
        logger.error(f"Error preparing data to load. Error: {e}")


def data_to_redshift(data, table_name='data_from_api'):
    try:
        conn = psycopg2.connect(host=redshift_host, port=redshift_port, database=redshift_db, user=redshift_user, password=redshift_password)
        engine = create_engine(f'postgresql://{os.getenv('REDSHIFT_USER')}:{os.getenv('REDSHIFT_USER')}@redshift:5432/postgres')
        logger.info("Redshift connection established successfully.")
    except Exception as e:
        logger.error(f"Failed to establish connection to Redshift. Error: {e}")

    try:
        status_code = data.to_sql(table_name, engine, if_exists='replace', index=True)
        conn.commit()
    except Exception as e:
        logger.error(f"Error while loading data to Redshift. Error: {e}")

    logger.info("Successfully loaded data to redshift")
    return status_code
    
def lambda_handler(event, context):
    df = get_source_data()
    prepare_data(df)
    status_code = data_to_redshift(df, 'api_transformed_data')
    if status_code == 9:
        return {
            'statusCode': status_code,
            'body': json.dumps('Enriched data inserted successfully')
        }
    else:
        return {
            'statusCode': status_code,
            'body': json.dumps('Error while loading data to Redshift. Check DB connection.')
        }

#For testing & debugging    
if __name__ == "__main__":
    event = {}
    lambda_handler(event, "")
    
    





    

