---
title: Delivery note OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-delivery-note-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Delivery note API](https://platform.mindee.com/mindee/delivery_notes).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/delivery_notes/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Delivery note sample](https://github.com/mindee/client-lib-test-data/blob/main/products/delivery_notes/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.DeliveryNoteV1,
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
:Mindee ID: d5ead821-edec-4d31-a69a-cf3998d9a506
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/delivery_notes v1.0
:Rotation applied: Yes

Prediction
==========
:Delivery Date: 2019-10-02
:Delivery Number: INT-001
:Supplier Name: John Smith
:Supplier Address: 4490 Oak Drive, Albany, NY 12210
:Customer Name: Jessie M Horne
:Customer Address: 4312 Wood Road, New York, NY 10031
:Total Amount: 204.75
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


### AmountField
The amount field `AmountField` only has one constraint: its **value** is an `Optional[float]`.

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Delivery note V1:

## Customer Address
**customer_address** ([StringField](#stringfield)): The address of the customer receiving the goods.

```py
print(result.document.inference.prediction.customer_address.value)
```

## Customer Name
**customer_name** ([StringField](#stringfield)): The name of the customer receiving the goods.

```py
print(result.document.inference.prediction.customer_name.value)
```

## Delivery Date
**delivery_date** ([DateField](#datefield)): The date on which the delivery is scheduled to arrive.

```py
print(result.document.inference.prediction.delivery_date.value)
```

## Delivery Number
**delivery_number** ([StringField](#stringfield)): A unique identifier for the delivery note.

```py
print(result.document.inference.prediction.delivery_number.value)
```

## Supplier Address
**supplier_address** ([StringField](#stringfield)): The address of the supplier providing the goods.

```py
print(result.document.inference.prediction.supplier_address.value)
```

## Supplier Name
**supplier_name** ([StringField](#stringfield)): The name of the supplier providing the goods.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Total Amount
**total_amount** ([AmountField](#amountfield)): The total monetary value of the goods being delivered.

```py
print(result.document.inference.prediction.total_amount.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
