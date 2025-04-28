---
title: Business Card OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-business-card-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Business Card API](https://platform.mindee.com/mindee/business_card).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/business_card/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Business Card sample](https://github.com/mindee/client-lib-test-data/blob/main/products/business_card/default_sample.jpg?raw=true)

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
    product.BusinessCardV1,
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
:Mindee ID: 6f9a261f-7609-4687-9af0-46a45156566e
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/business_card v1.0
:Rotation applied: Yes

Prediction
==========
:Firstname: Andrew
:Lastname: Morin
:Job Title: Founder & CEO
:Company: RemoteGlobal
:Email: amorin@remoteglobalconsulting.com
:Phone Number: +14015555555
:Mobile Number: +13015555555
:Fax Number: +14015555556
:Address: 178 Main Avenue, Providence, RI 02111
:Website: www.remoteglobalconsulting.com
:Social Media: https://www.linkedin.com/in/johndoe
               https://twitter.com/johndoe
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

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

# Attributes
The following fields are extracted for Business Card V1:

## Address
**address** ([StringField](#stringfield)): The address of the person.

```py
print(result.document.inference.prediction.address.value)
```

## Company
**company** ([StringField](#stringfield)): The company the person works for.

```py
print(result.document.inference.prediction.company.value)
```

## Email
**email** ([StringField](#stringfield)): The email address of the person.

```py
print(result.document.inference.prediction.email.value)
```

## Fax Number
**fax_number** ([StringField](#stringfield)): The Fax number of the person.

```py
print(result.document.inference.prediction.fax_number.value)
```

## Firstname
**firstname** ([StringField](#stringfield)): The given name of the person.

```py
print(result.document.inference.prediction.firstname.value)
```

## Job Title
**job_title** ([StringField](#stringfield)): The job title of the person.

```py
print(result.document.inference.prediction.job_title.value)
```

## Lastname
**lastname** ([StringField](#stringfield)): The lastname of the person.

```py
print(result.document.inference.prediction.lastname.value)
```

## Mobile Number
**mobile_number** ([StringField](#stringfield)): The mobile number of the person.

```py
print(result.document.inference.prediction.mobile_number.value)
```

## Phone Number
**phone_number** ([StringField](#stringfield)): The phone number of the person.

```py
print(result.document.inference.prediction.phone_number.value)
```

## Social Media
**social_media** (List[[StringField](#stringfield)]): The social media profiles of the person or company.

```py
for social_media_elem in result.document.inference.prediction.social_media:
    print(social_media_elem.value)
```

## Website
**website** ([StringField](#stringfield)): The website of the person or company.

```py
print(result.document.inference.prediction.website.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
