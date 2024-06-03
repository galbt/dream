import unittest
from unittest.mock import patch, MagicMock
import json
import os
from moto import s3
import boto3
import sys
from pathlib import Path

# Add the lambda_function directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'api_to_s3_lambda'))

from api_to_s3_lambda.lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    def test_lambda_handler(self, mock_requests_get):
        # Set up the mock S3 environment
        s3 = boto3.client('s3', endpoint_url='http://minio:6000', aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')
        response = s3.create_bucket(Bucket='test')
        response_status_code = response['ResponseMetadata'].get("HTTPStatusCode")
        self.assertEqual(response_status_code, 200)

        # Run the lambda function
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Assertions to verify the lambda function behavior
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Raw data file created successfully!', response['body'])

        # Verify the S3 object
        s3_response = s3.get_object(Bucket='dream-data', Key='raw_data.json')
        self.assertEqual(s3_response['ResponseMetadata'].get("HTTPStatusCode"), 200)

if __name__ == '__main__':
    unittest.main()
