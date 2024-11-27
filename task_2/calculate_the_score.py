from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch("http://localhost:9200")

# Query Elasticsearch for department data
def get_department_scores():
    query = {
        "query": {
            "match_all": {}
        }
    }
    response = es.search(index="department_scores", body=query, size=1000)

    # Extract department scores from the response
    department_scores = {}
    for hit in response['hits']['hits']:
        department = hit['_source']['department']
        threat_score = hit['_source']['threat_score']
        if department not in department_scores:
            department_scores[department] = []
        department_scores[department].append(threat_score)
    
    return department_scores

# Example of calculating aggregated score (without importance for simplicity)
def calculate_aggregated_score(department_scores):
    total_weighted_score = 0
    total_users = 0

    for department, scores in department_scores.items():
        total_weighted_score += sum(scores)
        total_users += len(scores)

    aggregated_score = total_weighted_score / total_users
    return round(min(max(aggregated_score, 0), 90))  # Ensure score is within 0-90 range

# Get department scores from Elasticsearch
department_scores = get_department_scores()

# Calculate aggregated score
aggregated_score = calculate_aggregated_score(department_scores)
print(f"Aggregated Threat Score: {aggregated_score}")
