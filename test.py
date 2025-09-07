print("Hello World!")


from google.cloud import bigquery

# Initialize client
client = bigquery.Client(project="cicd-demo-468415")

# Query the table
query = "SELECT * FROM `cicd-demo-468415.my_dataset.my_table`"
results = client.query(query)

# Print results
for row in results:
    print(f"id: {row.id}, name: {row.name}, created_at: {row.created_at}")