---
title: US Healthcare Card OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-us-healthcare-card-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Healthcare Card API](https://platform.mindee.com/mindee/us_healthcare_cards).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/us_healthcare_cards/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Healthcare Card sample](https://github.com/mindee/client-lib-test-data/blob/main/products/us_healthcare_cards/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.us.HealthcareCardV1,
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
:Mindee ID: 0ced9f49-00c0-4a1d-8221-4a1538813a95
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/us_healthcare_cards v1.0
:Rotation applied: No

Prediction
==========
:Company Name: UnitedHealthcare
:Member Name: SUBSCRIBER SMITH
:Member ID: 123456789
:Issuer 80840:
:Dependents: SPOUSE SMITH
             CHILD1 SMITH
             CHILD2 SMITH
             CHILD3 SMITH
:Group Number: 98765
:Payer ID: 87726
:RX BIN: 610279
:RX GRP: UHEALTH
:RX PCN: 9999
:copays:
  +--------------+--------------+
  | Service Fees | Service Name |
  +==============+==============+
  | 20.00        | office visit |
  +--------------+--------------+
  | 300.00       | emergency    |
  +--------------+--------------+
  | 75.00        | urgent care  |
  +--------------+--------------+
  | 30.00        | specialist   |
  +--------------+--------------+
:Enrollment Date: 2023-09-13
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

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### copays Field
Is a fixed amount for a covered service.

A `HealthcareCardV1Copay` implements the following attributes:

* **service_fees** (`float`): The price of service.
* **service_name** (`str`): The name of service of the copay.

# Attributes
The following fields are extracted for Healthcare Card V1:

## Company Name
**company_name** ([StringField](#stringfield)): The name of the company that provides the healthcare plan.

```py
print(result.document.inference.prediction.company_name.value)
```

## copays
**copays** (List[[HealthcareCardV1Copay](#copays-field)]): Is a fixed amount for a covered service.

```py
for copays_elem in result.document.inference.prediction.copays:
    print(copays_elem.value)
```

## Dependents
**dependents** (List[[StringField](#stringfield)]): The list of dependents covered by the healthcare plan.

```py
for dependents_elem in result.document.inference.prediction.dependents:
    print(dependents_elem.value)
```

## Enrollment Date
**enrollment_date** ([DateField](#datefield)): The date when the member enrolled in the healthcare plan.

```py
print(result.document.inference.prediction.enrollment_date.value)
```

## Group Number
**group_number** ([StringField](#stringfield)): The group number associated with the healthcare plan.

```py
print(result.document.inference.prediction.group_number.value)
```

## Issuer 80840
**issuer_80840** ([StringField](#stringfield)): The organization that issued the healthcare plan.

```py
print(result.document.inference.prediction.issuer_80840.value)
```

## Member ID
**member_id** ([StringField](#stringfield)): The unique identifier for the member in the healthcare system.

```py
print(result.document.inference.prediction.member_id.value)
```

## Member Name
**member_name** ([StringField](#stringfield)): The name of the member covered by the healthcare plan.

```py
print(result.document.inference.prediction.member_name.value)
```

## Payer ID
**payer_id** ([StringField](#stringfield)): The unique identifier for the payer in the healthcare system.

```py
print(result.document.inference.prediction.payer_id.value)
```

## RX BIN
**rx_bin** ([StringField](#stringfield)): The BIN number for prescription drug coverage.

```py
print(result.document.inference.prediction.rx_bin.value)
```

## RX GRP
**rx_grp** ([StringField](#stringfield)): The group number for prescription drug coverage.

```py
print(result.document.inference.prediction.rx_grp.value)
```

## RX PCN
**rx_pcn** ([StringField](#stringfield)): The PCN number for prescription drug coverage.

```py
print(result.document.inference.prediction.rx_pcn.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
