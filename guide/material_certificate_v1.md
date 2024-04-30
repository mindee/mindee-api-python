---
title: Material Certificate OCR Python
---
The Python OCR SDK supports the [Material Certificate API](https://platform.mindee.com/mindee/material_certificate).

The [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/material_certificate/default_sample.jpg) can be used for testing purposes.
![Material Certificate sample](https://github.com/mindee/client-lib-test-data/blob/main/products/material_certificate/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse
from time import sleep

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.MaterialCertificateV1,
    input_doc,
)

# Print a brief summary of the parsed data
print(result.document)
```
# Field Types
## Standard Fields
These fields are generic and used in several products.

### BasicField
Each prediction object contains a set of fields that inherit from the generic `BaseField` class.
A typical `BaseField` object will have the following attributes:

* **value** (`Union[float, str]`): corresponds to the field value. Can be `None` if no value was extracted.
* **confidence** (`float`): the confidence score of the field prediction.
* **bounding_box** (`[Point, Point, Point, Point]`): contains exactly 4 relative vertices (points) coordinates of a right rectangle containing the field in the document.
* **polygon** (`List[Point]`): contains the relative vertices coordinates (`Point`) of a polygon containing the field in the image.
* **page_id** (`int`): the ID of the page, is `None` when at document-level.
* **reconstructed** (`bool`): indicates whether an object was reconstructed (not extracted as the API gave it).

> **Note:** A `Point` simply refers to a List of two numbers (`[float, float]`).


Aside from the previous attributes, all basic fields have access to a custom `__str__` method that can be used to print their value as a string.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Material Certificate V1:

## Certificate Type
**certificate_type** ([StringField](#stringfield)): The type of certification.

```py
print(result.document.inference.prediction.certificate_type.value)
```

## Heat Number
**heat_number** ([StringField](#stringfield)): Heat Number is a unique identifier assigned to a batch of material produced in a manufacturing process.

```py
print(result.document.inference.prediction.heat_number.value)
```

## Norm
**norm** ([StringField](#stringfield)): The international standard used for certification.

```py
print(result.document.inference.prediction.norm.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
