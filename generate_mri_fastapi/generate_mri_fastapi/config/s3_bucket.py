import boto3

ACCESS_KEY_ID = 'AKIA357LUDGC5DGX4S6G'
SECRET_ACCESS_KEY = '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'

session = boto3.Session(region_name='ap-northeast-1',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
s3_client = session.client('s3')
s3 = session.resource("s3")
bucket_name = "mri-2d"

