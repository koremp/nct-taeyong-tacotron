from google.cloud import storage
import os
os.environ.setdefault("GCLOUD_PROJECT", "snappy-provider-389211")
storage_client = storage.Client()
buckets = list(storage_client.list_buckets())

print(buckets)
