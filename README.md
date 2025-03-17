# Hasura-MongoDB-Quickstart-Guide
This repo contains a step-by-step guide for setting up Hasura DDN with MongoDB, including schema introspection, metadata management, and GraphQL query execution.

### **Step 1: Install Hasura DDN CLI**
```
!curl -L https://graphql-engine-cdn.hasura.io/ddn/cli/v4/get.sh | bash
```
### **Step 2: Validate Installation**
```
!ddn doctor
```
### **Step 3: Install Docker (Ensure Docker is Installed and Running)**
# If Docker is not installed, follow instructions from: https://docs.docker.com/get-docker/

### **Step 4: Install `mongosh` (MongoDB Shell)**
# Visit https://www.mongodb.com/try/download/shell to download and install `mongosh`

### **Step 5: Authenticate Hasura DDN CLI**
```
!ddn auth login  # This will open a browser window for authentication
```
### **Step 6: Create a New Hasura DDN Project**
```
!ddn supergraph init my-project && cd my-project
```
### **Step 7: Initialize the MongoDB Connector**
```
!ddn connector init my_mongo -i  # Select MongoDB from the dropdown and confirm port
```
### **Step 8: Configure MongoDB Connection**
# Set connection string to MongoDB
```
MONGO_URI = "mongodb://local.hasura.dev:27017/my_database"
print(f"MongoDB connection set: {MONGO_URI}")
```
### **Step 9: Create Docker Compose File for MongoDB**
```
compose_content = """services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
"""
with open("app/connector/my_mongo/compose.mongo.yaml", "w") as f:
    f.write(compose_content)
print("Docker Compose file created.")
```
### **Step 10: Start MongoDB Container**
```
!docker compose -f app/connector/my_mongo/compose.mongo.yaml up -d
```
### **Step 11: Seed MongoDB with Initial Data**
```
!docker exec -it mongodb mongosh my_database --eval """
db.users.insertMany([
  { user_id: 1, name: 'Alice', age: 25 },
  { user_id: 2, name: 'Bob', age: 30 },
  { user_id: 3, name: 'Charlie', age: 35 }
]);
"""
```
### **Step 12: Introspect MongoDB Schema**
```
!ddn connector introspect my_mongo
```
### **Step 13: Track the Collection as a Model**
```
!ddn models add my_mongo users
```
### **Step 14: Create a Local Build**
```
!ddn supergraph build local
```
### **Step 15: Start Local Hasura DDN Services**
```
!ddn run docker-start
```
### **Step 16: Open Hasura Console and Run a Query**
```
!ddn console --local  # Open the GraphQL console
```
# Run this GraphQL query in the console manually:
```
query = """
query {
  users {
    userId
    name
    age
  }
}
"""
print("Paste this query in Hasura's GraphQL Explorer:")
print(query)
``
### **Step 17: Add a New Collection (Posts)**
```
!docker exec -it mongodb mongosh my_database --eval """
db.posts.insertMany([
  { user_id: 1, post_id: 1, title: 'My First Post', content: 'This is Alice\'s first post.' },
  { user_id: 1, post_id: 2, title: 'Another Post', content: 'Alice writes again!' },
  { user_id: 2, post_id: 3, title: 'Bob\'s Post', content: 'Bob shares his thoughts.' },
  { user_id: 3, post_id: 4, title: 'Hello World', content: 'Charlie joins the conversation.' }
]);
"""
```
### **Step 18: Refresh Metadata & Rebuild**
```
!ddn connector introspect my_mongo
!ddn model add my_mongo posts
!ddn supergraph build local
```
### **Step 19: Restart Services**
```
!ddn run docker-start
```
### **Step 20: Query the Posts Collection**
```
query_posts = """
query GetPosts {
  posts {
    userId
    postId
    title
    content
  }
}
"""
print("Paste this query in Hasura's GraphQL Explorer:")
print(query_posts)
```
### **Step 21: Create a Relationship Between Users and Posts**
```
relationship_yaml = """---
kind: Relationship
version: v1
definition:
  name: user
  sourceType: Posts
  target:
    model:
      name: Users
    relationshipType: Object
  mapping:
    - source:
        fieldPath:
          - fieldName: userId
      target:
        modelField:
          - fieldName: userId
"""
with open("app/metadata/Posts.hml", "a") as f:
    f.write(relationship_yaml)
print("Relationship added to metadata.")
```
### **Step 22: Final Rebuild and Restart**
```
!ddn supergraph build local
!ddn run docker-start
```
### **Step 23: Query Nested Data Using Relationship**
```
nested_query = """
query GetPosts {
  posts {
    postId
    title
    content
    user {
      userId
      name
      age
    }
  }
}
"""
print("Paste this query in Hasura's GraphQL Explorer:")
print(nested_query)
```
