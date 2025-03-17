import pymongo
import requests
import time
import os

# MongoDB connection details
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('DB_NAME', 'your_db')

# Hasura connection details
HASURA_ENDPOINT = os.getenv('HASURA_ENDPOINT', 'http://localhost:8080/v1/graphql')
HASURA_ADMIN_SECRET = os.getenv('HASURA_ADMIN_SECRET', 'your-secret')

# Connect to MongoDB
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client.get_default_database()

# Function to monitor MongoDB performance

def monitor_mongo_performance():
    server_status = db.command('serverStatus')
    metrics = {
        'connections': server_status['connections'],
        'opcounters': server_status['opcounters'],
        'mem': server_status.get('mem'),
        'opcounters': server_status.get('opcounters'),
        'connections': server_status['connections'],
        'uptime': server_status['uptime']
    }
    print("MongoDB Performance Metrics:", metrics)

# Function to monitor Hasura performance

def monitor_hasura_performance():
    headers = {'x-hasura-admin-secret': HASURA_ADMIN_SECRET}
    query = '{ __schema { queryType { name }}}'

    start_time = time.time()
    response = requests.post('http://localhost:8080/v1/graphql', json={'query': '{ __typename }'}, headers=headers)
    duration = time.time() - start_time

    if response.status_code == 200:
        print(f"Hasura response time: {duration:.4f}s")
    else:
        print("Hasura request failed:", response.text)


# Main monitoring loop
if __name__ == '__main__':
    while True:
        print("\nChecking performance metrics...")

        # MongoDB Monitoring
        monitor_mongo_performance()

        # Hasura performance Monitoring
        start_time = time.time()
        monitor_hasura_performance()

        # Run every 60 seconds
        time.sleep(60)
