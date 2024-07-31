---
title: Multi Receipts Detector OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-multi-receipts-detector-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Multi Receipts Detector API](https://platform.mindee.com/mindee/multi_receipts_detector).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/multi_receipts_detector/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Multi Receipts Detector sample](https://github.com/mindee/client-lib-test-data/blob/main/products/multi_receipts_detector/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.MultiReceiptsDetectorV1, input_doc)

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
:Product: mindee/multi_receipts_detector v1.0
:Rotation applied: Yes

Prediction
==========
:List of Receipts: Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.

Page Predictions
================

Page 0
------
:List of Receipts: Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
                   Polygon with 4 points.
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

# Attributes
The following fields are extracted for Multi Receipts Detector V1:

## List of Receipts
**receipts**(List[[PositionField](#positionfield)]): Positions of the receipts on the document.

```py
for receipts_elem in result.document.inference.prediction.receipts:
    print(receipts_elem.polygon)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
