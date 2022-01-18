# Mindee API helper library for Python

The full documentation is available [here](https://developers.mindee.com/docs/getting-started)

## Requirements

This library is officially supported on Python 3.7 to 3.10.

## Install

Install from PyPi using pip, a package manager for Python.

```shell script
pip install mindee
```

Don't have pip installed? Try installing it, by running this from the command line:

```shell script
$ curl https://bootstrap.pypa.io/get-pip.py | python
```

Getting started with the Mindee API couldn't be easier.
Create a Client and you're ready to go.

## Create your Client

The mindee.Client needs your [API credentials](https://developers.mindee.com/docs/make-your-first-request#create-an-api-key).
You can either pass these directly to the constructor (see the code below) or via environment variables.

Depending on what type of document you want to parse, you need to add specifics auth token for each endpoint.

```python
from mindee import Client

mindee_client = Client(
    expense_receipt_token="your_expense_receipt_api_token_here",
    invoice_token="your_invoice_api_token_here",
    passport_token="your_passport_api_token_here",
    license_plate_token="your_license_plate_api_token_here",
    raise_on_error=True
)
```

We suggest storing your credentials as environment variables.
Why? You'll never have to worry about committing your credentials and accidentally posting them somewhere public.


## Parsing methods

```python
# Call the receipt parsing API and create a receipt object under parsed_data.receipt
parsed_data = mindee_client.parse_receipt("/path/to/file")

# Call the invoice parsing API and create an invoice object under parsed_data.invoice
parsed_data = mindee_client.parse_invoice("/path/to/file")

# If you have a mixed data flow of invoice and receipt, use financial_document class
# Call the invoice or receipt parsing API according to your input data type
# and create a FinancialDocument object under parsed_data.financial_document
parsed_data = mindee_client.parse_financial_document("/path/to/file")

# Call the passport parsing API and create a Passport object under parsed_data.passport
parsed_data = mindee_client.parse_passport("/path/to/file")

# Call the license_plates parsing API and create a CarPlate object under parsed_data.license_plate
parsed_data = mindee_client.parse_license_plate("/path/to/file")
```

## Input data

You can pass your input file in three ways:

From file path
```python
receipt_data = mindee_client.parse_receipt('/path/to/file', input_type="path")
```

From a file object
```python
with open('/path/to/file', 'rb') as fp:
     receipt_data = mindee_client.parse_receipt(fp, input_type="file")
```

From a base64
```python
receipt_data = mindee_client.parse_receipt(base64_string, input_type="base64", filename="receipt.jpg")
```
