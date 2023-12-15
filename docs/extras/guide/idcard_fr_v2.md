---
title: FR Carte Nationale d'Identité OCR Python
---
The Python OCR SDK supports the [Carte Nationale d'Identité API](https://platform.mindee.com/mindee/idcard_fr).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/idcard_fr/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Carte Nationale d'Identité sample](https://github.com/mindee/client-lib-test-data/blob/main/products/idcard_fr/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.fr.IdCardV2, input_doc)

# Print a brief summary of the parsed data
print(result.document)
```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: d33828f1-ef7e-4984-b9df-a2bfaa38a78d
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/idcard_fr v2.0
:Rotation applied: Yes

Prediction
==========
:Nationality:
:Card Access Number: 175775H55790
:Document Number:
:Given Name(s): Victor
                Marie
:Surname: DAMBARD
:Alternate Name:
:Date of Birth: 1994-04-24
:Place of Birth: LYON 4E ARRONDISSEM
:Gender: M
:Expiry Date: 2030-04-02
:Mrz Line 1: IDFRADAMBARD<<<<<<<<<<<<<<<<<<075025
:Mrz Line 2: 170775H557903VICTOR<<MARIE<9404246M5
:Mrz Line 3:
:Date of Issue: 2015-04-03
:Issuing Authority: SOUS-PREFECTURE DE BELLE (02)

Page Predictions
================

Page 0
------
:Document Type: OLD
:Document Sides: RECTO & VERSO
:Nationality:
:Card Access Number: 175775H55790
:Document Number:
:Given Name(s): Victor
                Marie
:Surname: DAMBARD
:Alternate Name:
:Date of Birth: 1994-04-24
:Place of Birth: LYON 4E ARRONDISSEM
:Gender: M
:Expiry Date: 2030-04-02
:Mrz Line 1: IDFRADAMBARD<<<<<<<<<<<<<<<<<<075025
:Mrz Line 2: 170775H557903VICTOR<<MARIE<9404246M5
:Mrz Line 3:
:Date of Issue: 2015-04-03
:Issuing Authority: SOUS-PREFECTURE DE BELLE (02)
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


### ClassificationField
The classification field `ClassificationField` does not implement all the basic `BaseField` attributes. It only implements **value**, **confidence** and **page_id**.

> Note: a classification field's `value is always a `str`.

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Page-Level Fields
Some fields are constrained to the page level, and so will not be retrievable to through the document.

# Attributes
The following fields are extracted for Carte Nationale d'Identité V2:

## Alternate Name
**alternate_name** ([StringField](#stringfield)): The alternate name of the card holder.

```py
print(result.document.inference.prediction.alternate_name.value)
```

## Issuing Authority
**authority** ([StringField](#stringfield)): The name of the issuing authority.

```py
print(result.document.inference.prediction.authority.value)
```

## Date of Birth
**birth_date** ([DateField](#datefield)): The date of birth of the card holder.

```py
print(result.document.inference.prediction.birth_date.value)
```

## Place of Birth
**birth_place** ([StringField](#stringfield)): The place of birth of the card holder.

```py
print(result.document.inference.prediction.birth_place.value)
```

## Card Access Number
**card_access_number** ([StringField](#stringfield)): The card access number (CAN).

```py
print(result.document.inference.prediction.card_access_number.value)
```

## Document Number
**document_number** ([StringField](#stringfield)): The document number.

```py
print(result.document.inference.prediction.document_number.value)
```

## Document Sides
[📄](#page-level-fields "This field is only present on individual pages.")**document_side** ([ClassificationField](#classificationfield)): The sides of the document which are visible.

```py
for document_side_elem in result.document.document_side:
    print(document_side_elem.value)
```

## Document Type
[📄](#page-level-fields "This field is only present on individual pages.")**document_type** ([ClassificationField](#classificationfield)): The document type or format.

```py
for document_type_elem in result.document.document_type:
    print(document_type_elem.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): The expiry date of the identification card.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## Gender
**gender** ([StringField](#stringfield)): The gender of the card holder.

```py
print(result.document.inference.prediction.gender.value)
```

## Given Name(s)
**given_names** (List[[StringField](#stringfield)]): The given name(s) of the card holder.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## Date of Issue
**issue_date** ([DateField](#datefield)): The date of issue of the identification card.

```py
print(result.document.inference.prediction.issue_date.value)
```

## Mrz Line 1
**mrz1** ([StringField](#stringfield)): The Machine Readable Zone, first line.

```py
print(result.document.inference.prediction.mrz1.value)
```

## Mrz Line 2
**mrz2** ([StringField](#stringfield)): The Machine Readable Zone, second line.

```py
print(result.document.inference.prediction.mrz2.value)
```

## Mrz Line 3
**mrz3** ([StringField](#stringfield)): The Machine Readable Zone, third line.

```py
print(result.document.inference.prediction.mrz3.value)
```

## Nationality
**nationality** ([StringField](#stringfield)): The nationality of the card holder.

```py
print(result.document.inference.prediction.nationality.value)
```

## Surname
**surname** ([StringField](#stringfield)): The surname of the card holder.

```py
print(result.document.inference.prediction.surname.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
