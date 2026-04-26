from google.cloud import storage
from src.entity.config_entity import *

storage_client = storage.Client()

# def get_bucket_list():
#     for buckets in storage_client.list_buckets():
#         b = buckets
def download_blob(bucket_name, source_blob_name, destination_file_name):

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name) #basically the file name use in gcp
    blob.download_to_filename(destination_file_name)
    print(
        f"{source_blob_name} under {bucket_name} is downloaded at {destination_file_name}"
    )

def upload_blob(bucket_name, gcp_bucket_blob_processed, transformes_data_file_path):

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(gcp_bucket_blob_processed) #basically the file name use in gcp
    blob.upload_from_filename(transformes_data_file_path)

    print(
        f"File {transformes_data_file_path} uploaded to {gcp_bucket_blob_processed}."
    )