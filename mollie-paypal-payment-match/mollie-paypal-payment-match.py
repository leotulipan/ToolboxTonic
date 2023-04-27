import os
import datetime
from datetime import date
from dateutil.parser import parse
from dotenv import load_dotenv
from mollie.api.client import Client
from pprint import pprint
import glob
import csv
from typing import List
from plentyrest.rest import Plenty
import json
import base64
import io

# Load the .env file and read the secrets
load_dotenv()
mollie_api_key = os.getenv("MOLLIE_API_KEY")
restuser = os.environ.get('REST_USER')
restpwd = os.environ.get('REST_PASSWORD')

# Define the API endpoint
url = 'shop.tulipans.com'

docs = []

# Initialize the Plenty API client
plenty = Plenty(url, restuser, restpwd)
# Initialize the Mollie API client
mollie_client = Client()
mollie_client.set_api_key(mollie_api_key) 

def get_last_month_year_and_month() -> str:
    today = datetime.date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
    return last_day_of_previous_month.strftime('%Y%m')

def find_mollie_transaction_id(belegnr: str) -> str:

    # Define the transaction ID you want to search for
    transaction_id = belegnr
    #order_id = '34218'
    #transaction_id = '6447e402a0da5'

    # Define the date range
    from_date = date(2022, 11, 6)

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
            # print("Next Page...")
            payments = payments.get_next()
            
    # If the payment is found, print its details
    if found_payment:
        # print(f"Order ID: {found_payment.metadata['plentyOrderId']}")
        # print(f"Transaction ID: {transaction_id}")
        #pprint(found_payment)
        return found_payment.metadata['plentyOrderId']
    else:
        print("Payment not found.")
        # pprint(payments[-1])
        return belegnr

# Add a new function to append the document information to the global docs list
def append_invoice_to_docs(invoice_number: str, document_filename: str, document_id: int):
  
    docs.append({
        'documentId': document_id,
        'documentFilename': document_filename,
        'invoiceNumber': invoice_number
    })

def get_invoice_details(order_id: int) -> tuple:
    # Fetch the order details from Plenty
    params = {
        'orderIds': order_id,
        'with[]': 'documents'
    }
    order_details = plenty.request('rest/orders', 'GET', params)

    if order_details is None or 'entries' not in order_details:
        raise ValueError(f'No order found with ID {order_id}')

    order = order_details['entries'][0]
    
    # Extract the invoice number and document filename from the order details
    # invoice_number = order['invoiceNumber']
    document_filename = None
    invoice_number = None

    # if 'documents' in order:
    #     for document in order['documents']:
    #         if document['type'] == 'invoice':
    #             document_filename = os.path.basename(document['path'])
    #             invoice_number = document['numberWithPrefix']
    #             break

    if 'documents' in order:
        # Loop over each document in the 'documents' array for the current entry
        for doc in order['documents']:
            if doc['type'] == 'invoice':
                document_filename = os.path.basename(doc['path'])
                invoice_number = doc['numberWithPrefix']
                # print(f'Invoice Number: {invoice_number} - {document_filename} - {order_id}')
                # docs.append({
                #     'documentId': doc['id'],
                #     'documentFilename': document_filename,
                #     'invoiceNumber': invoice_number
                # })

    return invoice_number, document_filename, doc['id']


def download_invoices():
    for document in docs:
        response = plenty.request(f'rest/documents/{document["documentId"]}', 'GET')
        file_name = document['documentFilename']

        if len(response) > 500:
            if os.path.isfile(file_name):
                print(f"Skipping download of '{file_name}'")
            else:
                # Save PDF to file
                with open(file_name, 'wb') as f:
                    f.write(response)
                print(f"Downloaded '{file_name}'")
        else:
            print(f"Error with documentId {document['documentId']} for orderId {document['orderId']}")

        print("\n")

def process_csv(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='cp1252') as infile, open(output_file, 'w', encoding='cp1252', newline='') as outfile:
        reader = csv.reader(infile, delimiter=';')
        writer = csv.writer(outfile, delimiter=';')

        header = next(reader)
        writer.writerow(header)

        for row in reader:
            belegnr = row[1]

            if len(belegnr) != 13 or int(belegnr[:2]) < 63:
                writer.writerow(row)
            else:
                new_belegnr = find_mollie_transaction_id(belegnr)
                # if(new_belegnr != belegnr):
                #     invoice_number, document_filename = get_invoice_details(new_belegnr)
                #     print(f'Invoice Number: {invoice_number} - {new_belegnr}')
                if(new_belegnr != belegnr):
                    invoice_number, document_filename, document_id = get_invoice_details(new_belegnr)
                    print(f'Invoice Number: {invoice_number} - {new_belegnr}')
                    append_invoice_to_docs(invoice_number, document_filename, document_id)
                row[1] = invoice_number
                row[4] = row[4] + " " + new_belegnr

                writer.writerow(row)

def main():
    yyyy_mm = get_last_month_year_and_month()
    input_file_pattern = f'BMD_Buchungsstapel_PayPal_{yyyy_mm}_*.csv'

    matching_files = glob.glob(input_file_pattern)
    if len(matching_files) != 1:
        raise ValueError('Expected one input file, but found more or less than one.')

    input_file = matching_files[0]
    output_file = f'output_{yyyy_mm}.csv'

    process_csv(input_file, output_file)

    print("Downloading files now")
    download_invoices()


if __name__ == '__main__':
    main()
