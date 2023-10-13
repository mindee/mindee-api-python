---
title: Proof of Address OCR Python
---
The Python OCR SDK supports the [Proof of Address API](https://platform.mindee.com/mindee/proof_of_address).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/proof_of_address/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Proof of Address sample](https://github.com/mindee/client-lib-test-data/blob/main/products/proof_of_address/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.ProofOfAddressV1, input_doc)

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
:Mindee ID: 3a7e1da6-d4d0-4704-af91-051fe5484c2e
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/proof_of_address v1.0
:Rotation applied: Yes

Prediction
==========
:Locale: en; en; USD;
:Issuer Name: PPL ELECTRIC UTILITIES
:Issuer Company Registrations:
:Issuer Address: 2 NORTH 9TH STREET CPC-GENN1 ALLENTOWN,PA 18101-1175
:Recipient Name:
:Recipient Company Registrations:
:Recipient Address: 123 MAIN ST ANYTOWN,PA 18062
:Dates: 2011-07-27
        2011-07-06
        2011-08-03
        2011-07-27
        2011-06-01
        2011-07-01
        2010-07-01
        2010-08-01
        2011-07-01
        2009-08-01
        2010-07-01
        2011-07-27
:Date of Issue: 2011-07-27

Page Predictions
================

Page 0
------
:Locale: en; en; USD;
:Issuer Name: PPL ELECTRIC UTILITIES
:Issuer Company Registrations:
:Issuer Address: 2 NORTH 9TH STREET CPC-GENN1 ALLENTOWN,PA 18101-1175
:Recipient Name:
:Recipient Company Registrations:
:Recipient Address: 123 MAIN ST ANYTOWN,PA 18062
:Dates: 2011-07-27
        2011-07-06
        2011-08-03
        2011-07-27
        2011-06-01
        2011-07-01
        2010-07-01
        2010-08-01
        2011-07-01
        2009-08-01
        2010-07-01
        2011-07-27
:Date of Issue: 2011-07-27
```

# Field Types
## Standard Fields
These fields are generic and used in several products.

### Basic Field
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


### Company Registration Field
Aside from the basic `BaseField` attributes, the company registration field `CompanyRegistrationField` also implements the following:

* **type** (`str`): the type of company.

### Date Field
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### Locale Field
The locale field `LocaleField` only implements the **value**, **confidence** and **page_id** base `BaseField` attributes, but it comes with its own:

* **language** (`str`): ISO 639-1 language code (e.g.: `en` for English). Can be `None`.
* **country** (`str`): ISO 3166-1 alpha-2 or ISO 3166-1 alpha-3 code for countries (e.g.: `GRB` or `GB` for "Great Britain"). Can be `None`.
* **currency** (`str`): ISO 4217 code for currencies (e.g.: `USD` for "US Dollars"). Can be `None`.

### String Field
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Proof of Address V1:

## Date of Issue
**date** : The date the document was issued.

```py
print(result.document.inference.prediction.date.value)
```

## Dates
**dates** : List of dates found on the document.

```py
for dates_elem in result.document.inference.prediction.dates:
    print(dates_elem.value)
```

## Issuer Address
**issuer_address** : The address of the document's issuer.

```py
print(result.document.inference.prediction.issuer_address.value)
```

## Issuer Company Registrations
**issuer_company_registration** : List of company registrations found for the issuer.

```py
for issuer_company_registration_elem in result.document.inference.prediction.issuer_company_registration:
    print(issuer_company_registration_elem.value)
```

## Issuer Name
**issuer_name** : The name of the person or company issuing the document.

```py
print(result.document.inference.prediction.issuer_name.value)
```

## Locale
**locale** : The locale detected on the document.

```py
print(result.document.inference.prediction.locale.value)
```

## Recipient Address
**recipient_address** : The address of the recipient.

```py
print(result.document.inference.prediction.recipient_address.value)
```

## Recipient Company Registrations
**recipient_company_registration** : List of company registrations found for the recipient.

```py
for recipient_company_registration_elem in result.document.inference.prediction.recipient_company_registration:
    print(recipient_company_registration_elem.value)
```

## Recipient Name
**recipient_name** : The name of the person or company receiving the document.

```py
print(result.document.inference.prediction.recipient_name.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
