from elasticsearch import Elasticsearch
import warnings
import time
from urllib3.exceptions import InsecureRequestWarning

# Setup
warnings.simplefilter('ignore', InsecureRequestWarning)

ELASTIC_IP = "192.168.106.150" #Our server IP 
ELASTIC_USER = "elastic"
ELASTIC_PASS = "YOUR_PASSWORD" 

client = Elasticsearch(
    f"https://{ELASTIC_IP}:9200",
    basic_auth=(ELASTIC_USER, ELASTIC_PASS),
    verify_certs=False
)

def check_for_attacks():
    print("Scanning for Brute Force attempts...")
    
    # Query: Look specifically for Windows Event ID 4625 (Failed Login)
    # We look at the last 15 minutes roughly (by sorting desc)
    query = {
        "match": {
            "event.code": 4625 
        }
    }

    response = client.search(
        index="logs-*",
        query=query,
        size=10,
        sort=[{"@timestamp": "desc"}]
    )

    hits = response['hits']['hits']
    count = len(hits)

    if count > 0:
        print(f"ALERT! Detected {count} failed login attempts!")
        
        # Print details of the attacker (or the victim user)
        first_hit = hits[0]['_source']
        user = first_hit.get('user', {}).get('name', 'Unknown User')
        ip = first_hit.get('source', {}).get('ip', 'Local Console')
        time = first_hit.get('@timestamp')
        
        print(f"   Target User: {user}")
        print(f"   Source IP:   {ip}")
        print(f"   Time:        {time}")
        print("   ACTION REQUIRED: Investigate immediately.\n")
    else:
        print("System Secure. No failed logins detected.\n")

# Run the check
if __name__ == "__main__":
    check_for_attacks()