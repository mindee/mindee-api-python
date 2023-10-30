---
title: EU License Plate OCR Python
---
The Python OCR SDK supports the [License Plate API](https://platform.mindee.com/mindee/license_plates).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/license_plates/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![License Plate sample](https://github.com/mindee/client-lib-test-data/blob/main/products/license_plates/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.eu.LicensePlateV1, input_doc)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)
```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: f0f48232-2c80-4473-9c6f-88a09111b84d
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/license_plates v1.0
:Rotation applied: No

Prediction
==========
:License Plates: BY-323-YB

Page Predictions
================

Page 0
------
:License Plates: BY-323-YB
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
* **reconstructed** (`bool`): indicates whether or not an object was reconstructed (not extracted as the API gave it).

> **Note:** A `Point` simply refers to a List of two numbers (`[float, float]`).


Aside from the previous attributes, all basic fields have access to a custom `__str__` method that can be used to print their value as a string.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for License Plate V1:

## License Plates
**license_plates** (List[[StringField](#stringfield)]): List of all license plates found in the image.

```py
for license_plates_elem in result.document.inference.prediction.license_plates:
    print(license_plates_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
