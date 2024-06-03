import json
import os
import boto3
import requests
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_endpoint = 'http://minio:6000'
s3_client = boto3.client('s3', endpoint_url=s3_endpoint, aws_access_key_id=os.getenv('AWS_ACCESS_KEY'), aws_secret_access_key=os.getenv('AWS_ACCESS_KEY'))
logger.info("S3 client successfully established")

def lambda_handler(event, context):
    bucket_name = 'dream-data'
    try:
        api_url = 'https://jsonplaceholder.typicode.com/users'
        file_name = f'raw_data.json'
        response = requests.get(api_url)
        data = response.json()
        
    except Exception as e:
        logger.error(f'Error fetching data from API endpoint: {e}')
    
    try:
        s3_response = s3_client.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data)
        )

        logger.info(f"Data successfully written to bucket {bucket_name}")

        status_code = s3_response.get('ResponseMetadata').get("HTTPStatusCode")
        return {
            'statusCode': status_code,
            'body': json.dumps('Raw data file created successfully!')
        }
    
    except Exception as e:
        return {
            'statusCode': 404,
            'body': json.dumps(str(e))
        }
    
# # For testing & debugging    
if __name__ == "__main__":
    event = {}
    lambda_handler(event, "")
    
    





    

