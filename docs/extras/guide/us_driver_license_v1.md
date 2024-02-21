---
title: US Driver License OCR Python
---
The Python OCR SDK supports the [Driver License API](https://platform.mindee.com/mindee/us_driver_license).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/us_driver_license/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Driver License sample](https://github.com/mindee/client-lib-test-data/blob/main/products/us_driver_license/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.us.DriverLicenseV1, input_doc)

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
:Mindee ID: bf70068d-d3d6-49dc-b93a-b4b7d156fc3d
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/us_driver_license v1.0
:Rotation applied: Yes

Prediction
==========
:State: AZ
:Driver License ID: D12345678
:Expiry Date: 2018-02-01
:Date Of Issue: 2013-01-10
:Last Name: SAMPLE
:First Name: JELANI
:Address: 123 MAIN STREET PHOENIX AZ 85007
:Date Of Birth: 1957-02-01
:Restrictions: NONE
:Endorsements: NONE
:Driver License Class: D
:Sex: M
:Height: 5-08
:Weight: 185
:Hair Color: BRO
:Eye Color: BRO
:Document Discriminator: 1234567890123456

Page Predictions
================

Page 0
------
:Photo: Polygon with 4 points.
:Signature: Polygon with 4 points.
:State: AZ
:Driver License ID: D12345678
:Expiry Date: 2018-02-01
:Date Of Issue: 2013-01-10
:Last Name: SAMPLE
:First Name: JELANI
:Address: 123 MAIN STREET PHOENIX AZ 85007
:Date Of Birth: 1957-02-01
:Restrictions: NONE
:Endorsements: NONE
:Driver License Class: D
:Sex: M
:Height: 5-08
:Weight: 185
:Hair Color: BRO
:Eye Color: BRO
:Document Discriminator: 1234567890123456
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
The following fields are extracted for Driver License V1:

## Address
**address** ([StringField](#stringfield)): US driver license holders address

```py
print(result.document.inference.prediction.address.value)
```

## Date Of Birth
**date_of_birth** ([DateField](#datefield)): US driver license holders date of birth

```py
print(result.document.inference.prediction.date_of_birth.value)
```

## Document Discriminator
**dd_number** ([StringField](#stringfield)): Document Discriminator Number of the US Driver License

```py
print(result.document.inference.prediction.dd_number.value)
```

## Driver License Class
**dl_class** ([StringField](#stringfield)): US driver license holders class

```py
print(result.document.inference.prediction.dl_class.value)
```

## Driver License ID
**driver_license_id** ([StringField](#stringfield)): ID number of the US Driver License.

```py
print(result.document.inference.prediction.driver_license_id.value)
```

## Endorsements
**endorsements** ([StringField](#stringfield)): US driver license holders endorsements

```py
print(result.document.inference.prediction.endorsements.value)
```

## Expiry Date
**expiry_date** ([DateField](#datefield)): Date on which the documents expires.

```py
print(result.document.inference.prediction.expiry_date.value)
```

## Eye Color
**eye_color** ([StringField](#stringfield)): US driver license holders eye colour

```py
print(result.document.inference.prediction.eye_color.value)
```

## First Name
**first_name** ([StringField](#stringfield)): US driver license holders first name(s)

```py
print(result.document.inference.prediction.first_name.value)
```

## Hair Color
**hair_color** ([StringField](#stringfield)): US driver license holders hair colour

```py
print(result.document.inference.prediction.hair_color.value)
```

## Height
**height** ([StringField](#stringfield)): US driver license holders hight

```py
print(result.document.inference.prediction.height.value)
```

## Date Of Issue
**issued_date** ([DateField](#datefield)): Date on which the documents was issued.

```py
print(result.document.inference.prediction.issued_date.value)
```

## Last Name
**last_name** ([StringField](#stringfield)): US driver license holders last name

```py
print(result.document.inference.prediction.last_name.value)
```

## Photo
[📄](#page-level-fields "This field is only present on individual pages.")**photo** ([PositionField](#positionfield)): Has a photo of the US driver license holder

```py
for photo_elem in result.document.photo:
    print(photo_elem.polygon)
```

## Restrictions
**restrictions** ([StringField](#stringfield)): US driver license holders restrictions

```py
print(result.document.inference.prediction.restrictions.value)
```

## Sex
**sex** ([StringField](#stringfield)): US driver license holders gender

```py
print(result.document.inference.prediction.sex.value)
```

## Signature
[📄](#page-level-fields "This field is only present on individual pages.")**signature** ([PositionField](#positionfield)): Has a signature of the US driver license holder

```py
for signature_elem in result.document.signature:
    print(signature_elem.polygon)
```

## State
**state** ([StringField](#stringfield)): US State

```py
print(result.document.inference.prediction.state.value)
```

## Weight
**weight** ([StringField](#stringfield)): US driver license holders weight

```py
print(result.document.inference.prediction.weight.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
