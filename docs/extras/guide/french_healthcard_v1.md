---
title: FR Health Card OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-fr-health-card-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Health Card API](https://platform.mindee.com/mindee/french_healthcard).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/french_healthcard/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Health Card sample](https://github.com/mindee/client-lib-test-data/blob/main/products/french_healthcard/default_sample.jpg?raw=true)

# Quick-Start
```py
#
# Install the Python client library by running:
# pip install mindee
#

from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.fr.HealthCardV1,
    input_doc,
)

# Print a brief summary of the parsed data
print(result.document)

```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: 9ee2733d-933a-4dcd-a73a-a31395e3b288
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/french_healthcard v1.0
:Rotation applied: Yes

Prediction
==========
:Given Name(s): NATHALIE
:Surname: DURAND
:Social Security Number: 2 69 05 49 588 157 80
:Issuance Date: 2007-01-01
```

# Field Types
## Standard Fields
These fields are generic and used in several products.

### BaseField
Each prediction object contains a set of fields that inherit from the generic `BaseField` class.
A typical `BaseField` object will have the following attributes:

* **value** (`Union[float, str]`): corresponds to the field value. Can be `None` if no value was extracted.
* **confidence** (`float`): the confidence score of the field prediction.
* **bounding_box** (`[Point, Point, Point, Point]`): contains exactly 4 relative vertices (points) coordinates of a right rectangle containing the field in the document.
* **polygon** (`List[Point]`): contains the relative vertices coordinates (`Point`) of a polygon containing the field in the image.
* **page_id** (`int`): the ID of the page, always `None` when at document-level.
* **reconstructed** (`bool`): indicates whether an object was reconstructed (not extracted as the API gave it).

> **Note:** A `Point` simply refers to a List of two numbers (`[float, float]`).


Aside from the previous attributes, all basic fields have access to a custom `__str__` method that can be used to print their value as a string.

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Health Card V1:

## Given Name(s)
**given_names** (List[[StringField](#stringfield)]): The given names of the card holder.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## Issuance Date
**issuance_date** ([DateField](#datefield)): The date when the carte vitale document was issued.

```py
print(result.document.inference.prediction.issuance_date.value)
```

## Social Security Number
**social_security** ([StringField](#stringfield)): The social security number of the card holder.

```py
print(result.document.inference.prediction.social_security.value)
```

## Surname
**surname** ([StringField](#stringfield)): The surname of the card holder.

```py
print(result.document.inference.prediction.surname.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
