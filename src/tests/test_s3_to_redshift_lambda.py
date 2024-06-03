import unittest
from unittest.mock import patch
import boto3
import pandas as pd
from pathlib import Path
import sys

# Add the lambda_function directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent / 's3_to_redshift_lambda'))
from s3_to_redshift_lambda.lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('boto3.client')
    def test_get_source_data(self, mock_boto3_client):
        # Mock S3 client and its response
        s3 = boto3.client('s3', endpoint_url='http://minio:6000', aws_access_key_id='minioadmin', aws_secret_access_key='minioadmin')
        response = s3.create_bucket(Bucket='test')
        response_status_code = response['ResponseMetadata'].get("HTTPStatusCode")
        self.assertEqual(response_status_code, 200)
        s3.drop_bucket(Bucket='test')

        # Call the lambda function
        df = lambda_handler.get_source_data()

        # Assertions
        self.assertIsInstance(df, pd.DataFrame)

    def test_data_to_redshift(self):
        # Create a DataFrame for testing
        data = pd.DataFrame({'test_1': [1, 2, 3], 'test_2': ['a', 'b', 'c']})

        # Call the lambda function
        status_code = lambda_handler.data_to_redshift(data, 'test')

        # Assertions
        self.assertEqual(status_code, 9)

# Run the tests if the script is executed directly
if __name__ == '__main__':
    unittest.main()
