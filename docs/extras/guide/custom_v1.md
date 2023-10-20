---
title: Custom API Python
---
The Python OCR SDK supports [custom-built APIs](https://developers.mindee.com/docs/build-your-first-document-parsing-api).
If your document isn't covered by one of Mindee's Off-the-Shelf APIs, you can create your own API using the[API Builder](https://platform.mindee.com/api-builder).

# Quick-Start

```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")
my_endpoint = mindee_client.create_endpoint(
    endpoint_name="my-endpoint",
    account_name="my-account-name",
    version="my-version",
)

# Parse the document as an invoice by passing the appropriate type
result = mindee_client.parse(
    product.CustomV1,
    input_doc,
    endpoint=my_endpoint
)

# Print a brief summary of the parsed data
print(result.document)
```

# Custom Endpoints

You may have noticed in the previous step that in order to access a custom build, you will need to provide an account and an endpoint name at the very least.

Although it is optional, the version number should match the latest version of your build in most use-cases.
If it is not set, it will default to "1".


# Field Types

## Custom Fields

### List Field

A `ListField` is a special type of custom list that implements the following:

* **confidence** (`float`): the confidence score of the field prediction.
* **page_id** (`int`): the ID of the page.
* **reconstructed** (`bool`): indicates whether or not an object was reconstructed (not extracted as the API gave it).

Since the inner contents can vary, the value isn't accessed through a property, but rather through the following functions:
* **contents_list()** (`-> List[Union[str, float]]`): returns a list of values for each element.
* **contents_string(separator=" ")** (`-> str`): returns a list of concatenated values, with an optional **separator** `str` between them.
* **__str__()**: returns a string representation of all values, with an empty space between each of them.


### Classification Field

A `ClassificationField` is a special type of custom classification that implements the following:

* **value** (`str`): the value of the classification. Corresponds to one of the values specified during training.
* **confidence** (`float`): the confidence score of the field prediction.
* **__str__()**: returns a string representation of all values, with an empty space between each of them.

# Attributes

Custom builds always have access to at least two attributes:

## Fields

**fields** (Dict[`str`: List[ListField](#list-field)]): 

```python
print(str(result.document.inference.prediction.fields["my-field"]))
```

## Classifications

**classifications** ([`str`: List[ClassificationField](#classification-field)]): The purchase category among predefined classes.

```python
print(str(result.document.inference.prediction.classifications["my-classification"]))
```

# Questions?

[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
