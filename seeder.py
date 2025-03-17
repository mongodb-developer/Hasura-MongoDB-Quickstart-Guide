from pymongo import MongoClient

# MongoDB Connection
client = MongoClient("mongodb://local.hasura.dev:27017/my_database")
db = client["my_database"]

# Sample Users
users = [
    {"user_id": 1, "name": "Alice", "age": 25},
    {"user_id": 2, "name": "Bob", "age": 30},
    {"user_id": 3, "name": "Charlie", "age": 35}
]

# Sample Posts
posts = [
    {"user_id": 1, "post_id": 1, "title": "My First Post", "content": "This is Alice's first post."},
    {"user_id": 1, "post_id": 2, "title": "Another Post", "content": "Alice writes again!"},
    {"user_id": 2, "post_id": 3, "title": "Bob's Post", "content": "Bob shares his thoughts."},
    {"user_id": 3, "post_id": 4, "title": "Hello World", "content": "Charlie joins the conversation."}
]

# Insert into MongoDB
db.users.insert_many(users)
db.posts.insert_many(posts)

print("Database seeded successfully!")
