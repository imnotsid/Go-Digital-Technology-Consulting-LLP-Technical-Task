import boto3
import pandas as pd
from sqlalchemy import create_engine

# Initialize boto3 clients
s3_client = boto3.client('s3')
glue_client = boto3.client('glue')

# Parameters
bucket_name = 'your-s3-bucket-name'
file_key = 'your-file-key'
rds_endpoint = 'your-rds-endpoint'
rds_dbname = 'your-db-name'
rds_username = 'your-username'
rds_password = 'your-password'
glue_database = 'your-glue-database'
glue_table = 'your-glue-table'

def read_from_s3(bucket, key):
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    data = pd.read_csv(obj['Body'])
    return data

def push_to_rds(data):
    try:
        engine = create_engine(f'mysql+pymysql://{rds_username}:{rds_password}@{rds_endpoint}/{rds_dbname}')
        data.to_sql('your_table', engine, if_exists='replace', index=False)
    except Exception as e:
        print(f'Error pushing to RDS: {e}')
        return False
    return True

def push_to_glue(data):
    # Assuming the Glue Table has the same structure as the DataFrame
    response = glue_client.put_table(
        DatabaseName=glue_database,
        TableInput={
            'Name': glue_table,
            'StorageDescriptor': {
                'Columns': [{'Name': col, 'Type': 'string'} for col in data.columns],
                'Location': f's3://{bucket_name}/glue/',
                'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
                'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
                'Compressed': False,
                'NumberOfBuckets': -1,
                'SerdeInfo': {
                    'SerializationLibrary': 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe',
                    'Parameters': {'serialization.format': '1'}
                },
            },
            'TableType': 'EXTERNAL_TABLE'
        }
    )
    # Writing the data to S3 as CSV for Glue to read
    data.to_csv(f's3://{bucket_name}/glue/{glue_table}.csv', index=False)
    return response

def lambda_handler(event, context):
    data = read_from_s3(bucket_name, file_key)
    if not push_to_rds(data):
        push_to_glue(data)