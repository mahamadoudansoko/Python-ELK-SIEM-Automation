from elasticsearch import Elasticsearch
import warnings
from urllib3.exceptions import InsecureRequestWarning

# 1. Setup (Ignore SSL warnings for lab environment)
warnings.simplefilter('ignore', InsecureRequestWarning)

ELASTIC_IP = "192.168.106.150" #Our server IP
ELASTIC_USER = "elastic"
ELASTIC_PASS = "YOUR_PASSWORD" 

client = Elasticsearch(
    f"https://{ELASTIC_IP}:9200",
    basic_auth=(ELASTIC_USER, ELASTIC_PASS),
    verify_certs=False
)

print(f"Searching for Windows logs on {ELASTIC_IP}...")

# 2. The Search Query
# We look in "logs-*" index pattern.
# We ask for records where the OS is "windows".
# We sort by time (descending) to get the newest first.
try:
    response = client.search(
        index="logs-*",
        query={
            "match": {
                "host.os.type": "windows"
            }
        },
        size=5,
        sort=[{"@timestamp": "desc"}]
    )

    # 3. Process Results
    hits = response['hits']['hits']
    print(f"found {len(hits)} recent logs!\n")

    for hit in hits:
        source = hit['_source']
        timestamp = source.get('@timestamp', 'N/A')
        event_action = source.get('event', {}).get('action', 'Unknown Action')
        message = source.get('message', 'No message content')
        
        print(f"[{timestamp}] Action: {event_action}")
        print(f"   Message: {message[:100]}...") # Print first 100 chars only
        print("-" * 50)

except Exception as e:
    print(f"Error: {e}")