import logging
import os

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name="eu-central-1",
    config=boto3.session.Config(signature_version="s3v4"),
)
bucket_name = os.getenv("AWS_BUCKET_NAME")
download_path = "downloads/"


def download_file(file_name, file_extension="mp3"):
    """Download a file from an S3 bucket

    :param file_name: File to download
    :return: True if file was downloaded, else False
    """

    print("Downloading file", file_name, "from bucket", bucket_name)
    # if directory doesn't exist, create it
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    # create directory with file name
    os.makedirs(f"{download_path}/{file_name}", exist_ok=True)
    with open(f"{download_path}/{file_name}/original.{file_extension}", "wb") as f:
        try:
            s3.download_fileobj(bucket_name, file_name, f)
        except ClientError as e:
            logging.error(e)
            return False
        return True


def upload_file(file_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """

    # Use file name as object name
    object_name = os.path.basename(file_name)

    # Upload the file
    try:
        s3.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file_obj(file_obj, file_name):
    """Upload a file to an S3 bucket

    :param file_obj: File obj to upload
    :return: True if file was uploaded, else False
    """

    # Upload the file
    try:
        print("Uploading file", file_name, "to bucket", bucket_name)
        s3.upload_fileobj(file_obj, bucket_name, file_name)
        print("File uploaded")
    except ClientError as e:
        print("Error uploading file", e)
        logging.error(e)
        return False
    return True


def create_presigned_url(object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
