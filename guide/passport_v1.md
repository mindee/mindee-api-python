---
title: Passport OCR Python
---
The Python OCR SDK supports the [Passport API](https://platform.mindee.com/mindee/passport).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/passport/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Passport sample](https://github.com/mindee/client-lib-test-data/blob/main/products/passport/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.PassportV1, input_doc)

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
:Mindee ID: 18e41f6c-16cd-4f8e-8cd2-00ca02a35764
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/passport v1.0
:Rotation applied: Yes

Prediction
==========
:Country Code: GBR
:ID Number: 707797979
:Given Name(s): HENERT
:Surname: PUDARSAN
:Date of Birth: 1995-05-20
:Place of Birth: CAMTETH
:Gender: M
:Date of Issue: 2012-04-22
:Expiry Date: 2017-04-22
:MRZ Line 1: P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<
:MRZ Line 2: 7077979792GBR9505209M1704224<<<<<<<<<<<<<<00

Page Predictions
================

Page 0
------
:Country Code: GBR
:ID Number: 707797979
:Given Name(s): HENERT
:Surname: PUDARSAN
:Date of Birth: 1995-05-20
:Place of Birth: CAMTETH
:Gender: M
:Date of Issue: 2012-04-22
:Expiry Date: 2017-04-22
:MRZ Line 1: P<GBRPUDARSAN<<HENERT<<<<<<<<<<<<<<<<<<<<<<<
:MRZ Line 2: 7077979792GBR9505209M1704224<<<<<<<<<<<<<<00
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

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Passport V1:

## Date of Birth
**birth_date** ([DateField](#datefield)): The date of birth of the passport holder.

```py
print(result.document.inference.prediction.birth_date.value)
```

## Place of Birth
**birth_place** ([StringField](#stringfield)): The place of birth of the passport holder.

```py
print(result.document.inference.prediction.birth_place.value)
```

## Country Code
**country** ([StringField](#stringfield)): The country's 3 letter code (ISO 3166-1 alpha-3).

```py
print(result.document.inference.prediction.country.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): The expiry date of the passport.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## Gender
**gender** ([StringField](#stringfield)): The gender of the passport holder.

```py
print(result.document.inference.prediction.gender.value)
```

## Given Name(s)
**given_names** (List[[StringField](#stringfield)]): The given name(s) of the passport holder.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## ID Number
**id_number** ([StringField](#stringfield)): The passport's identification number.

```py
print(result.document.inference.prediction.id_number.value)
```

## Date of Issue
**issuance_date** ([DateField](#datefield)): The date the passport was issued.

```py
print(result.document.inference.prediction.issuance_date.value)
```

## MRZ Line 1
**mrz1** ([StringField](#stringfield)): Machine Readable Zone, first line

```py
print(result.document.inference.prediction.mrz1.value)
```

## MRZ Line 2
**mrz2** ([StringField](#stringfield)): Machine Readable Zone, second line

```py
print(result.document.inference.prediction.mrz2.value)
```

## Surname
**surname** ([StringField](#stringfield)): The surname of the passport holder.

```py
print(result.document.inference.prediction.surname.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
