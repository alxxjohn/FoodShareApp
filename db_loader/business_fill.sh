
#!/bin/bash

set -e

# Set API base URL
API_URL="http://localhost:8000/api/register/business"

BUSINESS1=$(cat <<EOF
{
  "firstname": "jess",
  "lastname": "iojio",
  "password": "alex123",
  "company_name": "ALexTest",
  "email": "sdsd@sdsdsd.com",
  "username": "alextest1Business",
  "tos_accepted": true,
  "address": "530 N. Blue Lake Ave.",
  "city": "Deland",
  "state": "FL",
  "zipCode": "32724",
  "phone": "3109278337",
  "is_business": true,
  "is_foodbank": false,
  "is_admin": false
}

EOF
)

BUSINESS2=$(cat <<EOF
{
  "firstname": "jess",
  "lastname": "iojio",
  "password": "alex123",
  "company_name": "alextest2business",
  "email": "sdsd@sdsdsd.com",
  "username": "alextest2",
  "tos_accepted": true,
  "address": "1645 N. Merch Ave.",
  "city": "Orlando",
  "state": "FL",
  "zipCode": "32724",
  "phone": "3109278337",
  "is_business": true,
  "is_foodbank": false,
  "is_admin": false
}
EOF
)

echo "Creating first business..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$BUSINESS1")

if [ "$RESPONSE" -ge 500 ]; then
  echo "Server error ($RESPONSE) during first business creation. Aborting."
  exit 1
elif [ "$RESPONSE" -ge 400 ]; then
  echo "Client error ($RESPONSE) creating first business, but not server fault. Continuing..."
else
  echo "First business created successfully."
fi

echo "Creating second business..."
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$BUSINESS2")

if [ "$RESPONSE" -ge 500 ]; then
  echo "Server error ($RESPONSE) during second business creation. Aborting."
  exit 1
elif [ "$RESPONSE" -ge 400 ]; then
  echo "Client error ($RESPONSE) creating second business."
else
  echo "Second business created successfully."
fi
