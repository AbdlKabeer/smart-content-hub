import base64
import json
import uuid
import os
import logging
from .amazon_connect import AmazonS3
import pandas as pd 
from django.conf import settings
from boto3 import client
import boto3
import traceback
import uuid
from io import BytesIO
from tempfile import NamedTemporaryFile




class ManageAws:

    def __init__(self):
        self.aws_access_key = settings.AWS_ACCESS_KEY_ID
        self.aws_secret_key = settings.AWS_SECRET_ACCESS_KEY
        self.aws_bucket_region = settings.AWS_BUCKET_REGION
        self.aws_bucket_name = settings.AWS_BUCKET_NAME
        self.aws_uri = f"https://{self.aws_bucket_name}.s3.{self.aws_bucket_region}.amazonaws.com/"
        # https://idradar-bucket.s3.eu-west-2.amazonaws.com/logs/

    def aws_connect(self):
        try:
            aws = AmazonS3(
                self.aws_access_key,
                self.aws_secret_key,
                self.aws_bucket_region)
            return True, aws
        except Exception as e:
            traceback.format_exc()
            logging.error(e)
            return False, e
        
    def upload_file_to_s3(self, file_path, file_name):
        s3_client = boto3.client('s3')
        try:
            # Upload the file to S3
            logging.info(f"Uploading file {file_name} to AWS S3")
            s3_client.upload_file(file_path, self.aws_bucket_name, file_name)
            # Generate the link to the uploaded file
            s3_link = f'https://{self.aws_bucket_name}.s3.amazonaws.com/{file_name}'
            logging.info(f"File uploaded to AWS S3: {s3_link}")
            return True, s3_link
        except Exception as e:
            traceback.format_exc()
            logging.error(e)
            return False, f"Error uploading the file to S3: {e}"


    def display_object_bucket(self):
        try:
            status, aws = self.aws_connect()
            if status:
                bucket_content = aws.show_contents_s3_bucket(
                    self.aws_bucket_name)
                return True, bucket_content

        except Exception as e:
            return False, e

    def upload_object_aws(self, file_name, file_path, is_pdf=False):
        try:
            status, aws = self.aws_connect()
            if status:
                
                if is_pdf:
                    extention = 'application/pdf'
                else:
                    extention=file_name.split('.')[1]
                file_size = os.path.getsize(file_path)
                print(file_size)
                with open(file_path, 'rb') as data:
                    aws.push_data_to_s3_bucket(
                        self.aws_bucket_name,
                        data,
                        file_name,
                        file_size,
                        extention)
                self.delete_csv_file(file_path)
                return True, self.aws_uri + file_name
                
            
            return False , 'Server error'

        except Exception as e:
            traceback.format_exc()
            logging.error(e)
            return False, print(e)


    def delete_object_aws(self, aws_conn):
        try:
            status, aws = self.aws_connect()
            if status:
                aws_conn.delete_contents_s3_bucket("polygonai", "ebuka.jpeg")
                return True, "Successfully Deleted"

        except Exception as e:
            return False, print(e)

    def convert_pandas_to_csv(pd_data_df):

        try:
            df = pd.DataFrame(pd_data_df)
            filename = uuid.uuid4()
            filename = str(filename) + '.csv'
            df.to_csv(filename)
            return True, filename
        except Exception as e:
            return False, print(e)

    def delete_csv_file(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print("File has been deleted")
            else:
                print("File does not exist")
        except Exception as e:
            return False, print(e)

    def read_file(self, file_name):
        s3_obj = client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key
        )

        s3_clientobj = s3_obj.get_object(
            Bucket=self.aws_bucket_name,
            Key=file_name
        )
        s3_clientdata = s3_clientobj['Body'].read().decode('utf-8')

        return s3_clientdata



    def upload_object_byte_aws(self, file_name, file_data,is_base64=False , is_json=False ):

        if is_base64:
            # Decode base64 data to BytesIO
            try:
                file_data = BytesIO(base64.b64decode(file_data))
            except Exception as e:
                logging.error(f"Error decoding base64 data: {e}")
                return False, "Invalid base64 data"
            
        if is_json:
            try:
                file_data = BytesIO(json.dumps(file_data).encode('utf-8'))
            except Exception as e:
                logging.error(f"Error encoding JSON data: {e}")
                return False, "Invalid JSON data"
        

        try:
            status, aws = self.aws_connect()
            if status:
                # Check if file_data is BytesIO
                if isinstance(file_data, (bytes, bytearray,BytesIO)):
                    # Save the file data from BytesIO to a temporary file

                    if isinstance(file_data,bytes):
                        file_size = len(file_data) 
                        aws.push_data_to_s3_bucket(
                            self.aws_bucket_name,
                            BytesIO(file_data),
                            file_name,
                            file_size,
                            file_name.split('.')[-1]
                        )
                    else:
                        with NamedTemporaryFile(delete=False) as temp_file:
                            temp_file.write(file_data.getvalue())
                            temp_file_name = temp_file.name
                            print(temp_file_name)
                        file_size = os.path.getsize(temp_file_name)
                        with open(temp_file_name, 'rb') as data:
                            aws.push_data_to_s3_bucket(
                                self.aws_bucket_name,
                                data,
                                file_name,
                                file_size,
                                file_name.split('.')[1])
                else:
                    file_size = os.path.getsize(file_data)
                    with open(file_data, 'rb') as data:
                        aws.push_data_to_s3_bucket(
                            self.aws_bucket_name,
                            data,
                            file_name,
                            file_size,
                            file_name.split('.')[1])
                
                # Make sure to correct the variable name from file_path to file_data
                self.delete_csv_file(file_data)  
                print("Image uploaded to S3 successfully. S3 URL:", self.aws_uri + file_name)
                return True, self.aws_uri + file_name
            
            return False , 'Server error'

        except Exception as e:
            traceback.format_exc()
            logging.error(e)
            return False, str(e)

