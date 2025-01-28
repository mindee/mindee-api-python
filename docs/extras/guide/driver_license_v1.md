---
title: Driver License OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-driver-license-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Driver License API](https://platform.mindee.com/mindee/driver_license).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/driver_license/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Driver License sample](https://github.com/mindee/client-lib-test-data/blob/main/products/driver_license/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.DriverLicenseV1,
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
:Mindee ID: fbdeae38-ada3-43ac-aa58-e01a3d47e474
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/driver_license v1.0
:Rotation applied: Yes

Prediction
==========
:Country Code: USA
:State: AZ
:ID: D12345678
:Category: D
:Last Name: Sample
:First Name: Jelani
:Date of Birth: 1957-02-01
:Place of Birth:
:Expiry Date: 2018-02-01
:Issued Date: 2013-01-10
:Issuing Authority:
:MRZ:
:DD Number: DD1234567890123456
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
The following fields are extracted for Driver License V1:

## Category
**category** ([StringField](#stringfield)): The category or class of the driver license.

```py
print(result.document.inference.prediction.category.value)
```

## Country Code
**country_code** ([StringField](#stringfield)): The alpha-3 ISO 3166 code of the country where the driver license was issued.

```py
print(result.document.inference.prediction.country_code.value)
```

## Date of Birth
**date_of_birth** ([DateField](#datefield)): The date of birth of the driver license holder.

```py
print(result.document.inference.prediction.date_of_birth.value)
```

## DD Number
**dd_number** ([StringField](#stringfield)): The DD number of the driver license.

```py
print(result.document.inference.prediction.dd_number.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): The expiry date of the driver license.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## First Name
**first_name** ([StringField](#stringfield)): The first name of the driver license holder.

```py
print(result.document.inference.prediction.first_name.value)
```

## ID
**id** ([StringField](#stringfield)): The unique identifier of the driver license.

```py
print(result.document.inference.prediction.id.value)
```

## Issued Date
**issued_date** ([DateField](#datefield)): The date when the driver license was issued.

```py
print(result.document.inference.prediction.issued_date.value)
```

## Issuing Authority
**issuing_authority** ([StringField](#stringfield)): The authority that issued the driver license.

```py
print(result.document.inference.prediction.issuing_authority.value)
```

## Last Name
**last_name** ([StringField](#stringfield)): The last name of the driver license holder.

```py
print(result.document.inference.prediction.last_name.value)
```

## MRZ
**mrz** ([StringField](#stringfield)): The Machine Readable Zone (MRZ) of the driver license.

```py
print(result.document.inference.prediction.mrz.value)
```

## Place of Birth
**place_of_birth** ([StringField](#stringfield)): The place of birth of the driver license holder.

```py
print(result.document.inference.prediction.place_of_birth.value)
```

## State
**state** ([StringField](#stringfield)): Second part of the ISO 3166-2 code, consisting of two letters indicating the US State.

```py
print(result.document.inference.prediction.state.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
