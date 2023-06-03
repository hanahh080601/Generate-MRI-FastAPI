from config.s3_bucket import s3, s3_client, bucket_name
from PIL import Image
import io, os

def check_data_s3_available(dataset, contrast):
    try:
        list_objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix =f'{dataset}/test/{contrast}')
        return True
    except Exception as e:
        print("Exception in getting data devices from S3: ", e)
        return False
    
def get_data(dataset, contrast):
    if check_data_s3_available(dataset, contrast):
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix =f'{dataset}/test/{contrast}')
        return [obj['Key'].split('/')[-1] for obj in objects['Contents']]
    
def get_image_by_filename(dataset, contrast, filename):
    if check_data_s3_available(dataset, contrast):
        obj = s3_client.get_object(Bucket=bucket_name, Key=f'{dataset}/test/{contrast}/{filename}')
        return Image.open(io.BytesIO(obj['Body'].read()))
    
def push_s3(image_path):
    try:
        s3_client.upload_file(image_path, bucket_name, f'generate/{image_path}')
        print("Done Push Data to S3 Bucket")
        return os.path.join(bucket_name, f'generate/{image_path}')
    except Exception as e:
        print(f"Failed push to S3: {e}")
        return None