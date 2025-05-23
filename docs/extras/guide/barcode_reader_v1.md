---
title: Barcode Reader OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-barcode-reader-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Barcode Reader API](https://platform.mindee.com/mindee/barcode_reader).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/barcode_reader/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Barcode Reader sample](https://github.com/mindee/client-lib-test-data/blob/main/products/barcode_reader/default_sample.jpg?raw=true)

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
    product.BarcodeReaderV1,
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
:Mindee ID: f9c48da1-a306-4805-8da8-f7231fda2d88
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/barcode_reader v1.0
:Rotation applied: Yes

Prediction
==========
:Barcodes 1D: Mindee
:Barcodes 2D: https://developers.mindee.com/docs/barcode-reader-ocr
              I love paperwork! - Said no one ever

Page Predictions
================

Page 0
------
:Barcodes 1D: Mindee
:Barcodes 2D: https://developers.mindee.com/docs/barcode-reader-ocr
              I love paperwork! - Said no one ever
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
The following fields are extracted for Barcode Reader V1:

## Barcodes 1D
**codes_1d** (List[[StringField](#stringfield)]): List of decoded 1D barcodes.

```py
for codes_1d_elem in result.document.inference.prediction.codes_1d:
    print(codes_1d_elem.value)
```

## Barcodes 2D
**codes_2d** (List[[StringField](#stringfield)]): List of decoded 2D barcodes.

```py
for codes_2d_elem in result.document.inference.prediction.codes_2d:
    print(codes_2d_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
