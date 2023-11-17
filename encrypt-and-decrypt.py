################## Author: Victor Iwuoha
################## Description: Tutorial

import os
import boto3
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv(override=True)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

# Create KMS client to nteract with the Customer manged key already created with AWS KMS
kms_client = boto3.client(
    "kms",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION,
)

with open(".secrets/key.txt") as file:
    # This key is your AWS Key ID in the format arn:aws:kms:us-east-2:123455:key/xxxxxx1233-444-5555
    key_id = file.read()

with open("data/raw-secret.txt") as file:
    secret_text = file.read()


def encrypt_data(key_id, plaintext, kms_client=kms_client):
    """Simple python Function to encrypt the plaintext.
    Args:
        key_id (str): The KMS key ID to use for encryption.
        plaintext (str): The plaintext to encrypt.
        kms_client (boto3.client): The KMS client to use for encryption.
    Returns:
        bytes: The ciphertext.
    Raises:
        Exception: If the encryption fails.

    """
    print("Encryption In Progress.")

    response = kms_client.encrypt(KeyId=key_id, Plaintext=plaintext)

    ciphertext = response["CiphertextBlob"]

    file_path = "data/encrypted-secret.txt"

    with open(f"{file_path}", "wb") as file:
        file.write(ciphertext)
        print(f"Encryption Successful.... Data written to {file_path}")

    return ciphertext


def decrypt_data(
    key_id, ciphertext_path="data/encrypted-secret.txt", kms_client=kms_client
):
    """Simple function to decrypt the ciphertext.
    Args:
        key_id (str): The KMS key ID to use for decryption.
        ciphertext (bytes): The ciphertext to decrypt.
        kms_client (boto3.client): The KMS client to use for decryption.
    Returns:
        bytes: The decrypted plaintext.
    Raises:
        Exception: If the decryption fails.

    """
    with open(ciphertext_path, "rb") as file:
        ciphertext = file.read()

    print("Decryption In Progress.")

    response = kms_client.decrypt(CiphertextBlob=ciphertext, KeyId=key_id)

    plaintext = response["Plaintext"]

    file_path = "data/decrypted-secret.txt"

    with open(f"{file_path}", "wb") as file:
        file.write(plaintext)
        print(f"Decryption Successful.... Data written to {file_path}")

    return plaintext


if __name__ == "__main__":
    ciphertext = encrypt_data(key_id, plaintext=secret_text)
    print(ciphertext)
    # TODO:Uncomment the next 2 lines to decrypt the ciphertext

    # plaintext = decrypt_data(key_id, ciphertext_path="data/encrypted-secret.txt")
    # print(plaintext)
