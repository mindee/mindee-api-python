---
title: US W9 OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-us-w9-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [W9 API](https://platform.mindee.com/mindee/us_w9).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/us_w9/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![W9 sample](https://github.com/mindee/client-lib-test-data/blob/main/products/us_w9/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.us.W9V1, input_doc)

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
:Mindee ID: d7c5b25f-e0d3-4491-af54-6183afa1aaab
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/us_w9 v1.0
:Rotation applied: Yes

Prediction
==========

Page Predictions
================

Page 0
------
:Name: Stephen W Hawking
:SSN: 560758145
:Address: Somewhere In Milky Way
:City State Zip: Probably Still At Cambridge P O Box CB1
:Business Name:
:EIN: 942203664
:Tax Classification: individual
:Tax Classification Other Details:
:W9 Revision Date: august 2013
:Signature Position: Polygon with 4 points.
:Signature Date Position:
:Tax Classification LLC:
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


### PositionField
The position field `PositionField` does not implement all the basic `BaseField` attributes, only **bounding_box**, **polygon** and **page_id**. On top of these, it has access to:

* **rectangle** (`[Point, Point, Point, Point]`): a Polygon with four points that may be oriented (even beyond canvas).
* **quadrangle** (`[Point, Point, Point, Point]`): a free polygon made up of four points.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Page-Level Fields
Some fields are constrained to the page level, and so will not be retrievable at document level.

# Attributes
The following fields are extracted for W9 V1:

## Address
[📄](#page-level-fields "This field is only present on individual pages.")**address** ([StringField](#stringfield)): The street address (number, street, and apt. or suite no.) of the applicant.

```py
for address_elem in result.document.address:
    print(address_elem.value)
```

## Business Name
[📄](#page-level-fields "This field is only present on individual pages.")**business_name** ([StringField](#stringfield)): The business name or disregarded entity name, if different from Name.

```py
for business_name_elem in result.document.business_name:
    print(business_name_elem.value)
```

## City State Zip
[📄](#page-level-fields "This field is only present on individual pages.")**city_state_zip** ([StringField](#stringfield)): The city, state, and ZIP code of the applicant.

```py
for city_state_zip_elem in result.document.city_state_zip:
    print(city_state_zip_elem.value)
```

## EIN
[📄](#page-level-fields "This field is only present on individual pages.")**ein** ([StringField](#stringfield)): The employer identification number.

```py
for ein_elem in result.document.ein:
    print(ein_elem.value)
```

## Name
[📄](#page-level-fields "This field is only present on individual pages.")**name** ([StringField](#stringfield)): Name as shown on the applicant's income tax return.

```py
for name_elem in result.document.name:
    print(name_elem.value)
```

## Signature Date Position
[📄](#page-level-fields "This field is only present on individual pages.")**signature_date_position** ([PositionField](#positionfield)): Position of the signature date on the document.

```py
for signature_date_position_elem in result.document.signature_date_position:
    print(signature_date_position_elem.polygon)
```

## Signature Position
[📄](#page-level-fields "This field is only present on individual pages.")**signature_position** ([PositionField](#positionfield)): Position of the signature on the document.

```py
for signature_position_elem in result.document.signature_position:
    print(signature_position_elem.polygon)
```

## SSN
[📄](#page-level-fields "This field is only present on individual pages.")**ssn** ([StringField](#stringfield)): The applicant's social security number.

```py
for ssn_elem in result.document.ssn:
    print(ssn_elem.value)
```

## Tax Classification
[📄](#page-level-fields "This field is only present on individual pages.")**tax_classification** ([StringField](#stringfield)): The federal tax classification, which can vary depending on the revision date.

```py
for tax_classification_elem in result.document.tax_classification:
    print(tax_classification_elem.value)
```

## Tax Classification LLC
[📄](#page-level-fields "This field is only present on individual pages.")**tax_classification_llc** ([StringField](#stringfield)): Depending on revision year, among S, C, P or D for Limited Liability Company Classification.

```py
for tax_classification_llc_elem in result.document.tax_classification_llc:
    print(tax_classification_llc_elem.value)
```

## Tax Classification Other Details
[📄](#page-level-fields "This field is only present on individual pages.")**tax_classification_other_details** ([StringField](#stringfield)): Tax Classification Other Details.

```py
for tax_classification_other_details_elem in result.document.tax_classification_other_details:
    print(tax_classification_other_details_elem.value)
```

## W9 Revision Date
[📄](#page-level-fields "This field is only present on individual pages.")**w9_revision_date** ([StringField](#stringfield)): The Revision month and year of the W9 form.

```py
for w9_revision_date_elem in result.document.w9_revision_date:
    print(w9_revision_date_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
