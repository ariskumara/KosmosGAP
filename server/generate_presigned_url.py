import json
import logging
import boto3
import botocore
import requests

from botocore.exceptions import ClientError
def create_presigned_url(bucket_name, object_name, expiration=600):
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',region_name="us-east-1",config=boto3.session.Config(signature_version='s3v4',))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        logging.error(e)
        return "Error"
    # The response contains the presigned URL
    return response
    
def lambda_handler(event, context):

    url = create_presigned_url('kosmosgapbucket','kosmos-android-installer.apk',3600)
    print(url)  
    data = {'url': url}
    
    payload=requests.post('https://cleanuri.com/api/v1/shorten',data=data)
    short_url=payload.json()['result_url']
    print("The short url is : {}".format(short_url))
