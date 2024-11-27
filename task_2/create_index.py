from elasticsearch import Elasticsearch
import json

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Define the index mapping
mapping = {
    "mappings": {
        "properties": {
            "department": {"type": "keyword"},
            "threat_score": {"type": "integer"}
        }
    }
}

# Create the index
index_name = "department_scores"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")
