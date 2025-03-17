#!/bin/bash

# Install Hasura DDN CLI
echo "Installing Hasura DDN CLI..."
curl -L https://graphql-engine-cdn.hasura.io/ddn/cli/v4/get.sh | bash

# Authenticate
echo "Authenticating Hasura DDN..."
ddn auth login

# Initialize Project
echo "Initializing Hasura DDN project..."
ddn supergraph init my-project && cd my-project

# Setup MongoDB Connector
echo "Setting up MongoDB connector..."
ddn connector init my_mongo -i <<EOF
mongo
EOF

# Start MongoDB Service
echo "Starting MongoDB service..."
docker compose -f app/connector/my_mongo/compose.mongo.yaml up -d

# Introspect Database Schema
echo "Introspecting MongoDB..."
ddn connector introspect my_mongo

# Add Users Model
echo "Adding Users model..."
ddn models add my_mongo users

# Build & Start Services
echo "Building and starting Hasura DDN services..."
ddn supergraph build local
ddn run docker-start

echo "Setup Complete! 🎉"
