---
title: FR Petrol Receipt OCR Python
---
The Python OCR SDK supports the [Petrol Receipt API](https://platform.mindee.com/mindee/petrol_receipts).

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.fr.PetrolReceiptV1, input_doc)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)
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


### Amount Field
The amount field `AmountField` only has one constraint: its **value** is an `Optional[float]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Fuel Type Field
The fuel type.

A `PetrolReceiptV1Fuel` implements the following attributes:

* **category** (`str`): The fuel category among a list of 4 possible choices.
* **raw_text** (`str`): As seen on the receipt.
Fields which are specific to this product; they are not used in any other product.

### Total Amount Field
The total amount paid.

A `PetrolReceiptV1Total` implements the following attributes:

* **amount** (`float`): The amount.

# Attributes
The following fields are extracted for Petrol Receipt V1:

## Fuel Type
**fuel** ([PetrolReceiptV1Fuel](#fuel-type-field)): The fuel type.

```py
print(result.document.inference.prediction.fuel.value)
```

## Price per Unit
**price** ([AmountField](#amountfield)): The price per unit of fuel.

```py
print(result.document.inference.prediction.price.value)
```

## Total Amount
**total** ([PetrolReceiptV1Total](#total-amount-field)): The total amount paid.

```py
print(result.document.inference.prediction.total.value)
```

## Volume
**volume** ([AmountField](#amountfield)): The volume of fuel purchased.

```py
print(result.document.inference.prediction.volume.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
