# Mindee API helper library for Python

The full documentation is available [here](https://developers.mindee.com/docs/getting-started)

## Installation

### Requirements

This library is officially supported on Python 3.7 to 3.10.

### Normal Installation

The preferred installation method is via `pip`:
```shell script
pip install mindee
```

### Development Installation

If you'll be modifying the source code, you'll need to install the development
requirements as well.

First clone this repo:
```shell script
git clone git@github.com:mindee/mindee-api-python.git
```

Then navigate to the clone directory and install all development requirements:
```shell script
cd mindee-api-python
pip install .[dev,test]
```

## Basic Usage

Getting started with the Mindee's Off-the-Shelf documents couldn't be easier.
Create a Client and you're ready to go.

### Create your Client

The `mindee.Client` needs your [API credentials](https://developers.mindee.com/docs/make-your-first-request#create-an-api-key).
You can either pass these directly to the constructor or via environment variables.

You only need to specify the API keys for the document endpoints you'll be using.

```python
from mindee import Client

mindee_client = Client(
    receipt_api_key="your_expense_receipt_api_key_here",
    invoice_api_key="your_invoice_api_key_here",
    passport_api_key="your_passport_api_key_here",
    raise_on_error=True
)
```

#### Environment variables
You can also set the API keys as environment variables.
This is highly recommended for any production deployment.

* `MINDEE_RECEIPT_API_KEY`
* `MINDEE_INVOICE_API_KEY`
* `MINDEE_PASSPORT_API_KEY`

### Parsing Documents

#### Document types
The document type must be specified when calling the `Client.parse` method.

The object containing the parsed data will be an attribute of the response object.
The name of this attribute will be the same as the `document_type`
specified when calling the `Client.parse` method.

Receipts
```python
api_response = mindee_client.parse_from_path("/path/to/receipt.jpg", "receipt")
print(api_response.receipt)
```
Invoices
```python
api_response = mindee_client.parse_from_path("/path/to/invoice.pdf", "invoice")
print(api_response.invoice)
```
Passports
```python
api_response = mindee_client.parse_from_path("/path/to/passport.jpg", "passport")
print(api_response.passport)
```

Mixed data flow of invoices and receipts.\
**Note:** You'll need an API key for _both_ invoice and receipts endpoints.
```python
api_response = mindee_client.parse_from_path("/path/to/receipt.jpg", "financial_document")
print(api_response.financial_document)
api_response = mindee_client.parse_from_path("/path/to/invoice.pdf", "financial_document")
print(api_response.financial_document)
```

### Document Sources

You can pass your document in various ways.

#### Path
An absolute path, as a string.
```python
invoice_data = mindee_client.parse_from_path('/path/to/invoice.pdf', "invoice")
```

#### File Object
A normal Python file object/handle.
```python
with open('/path/to/receipt.jpg', 'rb') as fo:
     receipt_data = mindee_client.parse_from_file(fo, "receipt")
```

#### Base64
A base64 encoded string.\
Note that the original filename of the encoded file is required when calling the method.
```python
b64_string = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLD...."
receipt_data = mindee_client.parse_from_b64string(b64_string, "receipt.jpg", "receipt")
```

#### Bytes
Raw bytes.\
Note that the original filename is required when calling the method.
```python
raw_bytes = b"%PDF-1.3\n%\xbf\xf7\xa2\xfe\n1 0 ob..."
invoice_data = mindee_client.parse_from_bytes(raw_bytes, "invoice.pdf", "invoice")
```

This is useful, for example, when using FastAPI `UploadFile` objects:
```python
@app.post("/invoice")
async def upload(upload: UploadFile):
    invoice_data = mindee_client.parse_from_bytes(
        upload.file.read(), "invoice", filename=upload.filename
    )
```

## Usage with the API Builder

If your document isn't covered by one of Mindee's Off-the-Shelf document endpoints,
you can create your own with the
[API Builder](https://developers.mindee.com/docs/build-your-first-document-parsing-api).

### Configuring the Client

Configuring custom documents is done with a list of dictionaries.
Each element in the list specifies a single custom endpoint.

There is no limit on the number of custom documents.

Specification for a custom endpoint configuration:

`document_type`\
The "document type" field in the "Settings" page of the API Builder.

`singular_name`\
The name of the attribute used to retrieve a _single_ document from the API response.

`plural_name`\
The name of the attribute used to retrieve _multiple_ documents from the API response.

`username`\
Your organization's username on the API Builder.

`api_key`\
Your API key for the endpoint.

```python
from mindee import Client

mindee_client = Client(
    custom_documents=[
        {
            "document_type": "my_custom_doc",
            "singular_name": "my_custom_doc",
            "plural_name": "my_custom_docs",
            "username": "JohnDoe",
            "api_key": "xxxxxxx",
        },
    ],
    raise_on_error=True
)
```

#### Environment variables
You can also set the API keys as environment variables,
it's the name of the `document_type` in uppercase:

* `MINDEE_MY_CUSTOM_DOC_API_KEY`


### Parsing Documents

The call to the `Client.parse` method is the same as with Off-the-Shelf documents.

```python
api_response = mindee_client.parse_from_path("/path/to/custom-doc.jpg", "my_custom_doc")
print(api_response.my_custom_doc)
```

## Command Line Usage

The CLI tool is provided mainly for quick tests and debugging.

```shell
# General help
python3 -m mindee -h

# Example command help
python3 -m mindee invoice -h

# Example parse command for Off-the-Shelf document
python3 -m mindee invoice --invoice-key xxxxxxx /path/to/invoice.pdf

# Works with environment variables
export MINDEE_INVOICE_API_KEY=xxxxxx
python3 -m mindee invoice /path/to/invoice.pdf

# Example parse command for a custom document
python3 -m mindee custom -u JohnDoe -k xxxxxxx my_custom_doc /path/to/invoice.pdf

# In the Git repo, there's a helper script for it
./mindee-cli.sh -h
```
