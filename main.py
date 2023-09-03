import os

from flask import Flask, jsonify
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hi, this is a simple Azure API using Flask!"


@app.route('/list-blobs')
def list_blobs():
    credential = DefaultAzureCredential()

    blob_storage_url = os.environ.get("BLOB_STORAGE_URL")
    container_name = os.environ.get("CONTAINER_NAME")
    if not blob_storage_url or not container_name:
        error_message = "Missing required environment variables: " \
                        "BLOB_STORAGE_URL, CONTAINER_NAME"
        return jsonify({"error": error_message}), 400

    try:
        blob_service_client = BlobServiceClient(account_url=blob_storage_url,
                                                credential=credential)

        container_client = blob_service_client.get_container_client(container_name)

        blob_list = [blob.name for blob in container_client.list_blobs()]

        return jsonify(blob_list)
    except Exception as e:
        return  str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
