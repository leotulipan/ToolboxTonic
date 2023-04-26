import os
from datetime import date
from dateutil.parser import parse
from dotenv import load_dotenv
from mollie.api.client import Client
from pprint import pprint



# Load the .env file and read the MOLLIE_API_KEY
load_dotenv()
mollie_api_key = os.getenv("MOLLIE_API_KEY")

# Initialize the Mollie API client
mollie_client = Client()
mollie_client.set_api_key(mollie_api_key)  # Replace with your actual API key

# Define the transaction ID you want to search for
transaction_id = '6418106a91420'
#order_id = '34218'
#transaction_id = '6447e402a0da5'

# Define the date range
from_date = date(2023, 3, 1)


# Iterate through all payments and look for the transaction ID

# Initialize variables
found_payment = None
first_payment = True
stop_search = False

# Fetch payments within the specified date range
payments = mollie_client.payments.list(limit=250)

while payments and not stop_search:
    for payment in payments:
        # Get the payment date
        payment_date = parse(payment.created_at).date()

        if first_payment:
            # print(f"Metadata for the first payment:")
            # pprint(payment.metadata)
            first_payment = False

        # Check if the order ID matches the desired order ID
        if payment.metadata and 'plentyTransactionCode' in payment.metadata and payment.metadata['plentyTransactionCode'] == transaction_id:
        #if payment.metadata and 'plentyOrderId' in payment.metadata and payment.metadata['plentyOrderId'] == order_id:
            found_payment = payment
            stop_search = True
            break

        # Check if the payment date is less than the from_date
        if payment_date < from_date:
            print(f"Date {from_date} reached. Stopping.")
            stop_search = True
            break

    # If the search hasn't stopped, fetch the next page of payments
    if not stop_search:
        print("Next Page...")
        payments = payments.get_next()
        
# If the payment is found, print its details
if found_payment:
    print(f"Order ID: {found_payment.metadata['plentyOrderId']}")
    print(f"Transaction ID: {transaction_id}")
    #pprint(found_payment)
    # Add more details as needed
else:
    print("Payment not found. Last:")
    pprint(payments[-1])


# If you need more details, you can access them through the payment object, e.g.:
# payment.customer_id, payment.metadata, etc.
