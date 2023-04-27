# Register your application in the Mollie Dashboard: https://www.mollie.com/dashboard/developers/applications
# Get the OAuth client_id and client_secret for your application.
# Implement the OAuth2 authorization flow to obtain an access token.
# Here's a basic example of how to get an access token using the requests library and the authorization_code grant type:
import os
import requests
from requests.auth import HTTPBasicAuth
import secrets
from dotenv import load_dotenv

# Generate a unique state value and store it securely
state = secrets.token_hex(16)

# Load the .env file and read the MOLLIE_API_KEY
load_dotenv()
client_id = os.getenv("MOLLIE_CLIENT_ID")
client_secret = os.getenv("MOLLIE_CLIENT_SECRET")
redirect_uri = 'https://tulipans.com/wp'

# The authorization URL to redirect the user to
auth_url = f'https://www.mollie.com/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=organizations.read&state={state}'

print(f'Redirect the user to this URL and obtain the authorization code: {auth_url}')

# After the user authorizes your application, they will be redirected to the redirect_uri with a "code" query parameter
# Replace this with the actual authorization code obtained
authorization_code = 'auth_kEbHmerhc2De6T2EGyVWGh387Tss3D'

# Exchange the authorization code for an access token
token_url = 'https://api.mollie.com/oauth2/tokens'
data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri
}

response = requests.post(token_url, data=data, auth=HTTPBasicAuth(client_id, client_secret))
access_token = response.json()['access_token']

print(access_token)
