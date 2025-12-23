from elasticsearch import Elasticsearch
import sys

# CONFIGURATION
ELASTIC_IP = "192.168.106.150"
ELASTIC_USER = "elastic"
ELASTIC_PASS = "Sajo22032002" # <--- Double check this!

print(f"Attempting to connect to https://{ELASTIC_IP}:9200...")

# Configure client with detailed SSL context
client = Elasticsearch(
    f"https://{ELASTIC_IP}:9200",
    basic_auth=(ELASTIC_USER, ELASTIC_PASS),
    verify_certs=False,
    ssl_show_warn=False
)

try:
    # We use .info() instead of .ping() because .info() throws specific errors
    info = client.info()
    print("\n✅ SUCCESS! Connection established.")
    print(info)
except Exception as e:
    print("\n❌ CONNECTION FAILED.")
    print("Here is the exact error:")
    print(e)