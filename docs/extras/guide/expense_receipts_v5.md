---
title: Receipt OCR Python
---
The Python OCR SDK supports the [Receipt API](https://platform.mindee.com/mindee/expense_receipts).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/expense_receipts/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Receipt sample](https://github.com/mindee/client-lib-test-data/blob/main/products/expense_receipts/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.ReceiptV5, input_doc)

# Print a brief summary of the parsed data
print(result.document)

# # Iterate over all the fields in the document
# for field_name, field_values in result.document.inference.prediction.fields.items():
#     print(field_name, "=", field_values)
```

**Output (RST):**
```rst
########
Document
########
:Mindee ID: ce41e37a-65d8-4de1-b34b-1c92ab04b1ae
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/expense_receipts v5.0
:Rotation applied: Yes

Prediction
==========
:Expense Locale: en-GB; en; GB; GBP;
:Purchase Category: food
:Purchase Subcategory: restaurant
:Document Type: EXPENSE RECEIPT
:Purchase Date: 2016-02-26
:Purchase Time: 15:20
:Total Amount: 10.20
:Total Net: 8.50
:Total Tax: 1.70
:Tip and Gratuity:
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  | 8.50          | VAT    | 20.00    | 1.70          |
  +---------------+--------+----------+---------------+
:Supplier Name: CLACHAN
:Supplier Company Registrations: 232153895
                                 232153895
:Supplier Address: 34 kingley street w1b 5qh
:Supplier Phone Number: 02074940834
:Line Items:
  +--------------------------------------+----------+--------------+------------+
  | Description                          | Quantity | Total Amount | Unit Price |
  +======================================+==========+==============+============+
  | Meantime Pale                        | 2.00     | 10.20        |            |
  +--------------------------------------+----------+--------------+------------+

Page Predictions
================

Page 0
------
:Expense Locale: en-GB; en; GB; GBP;
:Purchase Category: food
:Purchase Subcategory: restaurant
:Document Type: EXPENSE RECEIPT
:Purchase Date: 2016-02-26
:Purchase Time: 15:20
:Total Amount: 10.20
:Total Net: 8.50
:Total Tax: 1.70
:Tip and Gratuity:
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  | 8.50          | VAT    | 20.00    | 1.70          |
  +---------------+--------+----------+---------------+
:Supplier Name: CLACHAN
:Supplier Company Registrations: 232153895
                                 232153895
:Supplier Address: 34 kingley street w1b 5qh
:Supplier Phone Number: 02074940834
:Line Items:
  +--------------------------------------+----------+--------------+------------+
  | Description                          | Quantity | Total Amount | Unit Price |
  +======================================+==========+==============+============+
  | Meantime Pale                        | 2.00     | 10.20        |            |
  +--------------------------------------+----------+--------------+------------+
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


### Classification Field
The classification field `ClassificationField` does not implement all the basic `BaseField` attributes. It only implements **value**, **confidence** and **page_id**.

> Note: a classification field's `value is always a `str`.


### Company Registration Field
Aside from the basic `BaseField` attributes, the company registration field `CompanyRegistrationField` also implements the following:

* **type** (`str`): the type of company.

### Date Field
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### Locale Field
The locale field `LocaleField` only implements the **value**, **confidence** and **page_id** base `BaseField` attributes, but it comes with its own:

* **language** (`str`): ISO 639-1 language code (e.g.: `en` for English). Can be `None`.
* **country** (`str`): ISO 3166-1 alpha-2 or ISO 3166-1 alpha-3 code for countries (e.g.: `GRB` or `GB` for "Great Britain"). Can be `None`.
* **currency** (`str`): ISO 4217 code for currencies (e.g.: `USD` for "US Dollars"). Can be `None`.

### String Field
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

### Taxes Field
#### Tax
Aside from the basic `BaseField` attributes, the tax field `TaxField` also implements the following:

* **rate** (`float`): the tax rate applied to an item expressed as a percentage. Can be `None`.
* **code** (`str`): tax code (or equivalent, depending on the origin of the document). Can be `None`.
* **base** (`float`): base amount used for the tax. Can be `None`.

> Note: currently `TaxField` is not used on its own, and is accessed through a parent `Taxes` object, a list-like structure.

#### Taxes (Array)
The `Taxes` field represents a list-like collection of `TaxField` objects. As it is the representation of several objects, it has access to a custom `__str__` method that can render a `TaxField` object as a table line.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Line Items Field
List of line item details.

A `ReceiptV5LineItem` implements the following attributes:

* **description** (`str`): The item description.
* **quantity** (`float`): The item quantity.
* **total_amount** (`float`): The item total amount.
* **unit_price** (`float`): The item unit price.

# Attributes
The following fields are extracted for Receipt V5:

## Purchase Category
**category** : The purchase category among predefined classes.

```py
print(result.document.inference.prediction.category.value)
```

## Purchase Date
**date** : The date the purchase was made.

```py
print(result.document.inference.prediction.date.value)
```

## Document Type
**document_type** : One of: 'CREDIT CARD RECEIPT', 'EXPENSE RECEIPT'.

```py
print(result.document.inference.prediction.document_type.value)
```

## Line Items
**line_items** ([ReceiptV5LineItem]List[(#line-items-field)]): List of line item details.

```py
for line_items_elem in result.document.inference.prediction.line_items:
    print(line_items_elem.value)
```

## Expense Locale
**locale** : The locale detected on the document.

```py
print(result.document.inference.prediction.locale.value)
```

## Purchase Subcategory
**subcategory** : The purchase subcategory among predefined classes for transport and food.

```py
print(result.document.inference.prediction.subcategory.value)
```

## Supplier Address
**supplier_address** : The address of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_address.value)
```

## Supplier Company Registrations
**supplier_company_registrations** : List of company registrations associated to the supplier.

```py
for supplier_company_registrations_elem in result.document.inference.prediction.supplier_company_registrations:
    print(supplier_company_registrations_elem.value)
```

## Supplier Name
**supplier_name** : The name of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Supplier Phone Number
**supplier_phone_number** : The phone number of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_phone_number.value)
```

## Taxes
**taxes** : List of tax lines information.

```py
for taxes_elem in result.document.inference.prediction.taxes:
    print(taxes_elem.polygon)
```

## Purchase Time
**time** : The time the purchase was made.

```py
print(result.document.inference.prediction.time.value)
```

## Tip and Gratuity
**tip** : The total amount of tip and gratuity.

```py
print(result.document.inference.prediction.tip.value)
```

## Total Amount
**total_amount** : The total amount paid: includes taxes, discounts, fees, tips, and gratuity.

```py
print(result.document.inference.prediction.total_amount.value)
```

## Total Net
**total_net** : The net amount paid: does not include taxes, fees, and discounts.

```py
print(result.document.inference.prediction.total_net.value)
```

## Total Tax
**total_tax** : The total amount of taxes.

```py
print(result.document.inference.prediction.total_tax.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)