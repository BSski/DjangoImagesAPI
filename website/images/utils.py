import json

import boto3

from website import settings


def get_s3_client():
    """Creates and returns a boto3 client."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    return s3_client


def get_temp_thumbnail_link(s3_client, new_height, img_name, time_exp):
    """Creates and returns a temporary link to a thumbnail."""
    temp_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME,
            "Key": f"images/{new_height}_{img_name}",
        },
        ExpiresIn=time_exp,
    )
    return temp_url


def get_s3_objects(s3_client):
    return s3_client.list_objects_v2(
        Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME
    )


def create_new_thumbnail(new_height, img_name):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    destination_bucket = settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME

    extension = img_name.split(".")[-1]
    event_data = {
        "bucket_name": bucket_name,
        "destination_bucket_name": destination_bucket,
        "image_name": img_name,
        "new_height": new_height,
        "content_type": "image/png" if extension == "png" else "image/jpeg",
    }
    lambda_client = boto3.client("lambda", region_name="eu-central-1")
    lambda_client.invoke(
        FunctionName="CreateAndSaveThumbnailOnDemand",
        InvocationType="Event",
        Payload=json.dumps(event_data),
    )