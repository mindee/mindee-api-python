---
title: Invoice Splitter OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-invoice-splitter-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Invoice Splitter API](https://platform.mindee.com/mindee/invoice_splitter).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/invoice_splitter/default_sample.pdf), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Invoice Splitter sample](https://github.com/mindee/client-lib-test-data/blob/main/products/invoice_splitter/default_sample.pdf?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.InvoiceSplitterV1,
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
:Mindee ID: 15ad7a19-7b75-43d0-b0c6-9a641a12b49b
:Filename: default_sample.pdf

Inference
#########
:Product: mindee/invoice_splitter v1.2
:Rotation applied: No

Prediction
==========
:Invoice Page Groups:
  +--------------------------------------------------------------------------+
  | Page Indexes                                                             |
  +==========================================================================+
  | 0                                                                        |
  +--------------------------------------------------------------------------+
  | 1                                                                        |
  +--------------------------------------------------------------------------+
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

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Invoice Page Groups Field
List of page groups. Each group represents a single invoice within a multi-invoice document.

A `InvoiceSplitterV1InvoicePageGroup` implements the following attributes:

* **page_indexes** (`List[int]`): List of page indexes that belong to the same invoice (group).

# Attributes
The following fields are extracted for Invoice Splitter V1:

## Invoice Page Groups
**invoice_page_groups** (List[[InvoiceSplitterV1InvoicePageGroup](#invoice-page-groups-field)]): List of page groups. Each group represents a single invoice within a multi-invoice document.

```py
for invoice_page_groups_elem in result.document.inference.prediction.invoice_page_groups:
    print(invoice_page_groups_elem.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
