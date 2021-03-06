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


def get_temp_thumbnail_link(s3_client, thumbnail_size, img_name, time_exp):
    """Creates and returns a temporary link to a thumbnail."""
    temp_url = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME,
            "Key": f"images/{thumbnail_size}_{img_name}",
        },
        ExpiresIn=time_exp,
    )
    return temp_url


def create_new_thumbnail(thumbnail_size, img_name):
    """Creates a new thumbnail in the S3 thumbnail bucket."""
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    destination_bucket = settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME

    extension = img_name.split(".")[-1]
    event_data = {
        "bucket_name": bucket_name,
        "destination_bucket_name": destination_bucket,
        "image_name": img_name,
        "new_height": thumbnail_size,
        "content_type": "image/png" if extension == "png" else "image/jpeg",
    }
    lambda_client = boto3.client("lambda", region_name="eu-central-1")
    lambda_client.invoke(
        FunctionName="CreateAndSaveThumbnailOnDemand",
        InvocationType="Event",
        Payload=json.dumps(event_data),
    )


def _get_all_s3_objects(s3_client):
    return s3_client.list_objects_v2(Bucket=settings.AWS_THUMBNAILS_STORAGE_BUCKET_NAME)


def check_if_file_exists_in_s3(img_name, thumbnail_size, s3_client):
    """
    Checks whether file of name `thumbnail_size_img_name` exists in a S3 bucket.
    """
    s3_objects = _get_all_s3_objects(s3_client)
    img_path = f"images/{thumbnail_size}_{img_name}"
    return "Contents" in s3_objects and any(
        dictionary["Key"] == img_path for dictionary in s3_objects["Contents"]
    )
