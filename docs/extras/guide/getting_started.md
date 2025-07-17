---
title: Getting Started
category: 622b805aaec68102ea7fcbc2
slug: python-getting-started
parentDoc: 609808f773b0b90051d839de
---
This guide will help you get started with the Mindee Python  OCR SDK to easily extract data from your documents.

The Python  OCR SDK supports [invoice](https://developers.mindee.com/docs/python-invoice-ocr), [passport](https://developers.mindee.com/docs/python-passport-ocr), [receipt](https://developers.mindee.com/docs/python-receipt-ocr) OCR APIs and [custom-built API](https://developers.mindee.com/docs/python-api-builder) from the API Builder.

You can view the source code on [GitHub](https://github.com/mindee/mindee-api-python), and the package on [PyPI](https://pypi.org/project/mindee/).

## Prerequisite

- Download and install [Python](https://www.python.org/downloads/). This library is officially supported on Python `3.7` to `3.11`. Note: support for `3.12` is on its way, but currently untested.
- Download and install [pip package manager](https://pip.pypa.io/en/stable/installation/).

## Installation

To quickly get started with the Python OCR SDK anywhere, the preferred installation method is via `pip`.

```shell
pip install mindee
```

### Development Installation

If you'll be modifying the source code, you'll need to install the development requirements to get started.

1. First clone the repo.

```shell
git clone git@github.com:mindee/mindee-api-python.git
```

2. Then navigate to the cloned directory and install all development requirements.

```shell
cd mindee-api-python
pip install -e ".[dev,test]"
```

## Updating the Version

It is important to always check the version of the Mindee OCR SDK you are using, as new and updated features won’t work on old versions.

To check the installed version:

```shell
pip show mindee
```

To get the latest version:

```shell
pip install mindee --upgrade
```

To install a specific version:

```shell
pip install mindee==<your_version>
```

## Usage

To get started with Mindee's APIs, you need to create a `Client` and you're ready to go.

Let's take a deep dive into how this works.

## Initializing the Client

The `Client` centralizes document configurations in a single object.

The `Client` requires your [API key](https://developers.mindee.com/docs/make-your-first-request#create-an-api-key).

You can either pass these directly to the constructor or through environment variables.

### Pass the API key directly

```python
from mindee import Client
#  Init with your API key
mindee_client = Client(api_key="my-api-key")
```

### Set the API key in the environment

API keys should be set as environment variables, especially for any production deployment.

The following environment variable will set the global API key:

```shell
MINDEE_API_KEY="my-api-key"
```

Then in your code:

```python
from mindee import Client
#  Init without an API key
mindee_client = Client()
```

### Setting the Request Timeout

The request timeout can be set using an environment variable:

```shell
MINDEE_REQUEST_TIMEOUT=200
```

## Loading a Document File

Before being able to send a document to the API, it must first be loaded.

You don't need to worry about different MIME types, the library will take care of handling  
all supported types automatically.

Once a document is loaded, interacting with it is done in exactly the same way, regardless  
of how it was loaded.

There are a few different ways of loading a document file, depending on your use case:

- [Path](#path)
- [File Object](#file-object)
- [Base64](#base64)
- [Bytes](#bytes)
- [URL](#url)

### Path

Load from a file directly from disk. Requires an absolute path, as a string.

```python
input_doc = mindee_client.source_from_path("/path/to/the/invoice.pdf")
```

### File Object

A normal Python file object with a path. **Must be in binary mode**.

```python
with open("/path/to/the/receipt.jpg", 'rb') as fo:
     input_doc = mindee_client.source_from_file(fo)
```

### Base64

Requires a base64 encoded string.

**Note**: The original filename is required when calling the method.

```python
b64_string = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLD...."
input_doc = mindee_client.source_from_b64string(b64_string, "receipt.jpg")
```

### Bytes

Requires raw bytes.

**Note**: The original filename is required when calling the method.

```python
raw_bytes = b"%PDF-1.3\n%\xbf\xf7\xa2\xfe\n1 0 ob..."
input_doc = mindee_client.source_from_bytes(raw_bytes, "invoice.pdf")
```

Loading from bytes is useful when using FastAPI `UploadFile` objects.

```python
@app.post("/process-file")
async def upload(upload: UploadFile):
    input_doc = mindee_client.source_from_bytes(
        upload.file.read(),
        filename=upload.filename
    )
```

### URL

Allows sending an URL directly.

**Note**: No local operations can be performed on the input (such as removing pages from a PDF).

```python
input_doc = mindee_client.source_from_url(url="https://www.example.com/invoice.pdf")
```

## Sending a File

To send a file to the API, we need to specify how to process the document.  
This will determine which API endpoint is used and how the API return will be handled internally by the library.

More specifically, we need to set a `mindee.product` class as the first parameter of the `parse` method.

This is because the `parse` method's' return type depends on its first argument.

Product classes inherit from the base `mindee.parsing.common.inference` class.

More information is available in each document-specific guide.

### Off-the-Shelf Documents

Simply setting the correct class and passing the input document is enough:

```python
result = mindee_client.parse(product.InvoiceV4, input_doc)
```

### Custom Documents (docTI & Custom APIs)

The endpoint to use must be created beforehand and subsequently passed to the `endpoint` argument of the `enqueue_and_parse` method:

```python
custom_endpoint = mindee_client.create_endpoint(
    "my-endpoin-url",
    "my-account-name",
    # "my-version" # optional
)
result = mindee_client.enqueue_and_get_inference(product.GeneratedV1, input_doc, endpoint=custom_endpoint)
```

This is because the `GeneratedV1` class is enough to handle the return processing, but the actual endpoint needs to be specified.


## Processing the Response

Results of a prediction can be retrieved in two different places:

- [Document level predictions](#document-level-prediction)
- [Page level predictions](#page-level-prediction)

### Document Level Prediction

The `document` attribute is an object specific to the type of document being processed.  
It is an instance of the `Document` class, to which a generic type is given.

It contains the data extracted from the entire document, all pages combined.  
It's possible to have the same field in various pages, but at the document level only the highest confidence field data will be shown (this is all done automatically at the API level).

Usage:
```py
print(resp.document)
```

A `document`'s fields (attributes) can be accessed through it's `prediction` attribute, which have types that can vary from one product to another.  
These attributes are detailed in each product's respective guide.

### Page Level Prediction

The `pages` attribute is a list of `Page` objects. `Page` is a wrapper around elements that extend the [`Document` class](#document-level-prediction).  
The `prediction` of a `Page` inherits from the product's own `Document`, and adds all page-specific fields to it.

The order of the elements in the list matches the order of the pages in the document.

All response objects have a `pages` property, regardless of the number of pages.  
Single-page documents will have a single entry.

Iteration over `pages` is done like with any list, for example:

```py
for page in resp.pages:
    print(page)
```

## Questions?

[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
