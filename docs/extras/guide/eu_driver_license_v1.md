---
title: EU Driver License OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-eu-driver-license-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Driver License API](https://platform.mindee.com/mindee/eu_driver_license).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/eu_driver_license/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Driver License sample](https://github.com/mindee/client-lib-test-data/blob/main/products/eu_driver_license/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.eu.DriverLicenseV1, input_doc)

# Print a summary of the API result
print(result.document)

# Print the document-level summary
# print(result.document.inference.prediction)

```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: b19cc32e-b3e6-4ff9-bdc7-619199355d54
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/eu_driver_license v1.0
:Rotation applied: Yes

Prediction
==========
:Country Code: FR
:Document ID: 13AA00002
:Driver License Category: AM A1 B1 B D BE DE
:Last Name: MARTIN
:First Name: PAUL
:Date Of Birth: 1981-07-14
:Place Of Birth: Utopiacity
:Expiry Date: 2018-12-31
:Issue Date: 2013-01-01
:Issue Authority: 99999UpiaCity
:MRZ: D1FRA13AA000026181231MARTIN<<9
:Address:

Page Predictions
================

Page 0
------
:Photo: Polygon with 4 points.
:Signature: Polygon with 4 points.
:Country Code: FR
:Document ID: 13AA00002
:Driver License Category: AM A1 B1 B D BE DE
:Last Name: MARTIN
:First Name: PAUL
:Date Of Birth: 1981-07-14
:Place Of Birth: Utopiacity
:Expiry Date: 2018-12-31
:Issue Date: 2013-01-01
:Issue Authority: 99999UpiaCity
:MRZ: D1FRA13AA000026181231MARTIN<<9
:Address:
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


### PositionField
The position field `PositionField` does not implement all the basic `BaseField` attributes, only **bounding_box**, **polygon** and **page_id**. On top of these, it has access to:

* **rectangle** (`[Point, Point, Point, Point]`): a Polygon with four points that may be oriented (even beyond canvas).
* **quadrangle** (`[Point, Point, Point, Point]`): a free polygon made up of four points.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Page-Level Fields
Some fields are constrained to the page level, and so will not be retrievable at document level.

# Attributes
The following fields are extracted for Driver License V1:

## Address
**address** ([StringField](#stringfield)): EU driver license holders address

```py
print(result.document.inference.prediction.address.value)
```

## Driver License Category
**category** ([StringField](#stringfield)): EU driver license holders categories

```py
print(result.document.inference.prediction.category.value)
```

## Country Code
**country_code** ([StringField](#stringfield)): Country code extracted as a string.

```py
print(result.document.inference.prediction.country_code.value)
```

## Date Of Birth
**date_of_birth** ([DateField](#datefield)): The date of birth of the document holder

```py
print(result.document.inference.prediction.date_of_birth.value)
```

## Document ID
**document_id** ([StringField](#stringfield)): ID number of the Document.

```py
print(result.document.inference.prediction.document_id.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): Date the document expires

```py
print(result.document.inference.prediction.expiry_date.value)
```

## First Name
**first_name** ([StringField](#stringfield)): First name(s) of the driver license holder

```py
print(result.document.inference.prediction.first_name.value)
```

## Issue Authority
**issue_authority** ([StringField](#stringfield)): Authority that issued the document

```py
print(result.document.inference.prediction.issue_authority.value)
```

## Issue Date
**issue_date** ([DateField](#datefield)): Date the document was issued

```py
print(result.document.inference.prediction.issue_date.value)
```

## Last Name
**last_name** ([StringField](#stringfield)): Last name of the driver license holder.

```py
print(result.document.inference.prediction.last_name.value)
```

## MRZ
**mrz** ([StringField](#stringfield)): Machine-readable license number

```py
print(result.document.inference.prediction.mrz.value)
```

## Photo
[📄](#page-level-fields "This field is only present on individual pages.")**photo** ([PositionField](#positionfield)): Has a photo of the EU driver license holder

```py
for photo_elem in result.document.photo:
    print(photo_elem.polygon)
```

## Place Of Birth
**place_of_birth** ([StringField](#stringfield)): Place where the driver license holder was born

```py
print(result.document.inference.prediction.place_of_birth.value)
```

## Signature
[📄](#page-level-fields "This field is only present on individual pages.")**signature** ([PositionField](#positionfield)): Has a signature of the EU driver license holder

```py
for signature_elem in result.document.signature:
    print(signature_elem.polygon)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
