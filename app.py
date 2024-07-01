import boto3
import pandas as pd
from sqlalchemy import create_engine

# Your AWS credentials and configurations
AWS_ACCESS_KEY = 'YOUR_AWS_ACCESS_KEY'
AWS_SECRET_KEY = 'YOUR_AWS_SECRET_KEY'
S3_BUCKET = 'YOUR_S3_BUCKET'
RDS_ENDPOINT = 'YOUR_RDS_ENDPOINT'
RDS_DATABASE = 'YOUR_RDS_DATABASE'
RDS_USER = 'YOUR_RDS_USER'
RDS_PASSWORD = 'YOUR_RDS_PASSWORD'

def read_from_s3(bucket, key):
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])

def push_to_rds(df):
    try:
        engine = create_engine(f'postgresql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}/{RDS_DATABASE}')
        df.to_sql('table_name', engine, if_exists='replace')
        print("Data pushed to RDS successfully.")
    except Exception as e:
        print(f"Failed to push data to RDS: {e}")
        push_to_glue(df)

def push_to_glue(df):
    # Add logic to push data to AWS Glue
    print("Data pushed to Glue successfully.")

if __name__ == "__main__":
    df = read_from_s3(S3_BUCKET, 'your-file-key.csv')
    push_to_rds(df)
