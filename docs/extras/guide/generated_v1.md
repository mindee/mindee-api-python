---
title: Generated OCR Python
category: 622b805aaec68102ea7fcbc2
slug: generated-api-python
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports generated APIs.
Generated APIs can theoretically support all APIs in a catch-all generic format.

# Quick-Start

```python
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Add the corresponding endpoint (document). Set the account_name to "mindee" if you are using OTS.
my_endpoint = mindee_client.create_endpoint(
    account_name="my-account",
    endpoint_name="my-endpoint",
    version="my-version"
)

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Parse the file.
# The endpoint must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.enqueue_and_parse(
    product.GeneratedV1,
    input_doc,
    endpoint=my_endpoint
)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)
```

# Generated Endpoints

You may have noticed in the previous step that in order to access a custom build, you will need to provide an account and an endpoint name at the very least.

Although it is optional, the version number should match the latest version of your build in most use-cases.
If it is not set, it will default to "1".

# Field Types

## Generated Fields

### Generated List Field

A `GeneratedListField` is a special type of custom list that implements the following:

- **values** (`List[Union[StringField`[GeneratedObjectField](#Generated-object-field)`]]`): the confidence score of the field prediction.
- **page_id** (`int`): only available for some documents ATM.

Since the inner contents can vary, the value isn't accessed through a property, but rather through the following functions:

- **contents_list()** (`-> List[Union[str, float]]`): returns a list of values for each element.
- **contents_string(separator=" ")** (`-> str`): returns a list of concatenated values, with an optional **separator** `str` between them.
> **Note:** the `str()` method returns a string representation of all values of this object, with an empty space between each of them.

### Generated Object Field

Unrecognized structures and sometimes values of `ListField`s are stored in a `GeneratedObjectField` structure, which is implemented dynamically depending on the object's structure.

- **page_id** (`Optional[int]`): the ID of the page, is `None` when at document-level.
- **raw_value** (`Optional[str]`): an optional field for when some post-processing has been done on fields (e.g. amounts). `None` in most instances.
- **confidence** (`Optional[float]`): the confidence score of the field prediction. Warning: support isn't guaranteed on all APIs.


> **Other fields**:No matter what, other fields will be stored in a dictionary-like structure with a `key: value` pair where `key` is a string and `value` is a nullable string. They can be accessed like any other regular value, but won't be suggested by your IDE.


### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.


# Attributes

Generated builds always have access to at least two attributes:

## Fields

**fields** (`Dict[str`: `List[Union[`[GeneratedListField](#generated-list-field), [GeneratedObjectField](#generated-object-field), `(#stringfield)[StringField]]]`):

```python
print(str(result.document.inference.prediction.fields["my-field"]))
```

### Nested fields

If your field `my-field` is a `GeneratedObjectField`, you can access its individual properties using the following syntax:

```python
print(str(result.document.inference.prediction.fields["my-field"].my_attribute))
```

# Questions?

[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
