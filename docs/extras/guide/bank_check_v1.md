---
title: US Bank Check OCR Python
---
The Python OCR SDK supports the [Bank Check API](https://platform.mindee.com/mindee/bank_check).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/bank_check/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Bank Check sample](https://github.com/mindee/client-lib-test-data/blob/main/products/bank_check/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.us.BankCheckV1, input_doc)

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
:Mindee ID: b9809586-57ae-4f84-a35d-a85b2be1f2a2
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/bank_check v1.0
:Rotation applied: Yes

Prediction
==========
:Check Issue Date: 2022-03-29
:Amount: 15332.90
:Payees: JOHN DOE
         JANE DOE
:Routing Number:
:Account Number: 7789778136
:Check Number: 0003401

Page Predictions
================

Page 0
------
:Check Position: Polygon with 21 points.
:Signature Positions: Polygon with 6 points.
:Check Issue Date: 2022-03-29
:Amount: 15332.90
:Payees: JOHN DOE
         JANE DOE
:Routing Number:
:Account Number: 7789778136
:Check Number: 0003401
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


### AmountField
The amount field `AmountField` only has one constraint: its **value** is an `Optional[float]`.

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
Some fields are constrained to the page level, and so will not be retrievable to through the document.

# Attributes
The following fields are extracted for Bank Check V1:

## Account Number
**account_number** ([StringField](#stringfield)): The check payer's account number.

```py
print(result.document.inference.prediction.account_number.value)
```

## Amount
**amount** ([AmountField](#amountfield)): The amount of the check.

```py
print(result.document.inference.prediction.amount.value)
```

## Check Number
**check_number** ([StringField](#stringfield)): The issuer's check number.

```py
print(result.document.inference.prediction.check_number.value)
```

## Check Position
[📄](#page-level-fields "This field is only present on individual pages.")**check_position** ([PositionField](#positionfield)): The position of the check on the document.

```py
for check_position_elem of result.document.check_position:
    print(check_position_elem.polygon)
```

## Check Issue Date
**date** ([DateField](#datefield)): The date the check was issued.

```py
print(result.document.inference.prediction.date.value)
```

## Payees
**payees** (List[[StringField](#stringfield)]): List of the check's payees (recipients).

```py
for payees_elem in result.document.inference.prediction.payees:
    print(payees_elem.value)
```

## Routing Number
**routing_number** ([StringField](#stringfield)): The check issuer's routing number.

```py
print(result.document.inference.prediction.routing_number.value)
```

## Signature Positions
[📄](#page-level-fields "This field is only present on individual pages.")**signatures_positions** (List[[PositionField](#positionfield)]): List of signature positions

```py
for page in result.document.inference.pages:
    for signatures_positions_elem of page.prediction.signatures_positions):
        print(signatures_positions_elem.polygon)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
