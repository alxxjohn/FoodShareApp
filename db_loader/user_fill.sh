#!/bin/bash

set -e

# Set API base URL
API_URL="http://localhost:8000/api/register"

# First user data
USER1=$(cat <<EOF
{
  "email": "user1@example.com",
  "username": "user1",
  "firstname": "User",
  "lastname": "One",
  "password": "testpassword"
}
EOF
)

# Second user data
USER2=$(cat <<EOF
{
  "email": "user2@example.com",
  "username": "user2",
  "firstname": "User",
  "lastname": "Two",
  "password": "testpassword"
}
EOF
)

echo "Creating first user..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$USER1")

if [ "$RESPONSE" -ge 500 ]; then
  echo "Server error ($RESPONSE) during first user creation. Aborting."
  exit 1
elif [ "$RESPONSE" -ge 400 ]; then
  echo "Client error ($RESPONSE) creating first user, but not server fault. Continuing..."
else
  echo "First user created successfully."
fi

echo "Creating second user..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$USER2")

if [ "$RESPONSE" -ge 500 ]; then
  echo "Server error ($RESPONSE) during second user creation. Aborting."
  exit 1
elif [ "$RESPONSE" -ge 400 ]; then
  echo "Client error ($RESPONSE) creating second user."
else
  echo "Second user created successfully."
fi
