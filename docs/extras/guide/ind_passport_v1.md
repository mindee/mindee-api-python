---
title: IND Passport - India OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-ind-passport---india-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Passport - India API](https://platform.mindee.com/mindee/ind_passport).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/ind_passport/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Passport - India sample](https://github.com/mindee/client-lib-test-data/blob/main/products/ind_passport/default_sample.jpg?raw=true)

# Quick-Start
```py
#
# Install the Python client library by running:
# pip install mindee
#

from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.ind.IndianPassportV1,
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
:Mindee ID: cf88fd43-eaa1-497a-ba29-a9569a4edaa7
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/ind_passport v1.2
:Rotation applied: Yes

Prediction
==========
:Page Number: 1
:Country: IND
:ID Number: J8369854
:Given Names: JOCELYN MICHELLE
:Surname: DOE
:Birth Date: 1959-09-23
:Birth Place: GUNDUGOLANU
:Issuance Place: HYDERABAD
:Gender: F
:Issuance Date: 2011-10-11
:Expiry Date: 2021-10-10
:MRZ Line 1: P<DOE<<JOCELYNMICHELLE<<<<<<<<<<<<<<<<<<<<<
:MRZ Line 2: J8369854<4IND5909234F2110101<<<<<<<<<<<<<<<8
:Legal Guardian:
:Name of Spouse:
:Name of Mother:
:Old Passport Date of Issue:
:Old Passport Number:
:Old Passport Place of Issue:
:Address Line 1:
:Address Line 2:
:Address Line 3:
:File Number:
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


### ClassificationField
The classification field `ClassificationField` does not implement all the basic `BaseField` attributes. It only implements **value**, **confidence** and **page_id**.

> Note: a classification field's `value is always a `str`.

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Passport - India V1:

## Address Line 1
**address1** ([StringField](#stringfield)): The first line of the address of the passport holder.

```py
print(result.document.inference.prediction.address1.value)
```

## Address Line 2
**address2** ([StringField](#stringfield)): The second line of the address of the passport holder.

```py
print(result.document.inference.prediction.address2.value)
```

## Address Line 3
**address3** ([StringField](#stringfield)): The third line of the address of the passport holder.

```py
print(result.document.inference.prediction.address3.value)
```

## Birth Date
**birth_date** ([DateField](#datefield)): The birth date of the passport holder, ISO format: YYYY-MM-DD.

```py
print(result.document.inference.prediction.birth_date.value)
```

## Birth Place
**birth_place** ([StringField](#stringfield)): The birth place of the passport holder.

```py
print(result.document.inference.prediction.birth_place.value)
```

## Country
**country** ([StringField](#stringfield)): ISO 3166-1 alpha-3 country code (3 letters format).

```py
print(result.document.inference.prediction.country.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): The date when the passport will expire, ISO format: YYYY-MM-DD.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## File Number
**file_number** ([StringField](#stringfield)): The file number of the passport document.

```py
print(result.document.inference.prediction.file_number.value)
```

## Gender
**gender** ([ClassificationField](#classificationfield)): The gender of the passport holder.

#### Possible values include:
 - 'M'
 - 'F'

```py
print(result.document.inference.prediction.gender.value)
```

## Given Names
**given_names** ([StringField](#stringfield)): The given names of the passport holder.

```py
print(result.document.inference.prediction.given_names.value)
```

## ID Number
**id_number** ([StringField](#stringfield)): The identification number of the passport document.

```py
print(result.document.inference.prediction.id_number.value)
```

## Issuance Date
**issuance_date** ([DateField](#datefield)): The date when the passport was issued, ISO format: YYYY-MM-DD.

```py
print(result.document.inference.prediction.issuance_date.value)
```

## Issuance Place
**issuance_place** ([StringField](#stringfield)): The place where the passport was issued.

```py
print(result.document.inference.prediction.issuance_place.value)
```

## Legal Guardian
**legal_guardian** ([StringField](#stringfield)): The name of the legal guardian of the passport holder (if applicable).

```py
print(result.document.inference.prediction.legal_guardian.value)
```

## MRZ Line 1
**mrz1** ([StringField](#stringfield)): The first line of the machine-readable zone (MRZ) of the passport document.

```py
print(result.document.inference.prediction.mrz1.value)
```

## MRZ Line 2
**mrz2** ([StringField](#stringfield)): The second line of the machine-readable zone (MRZ) of the passport document.

```py
print(result.document.inference.prediction.mrz2.value)
```

## Name of Mother
**name_of_mother** ([StringField](#stringfield)): The name of the mother of the passport holder.

```py
print(result.document.inference.prediction.name_of_mother.value)
```

## Name of Spouse
**name_of_spouse** ([StringField](#stringfield)): The name of the spouse of the passport holder (if applicable).

```py
print(result.document.inference.prediction.name_of_spouse.value)
```

## Old Passport Date of Issue
**old_passport_date_of_issue** ([DateField](#datefield)): The date of issue of the old passport (if applicable), ISO format: YYYY-MM-DD.

```py
print(result.document.inference.prediction.old_passport_date_of_issue.value)
```

## Old Passport Number
**old_passport_number** ([StringField](#stringfield)): The number of the old passport (if applicable).

```py
print(result.document.inference.prediction.old_passport_number.value)
```

## Old Passport Place of Issue
**old_passport_place_of_issue** ([StringField](#stringfield)): The place of issue of the old passport (if applicable).

```py
print(result.document.inference.prediction.old_passport_place_of_issue.value)
```

## Page Number
**page_number** ([ClassificationField](#classificationfield)): The page number of the passport document.

#### Possible values include:
 - '1'
 - '2'

```py
print(result.document.inference.prediction.page_number.value)
```

## Surname
**surname** ([StringField](#stringfield)): The surname of the passport holder.

```py
print(result.document.inference.prediction.surname.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
