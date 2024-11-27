import pandas as pd
from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Read data from CSV file
df = pd.read_csv('department_scores.csv')

# Index data into Elasticsearch
for i, row in df.iterrows():
    document = {
        "department": row['department'],
        "threat_score": row['threat_score']
    }
    es.index(index="department_scores", document=document)

print("Data indexed successfully.")

