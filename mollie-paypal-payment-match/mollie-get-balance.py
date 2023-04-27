import os
from mollie.api.client import Client
from dotenv import load_dotenv

load_dotenv()
access_token = os.getenv("MOLLIE_ACCESS_TOKEN")

mollie_client = Client()
mollie_client.set_access_token(access_token)

balance_response = mollie_client.organizations.get('me')
balance = balance_response['balance']

print(f"Current balance: {balance}")