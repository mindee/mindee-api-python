---
title: International ID OCR Python
---
The Python OCR SDK supports the [International ID API](https://platform.mindee.com/mindee/international_id).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/international_id/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![International ID sample](https://github.com/mindee/client-lib-test-data/blob/main/products/international_id/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.InternationalIdV2, input_doc)

# Print a summary of the API result
print(result.document)

# Print the document-level summary
# print(result.document.inference.prediction)
```

**Output (RST):**
```rst
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

# Attributes
The following fields are extracted for International ID V2:

## Address
**address** ([StringField](#stringfield)): The physical address of the document holder.

```py
print(result.document.inference.prediction.address.value)
```

## Birth Date
**birth_date** ([DateField](#datefield)): The date of birth of the document holder.

```py
print(result.document.inference.prediction.birth_date.value)
```

## Birth Place
**birth_place** ([StringField](#stringfield)): The place of birth of the document holder.

```py
print(result.document.inference.prediction.birth_place.value)
```

## Country of Issue
**country_of_issue** ([StringField](#stringfield)): The country where the document was issued.

```py
print(result.document.inference.prediction.country_of_issue.value)
```

## Document Number
**document_number** ([StringField](#stringfield)): The unique identifier assigned to the document.

```py
print(result.document.inference.prediction.document_number.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): The type of personal identification document.

```py
print(result.document.inference.prediction.document_type.value)
```

## Expiration Date
**expiry_date** ([DateField](#datefield)): The date when the document becomes invalid.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## Given Names
**given_names** (List[[StringField](#stringfield)]): The list of the document holder's given names.

```py
for given_names_elem in result.document.inference.prediction.given_names:
    print(given_names_elem.value)
```

## Issue Date
**issue_date** ([DateField](#datefield)): The date when the document was issued.

```py
print(result.document.inference.prediction.issue_date.value)
```

## MRZ Line 1
**mrz_line1** ([StringField](#stringfield)): The Machine Readable Zone, first line.

```py
print(result.document.inference.prediction.mrz_line1.value)
```

## MRZ Line 2
**mrz_line2** ([StringField](#stringfield)): The Machine Readable Zone, second line.

```py
print(result.document.inference.prediction.mrz_line2.value)
```

## MRZ Line 3
**mrz_line3** ([StringField](#stringfield)): The Machine Readable Zone, third line.

```py
print(result.document.inference.prediction.mrz_line3.value)
```

## Nationality
**nationality** ([StringField](#stringfield)): The country of citizenship of the document holder.

```py
print(result.document.inference.prediction.nationality.value)
```

## Personal Number
**personal_number** ([StringField](#stringfield)): The unique identifier assigned to the document holder.

```py
print(result.document.inference.prediction.personal_number.value)
```

## Sex
**sex** ([StringField](#stringfield)): The biological sex of the document holder.

```py
print(result.document.inference.prediction.sex.value)
```

## State of Issue
**state_of_issue** ([StringField](#stringfield)): The state or territory where the document was issued.

```py
print(result.document.inference.prediction.state_of_issue.value)
```

## Surnames
**surnames** (List[[StringField](#stringfield)]): The list of the document holder's family names.

```py
for surnames_elem in result.document.inference.prediction.surnames:
    print(surnames_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
