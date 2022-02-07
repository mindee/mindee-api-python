# Mindee API Helper Library for Python

## Quick Start
Here's the TL;DR of getting started.

First, get an [API Key](https://developers.mindee.com/docs/make-your-first-request#create-an-api-key)

Then, install this library:
```shell script
pip install mindee
```

Finally, Python away!
```python
from mindee import Client

# Init a new client and pass it the Invoice API key
mindee_client = Client().config_invoice("my-invoice-api-key")

# Load a file from disk and parse it
api_response = mindee_client.doc_from_path("/path/to/the/invoice.pdf").parse("invoice")

# Print a brief summary of the parsed data
print(api_response.invoice)
```

There's more to it than that for those that need more features, read on for the juicy details.

The full Mindee documentation is also
[available](https://developers.mindee.com/docs/getting-started).

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

Then navigate to the cloned directory and install all development requirements:
```shell script
cd mindee-api-python
pip install .[dev,test]
```

### The Client
The client centralizes document configurations in a single object.

Documents are added to the `Client` using a *config_xxx* method.

You only need to specify the API keys for the document endpoints you'll be using.

#### Single Document
You can have a separate client for each document.

If you have only a single document type you're working with,
this is the easiest way to get started.

```python
from mindee import Client

receipt_client = Client().config_receipt("receipt-api-key")

invoice_client = Client().config_invoice("invoice-api-key")

financial_client = Client().config_financial_doc("receipt-api-key", "invoice-api-key")

passport_client = Client().config_passport("passport-api-key")

pokemon_client = Client().config_custom_doc(
    document_type="pokemon-card",
    singular_name="card",
    plural_name="cards",
    account_name="pikachu",
    api_key="pokemon-card-api-key"
)
```
You can always add more document types to the client later, see the section below.

#### Multiple Documents
you can have all your documents configured in the same client.

If you're working with multiple document types this is the easiest way to get started.

Since each *config_xxx* method returns the current `Client` object,
you can simply chain all the calls together:

```python
from mindee import Client

mindee_client = (
    Client()
        .config_receipt("receipt-api-key")
        .config_invoice("invoice-api-key")
        .config_financial_doc("receipt-api-key", "invoice-api-key")
        .config_passport("passport-api-key")
        .config_custom_doc(
        document_type="pokemon-card",
        singular_name="card",
        plural_name="cards",
        account_name="pikachu",
        api_key="pokemon-card-api-key"
    )
)
```

#### Mix and Match
You can also mix and match. This approach is useful to have groups of documents
handled in different ways.

```python
from mindee import Client

strict_client = (
    Client(raise_on_error=True)
        .config_receipt("receipt-api-key")
        .config_invoice("invoice-api-key")
        .config_financial_doc("receipt-api-key", "invoice-api-key")
)

permissive_client = (
    Client(raise_on_error=False)
        .config_passport("passport-api-key")
        .config_custom_doc(
        document_type="pokemon-card",
        singular_name="card",
        plural_name="cards",
        account_name="pikachu",
        api_key="pokemon-card-api-key"
    )
)
```

### Environment Variables
You can also set the API keys as environment variables.\
You **are** using environment variables in production, right?

* `MINDEE_RECEIPT_API_KEY`
* `MINDEE_INVOICE_API_KEY`
* `MINDEE_PASSPORT_API_KEY`

Custom documents can be set as well,
in keeping with the example above:
* `MINDEE_PIKACHU_POKEMON_CARD_API_KEY`

### Loading Documents
You can load your document in several ways.

The various methods are called from the `Client` and
return an object you can then serialize to the API.

#### Path
An absolute path, as a string.
```python
loaded_doc = mindee_client.doc_from_path('/path/to/invoice.pdf')
```

#### File Object
A normal Python file object/handle. Must be in binary mode!
```python
with open('/path/to/receipt.jpg', 'rb') as fo:
     loaded_doc = mindee_client.doc_from_file(fo)
```

#### Base64
A base64 encoded string.\
Note that the original filename of the encoded file is required when calling the method.
```python
b64_string = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLD...."
loaded_doc = mindee_client.doc_from_b64string(b64_string, "receipt.jpg")
```

#### Bytes
Raw bytes.\
Note that the original filename is required when calling the method.
```python
raw_bytes = b"%PDF-1.3\n%\xbf\xf7\xa2\xfe\n1 0 ob..."
loaded_doc = mindee_client.doc_from_bytes(raw_bytes, "invoice.pdf")
```

Loading from bytes is useful, for example,
when using FastAPI `UploadFile` objects:
```python
@app.post("/invoice")
async def upload(upload: UploadFile):
    invoice_data = mindee_client.doc_from_bytes(
        upload.file.read(),
        filename=upload.filename
    ).parse(
        "invoice"
    )
```

#### Document Parsing
Once a document is loaded, you can send it to the API endpoint(s).

The document parse type must be specified when calling the `parse` method.

The object containing the parsed data will be an attribute of the response object.

Receipts
```python
api_response = loaded_doc.parse("receipt")
print(api_response.receipt)
```
Invoices
```python
api_response = loaded_doc.parse("invoice")
print(api_response.invoice)
```
Passports
```python
api_response = loaded_doc.parse("passport")
print(api_response.passport)
```

Financial, mixed data flow of invoices and receipts.\
**Note:** You'll need an API key for _both_ invoice and receipts endpoints.
```python
api_response = loaded_doc.parse("financial_doc")
```

## Usage with the API Builder
If your document isn't covered by one of Mindee's Off-the-Shelf document endpoints,
you can create your own with the
[API Builder](https://developers.mindee.com/docs/build-your-first-document-parsing-api).

### Configuring the Client
Specification for a custom endpoint configuration:

`document_type`\
The "document type" field in the "Settings" page of the API Builder.

`singular_name`\
The name of the attribute used to retrieve a _single_ document from the API response.

`plural_name`\
The name of the attribute used to retrieve _multiple_ documents from the API response.

`account_name`\
Your organization's username in the API Builder.

`api_key`\
Your API key for the endpoint.

```python
from mindee import Client

mindee_client = Client().config_custom_doc(
    document_type="pokemon-card",
    singular_name="card",
    plural_name="cards",
    account_name="pikachu",
    api_key="pokemon-card-api-key"
)
```

#### Environment Variables
You can also set the API keys as environment variables.

The format is `MINDEE_<username>_<document_type>_API_KEY`\
Where `<username>` and `<document_type>` are uppercase, any `-` replaced with `_`.

The example above would look for:
* `MINDEE_PIKACHU_POKEMON_CARD_API_KEY`


### Parsing Documents
The call to the `parse` method is the same as with Off-the-Shelf documents.

```python
loaded_doc = mindee_client.doc_from_path("/my/cards/pikachu.jpg")
parsed_data = loaded_doc.parse("pokemon-card")
```

**NOTE:** If your custom document has the same name as an Off-The-Shelf document,
you must specify your username when calling the `parse` method.

```python
from mindee import Client

mindee_client = Client().config_custom_doc(
    document_type="receipt",
    singular_name="receipt",
    plural_name="receipts",
    account_name="JohnDoe",
    api_key="johndoe-receipt-api-key"
)

loaded_doc = mindee_client.doc_from_path("/path/to/receipt.jpg")
parsed_data = loaded_doc.parse("receipt", "JohnDoe")
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
python3 -m mindee custom -u pikachu -k xxxxxxx pokemon_card /path/to/card.jpg

# You can get the full parsed output as well
python3 -m mindee invoice -o parsed /path/to/invoice.pdf

# In the Git repo, there's a helper script for it
./mindee-cli.sh -h
```

## License
Copyright © Mindee

Distributed under the MIT License.
