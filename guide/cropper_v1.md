---
title: Cropper OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-cropper-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Cropper API](https://platform.mindee.com/mindee/cropper).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/cropper/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Cropper sample](https://github.com/mindee/client-lib-test-data/blob/main/products/cropper/default_sample.jpg?raw=true)

# Quick-Start
```py
#
# Install the Python client library by running:
# pip install mindee
#

from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
result: PredictResponse = mindee_client.parse(
    product.CropperV1,
    input_doc,
)

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
:Mindee ID: 149ce775-8302-4798-8649-7eda9fb84a1a
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/cropper v1.0
:Rotation applied: No

Prediction
==========

Page Predictions
================

Page 0
------
:Document Cropper: Polygon with 26 points.
                   Polygon with 25 points.
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

## Page-Level Fields
Some fields are constrained to the page level, and so will not be retrievable at document level.

# Attributes
The following fields are extracted for Cropper V1:

## Document Cropper
[📄](#page-level-fields "This field is only present on individual pages.")**cropping** (List[[PositionField](#positionfield)]): List of documents found in the image.

```py
for page in result.document.inference.pages:
    for cropping_elem in page.prediction.cropping):
        print(cropping_elem.polygon)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
