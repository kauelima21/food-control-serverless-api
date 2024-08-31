import logging

import boto3

logging.getLogger().setLevel(logging.INFO)


def create_bucket(bucket_name: str, region="sa-east-1"):
    s3 = boto3.client('s3')
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={'LocationConstraint': region}
    )

    logging.info("Bucket [{}] was created".format(bucket_name))

    return bucket_name


def generate_post_url(bucket_name: str, object_name: str, type: str,
                      expiration=3600):
    s3_client = boto3.client("s3")
    return s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": bucket_name,
            "Key": object_name,
            "ContentType": type,
        },
        ExpiresIn=expiration
    )
