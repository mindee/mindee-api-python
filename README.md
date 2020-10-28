# mindee-python


The documentation for the Mindee API can be found [here].

The Python library documentation can be found [here].

# Contents

1. [Installation](#installation)
2. [Getting started](#getting-started)
    * [API Credentials](#api-credentials)
    * [Client response structure](#client-response-structure)
3. [Parse a receipt](#components)
    * [Receipt objects data](#receipt-objects-data)
    * [Receipt objects methods](#receipt-objects-methods)
4. [Parse an invoice](#components)
    * [Invoice objects data](#receipt-objects-data)
    * [Invoice objects methods](#receipt-objects-methods)
5. [Parse invoice and receipt in a single endpoint](#components)
    * [Financial Document objects data](#receipt-objects-data)
    * [Financial Document objects methods](#receipt-objects-methods)
6. [Parse a passport](#components)
    * [Passport objects data](#receipt-objects-data)
    * [Passport objects methods](#receipt-objects-methods)

## Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a
package manager for Python.

    pip install mindee

If pip install fails on Windows, check the path length of the directory. If it is greater 260 characters then enable [Long Paths](https://docs.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation) or choose other shorter location.

Don't have pip installed? Try installing it, by running this from the command
line:

    $ curl https://bootstrap.pypa.io/get-pip.py | python

You may need to run the above commands with `sudo`.

## Getting Started

Getting started with the Mindee API couldn't be easier. Create a
`Client` and you're ready to go.

### API Credentials

The `Mindee` needs your API credentials. You can either pass these
directly to the constructor (see the code below) or via environment variables.

Depending on what type of document you want to parse, you need to add
specifics auth token for each endpoint.
```python
from mindee import Client

mindee_client = Client(
    expense_receipt_token="your_expense_receipts_api_token_here",
    invoice_token="your_invoices_api_token_here",
    passport_token="your_passport_api_token_here"
)
```

We suggest storing your credentials as environment variables. Why? You'll never
have to worry about committing your credentials and accidentally posting them
somewhere public.

### Client response structure

The client object contains different parsing method specific for each type of
 document supported by Mindee API.
 
Examples: 

```python
from mindee import Client

mindee_client = Client(
    expense_receipt_token="your_expense_receipts_api_token_here",
    invoice_token="your_invoices_api_token_here",
    passport_token="your_passport_api_token_here"
)

# This is a dummy example, see other methods below for real examples
parsed_data = mindee_client.parse_document_xxx("/path/to/file")
```

Each object returned by parsing methods follows the same structure:

#### parsed_data.document
This attribute is the Document object constructed by gathering all the pages into a 
single document. If you many objects for multi pages pdfs, see data.pages.
```python
parsed_data.document # returns a unique object from class DocumentXXX
```


#### parsed_data.pages
For multi pages pdf, the 'pages' attribute is a list of documents objects, each object 
is constructed using a unique page of the pdf;
```python
parsed_data.pages # [DocumentXXX, DocumentXXX ...] 
```


#### parsed_data.http_response
Contains the full Mindee API response object
 ```python
parsed_data.http_response # full HTTP request object 
```

## Parse a receipt

```python
from mindee import Client

mindee_client = Client(
    expense_receipt_token="your_expense_receipts_api_token_here"
)

receipt_data = mindee_client.parse_receipt('./path/to/receipt.jpg')
print(receipt_data.document)
```

#### Receipt objects data
Here are the different fields extracted and examples on how to get them from a Receipt object
* locale
```python
receipt_data.document.locale.value # en-US (string)
receipt_data.document.locale.language # en (string)
receipt_data.document.locale.country # US (string)
receipt_data.document.locale.probability # 0.89 (float)
```
* total_incl
```python
receipt_data.document.total_incl.value # 144.97 (float)
receipt_data.document.total_incl.probability # 0.89 (float)
```
* date
```python
receipt_data.document.date.value # 2020-12-04 (float)
receipt_data.document.date.date_object # Object (datetime.date object)
receipt_data.document.date.probability # 0.99 (float)
```
* merchant_name
```python
receipt_data.document.merchant_name.value # Amazon (string)
receipt_data.document.merchant_name.probability # 0.97 (float)
```
* time
```python
receipt_data.document.time.value # 15:02 (string)
receipt_data.document.time.probability # 0.44 (float)
```
* orientation
```python
receipt_data.document.orientation.value # 90 (int)
receipt_data.document.orientation.probability # 0.97 (float)
```
* total_tax
```python
receipt_data.document.total_tax.value # 12.48 (float)
receipt_data.document.total_tax.probability # 0.97 (float)
```
* taxes
```python
receipt_data.document.taxes # List of Tax objects

receipt_data.document.taxes[0].value # 2.41 (float)
receipt_data.document.taxes[0].probability # 0.45 (float)
receipt_data.document.taxes[0].rate # 0.2 (float)
```

#### Receipt objects methods

## Parse a passport

```python
from mindee import Client

mindee_client = Client(
    passport_token="your_passport_api_token_here"
)

passport_data = mindee_client.parse_passport('./path/to/passport.jpeg')
print(passport_data.document)

```


## Parse an invoice

```python
from mindee import Client

mindee_client = Client(
    invoice_token="your_invoices_api_token_here"
)

invoice_data = mindee_client.parse_invoice("./path/to/invoice.pdf")
print(invoice_data.document)
```


## Receipts and invoices with a single endpoint

```python
from mindee import Client

mindee_client = Client(
    expense_receipt_token="your_expense_receipts_api_token_here",
    invoice_token="your_invoices_api_token_here"
)

financial_document = mindee_client.parse_financial_document("./path/to/invoice.pdf/or/receipt.jpg")
print(financial_document.document)
```

