import boto3
import os
from datetime import datetime, timedelta


def lambda_handler(event, context):
    kms_key_id = os.environ.get(
        "KMS_KEY_ID"
    )  # The KMS key ID to be scheduled for deletion exported by terraform
    response_data = {}

    try:
        # Calculate the deletion date (7 days from now)
        deletion_date = datetime.now() + timedelta(days=7)

        # Schedule the KMS key for deletion
        client = boto3.client("kms")
        client.schedule_key_deletion(KeyId=kms_key_id, PendingWindowInDays=7)

        # Signal success
        response_data["StatusCode"] = 200
        response_data[
            "Message"
        ] = f"KMS key `{kms_key_id}` scheduled for deletion on `{deletion_date}`"
        print("SUCCESS:", response_data["Message"])
        return response_data

    except Exception as e:
        print(f"Error: {e}")
        # Signal failure
        response_data["StatusCode"] = 500
        response_data[
            "Message"
        ] = f"Error scheduling deletion of KMS key {kms_key_id}: {str(e)}"
        return response_data
