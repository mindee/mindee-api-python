---
title: Custom API Python (Deprecated)
category: 622b805aaec68102ea7fcbc2
slug: python-api-builder
parentDoc: 609808f773b0b90051d839de
---
> 🚧 This product is still supported, but is considered to be deprecated. If you are looking for the DocTI API documentation, you can find it [here](https://developers.mindee.com/docs/generated-api-python).

The Python OCR SDK supports [custom-built APIs](https://developers.mindee.com/docs/build-your-first-document-parsing-api).
If your document isn't covered by one of Mindee's Off-the-Shelf APIs, you can create your own API using the[API Builder](https://platform.mindee.com/api-builder).

# Quick-Start

```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Add your custom endpoint (document)
my_endpoint = mindee_client.create_endpoint(
    account_name="my-account",
    endpoint_name="my-endpoint",
)

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the file.
# The endpoint must be specified since it cannot be determined from the class.
result = mindee_client.parse(
    product.CustomV1,
    input_doc,
    endpoint=my_endpoint
)

# Print a brief summary of the parsed data
print(result.document)

# Iterate over all the fields in the document
for field_name, field_values in result.document.fields.items():
    print(field_name, "=", field_values)
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
* **reconstructed** (`bool`): indicates whether or not an object was reconstructed (not extracted as the API gave it).
* **values** (`List[`[ListFieldValue](#list-field-value)`]`): list of value fields

Since the inner contents can vary, the value isn't accessed through a property, but rather through the following functions:
* **contents_list()** (`-> List[Union[str, float]]`): returns a list of values for each element.
* **contents_string(separator=" ")** (`-> str`): returns a list of concatenated values, with an optional **separator** `str` between them.
> **Note:** the `str()` method returns a string representation of all values of this object, with an empty space between each of them.


#### List Field Value

Values of `ListField`s are stored in a `ListFieldValue` structure, which is implemented as follows:
* **content** (`str`): extracted content of the prediction
* **confidence** (`float`): the confidence score of the prediction
* **bounding_box** (`BBox`): 4 relative vertices corrdinates of a rectangle containing the word in the document.
* **polygon** (`Polygon`): vertices of a polygon containing the word.
* **page_id** (`int`): the ID of the page, is `None` when at document-level.


### Classification Field

A `ClassificationField` is a special type of custom classification that implements the following:

* **value** (`str`): the value of the classification. Corresponds to one of the values specified during training.
* **confidence** (`float`): the confidence score of the field prediction.
> **Note:** the `str()` method returns a string representation of all values of this object, with an empty space between each of them.

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


# 🧪 Custom Line Items

> **⚠️ Warning**: Custom Line Items are an **experimental** feature, results may vary.


Though not supported directly in the API, sometimes you might need to reconstitute line items by hand.
The library provides a tool for this very purpose:

## columns_to_line_items()
The **columns_to_line_items()** function can be called from the document and page level prediction objects.

It takes the following arguments:

* **anchor_names** (`List[str]`): a list of the names of possible anchor (field) candidate for the horizontal placement a line. If all provided anchors are invalid, the `CustomLine` won't be built.
* **field_names** (`List[str]`): a list of fields to retrieve the values from
* **height_tolerance** (`float`): Optional, the height tolerance used to build the line. It helps when the height of a line can vary unexpectedly.

Example use:

```python
# document-level
response.document.inference.prediction.columns_to_line_items(
  anchor_names,
  field_names,
  0.011 # optional, defaults to 0.01
)

# page-level
response.document.pages[0].prediction.columns_to_line_items(
    anchor_names,
    field_names,
    0.011 # optional, defaults to 0.01
)
```

It returns a list of [CustomLine](#CustomLine) objects.

## CustomLine

`CustomLine` represents a line as it has been read from column fields. It has the following attributes:

* **row_number** (`int`): Number of a given line. Starts at 1.
* **fields** (`Dict[str, ListFieldValue]`[]): List of the fields associated with the line, indexed by their column name.
* **bbox** (`BBox`): Simple bounding box of the current line representing the 4 minimum & maximum coordinates as `float` values.


# Questions?

[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
