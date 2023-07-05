import boto3

ACCESS_KEY_ID = 'AKIA357LUDGC2QN3N2XY'
SECRET_ACCESS_KEY = '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'

session = boto3.Session(region_name='ap-northeast-1',
                        aws_access_key_id=ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY)
s3_client = session.client('s3')
s3 = session.resource("s3")
bucket_name = "mri-2d"

