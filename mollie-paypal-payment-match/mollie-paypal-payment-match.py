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

def get_last_month_year_and_month() -> str:
    today = datetime.date.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
    return last_day_of_previous_month.strftime('%Y%m')

def find_mollie_transaction_id(belegnr: str) -> str:


    # Initialize the Mollie API client
    mollie_client = Client()
    mollie_client.set_api_key(mollie_api_key)  # Replace with your actual API key


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
            print("Next Page...")
            payments = payments.get_next()
            
    # If the payment is found, print its details
    if found_payment:
        print(f"Order ID: {found_payment.metadata['plentyOrderId']}")
        print(f"Transaction ID: {transaction_id}")
        #pprint(found_payment)
        return found_payment.metadata['plentyOrderId']
    else:
        print("Payment not found. Last:")
        pprint(payments[-1])
        return belegnr
    

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
                row[1] = new_belegnr
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


if __name__ == '__main__':
    main()
