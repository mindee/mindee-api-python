---
title: Receipt OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-receipt-ocr
parentDoc: 609808f773b0b90051d839de
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

# Print a summary of the API result
print(result.document)

# Print the document-level summary
# print(result.document.inference.prediction)

```

You can also call this product asynchronously:

```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.ReceiptV5,
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
:Mindee ID: d96fb043-8fb8-4adc-820c-387aae83376d
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/expense_receipts v5.3
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
:Supplier Name: Clachan
:Supplier Company Registrations: Type: VAT NUMBER, Value: 232153895
                                 Type: VAT NUMBER, Value: 232153895
:Supplier Address: 34 Kingley Street W1B 50H
:Supplier Phone Number: 02074940834
:Receipt Number: 54/7500
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
:Supplier Name: Clachan
:Supplier Company Registrations: Type: VAT NUMBER, Value: 232153895
                                 Type: VAT NUMBER, Value: 232153895
:Supplier Address: 34 Kingley Street W1B 50H
:Supplier Phone Number: 02074940834
:Receipt Number: 54/7500
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


### AmountField
The amount field `AmountField` only has one constraint: its **value** is an `Optional[float]`.


### ClassificationField
The classification field `ClassificationField` does not implement all the basic `BaseField` attributes. It only implements **value**, **confidence** and **page_id**.

> Note: a classification field's `value is always a `str`.


### CompanyRegistrationField
Aside from the basic `BaseField` attributes, the company registration field `CompanyRegistrationField` also implements the following:

* **type** (`str`): the type of company.

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### LocaleField
The locale field `LocaleField` only implements the **value**, **confidence** and **page_id** base `BaseField` attributes, but it comes with its own:

* **language** (`str`): ISO 639-1 language code (e.g.: `en` for English). Can be `None`.
* **country** (`str`): ISO 3166-1 alpha-2 or ISO 3166-1 alpha-3 code for countries (e.g.: `GRB` or `GB` for "Great Britain"). Can be `None`.
* **currency** (`str`): ISO 4217 code for currencies (e.g.: `USD` for "US Dollars"). Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

### TaxesField
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
List of all line items on the receipt.

A `ReceiptV5LineItem` implements the following attributes:

* **description** (`str`): The item description.
* **quantity** (`float`): The item quantity.
* **total_amount** (`float`): The item total amount.
* **unit_price** (`float`): The item unit price.

# Attributes
The following fields are extracted for Receipt V5:

## Purchase Category
**category** ([ClassificationField](#classificationfield)): The purchase category of the receipt.

#### Possible values include:
 - 'toll'
 - 'food'
 - 'parking'
 - 'transport'
 - 'accommodation'
 - 'gasoline'
 - 'telecom'
 - 'miscellaneous'

```py
print(result.document.inference.prediction.category.value)
```

## Purchase Date
**date** ([DateField](#datefield)): The date the purchase was made.

```py
print(result.document.inference.prediction.date.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): The type of receipt: EXPENSE RECEIPT or CREDIT CARD RECEIPT.

#### Possible values include:
 - 'EXPENSE RECEIPT'
 - 'CREDIT CARD RECEIPT'

```py
print(result.document.inference.prediction.document_type.value)
```

## Line Items
**line_items** (List[[ReceiptV5LineItem](#line-items-field)]): List of all line items on the receipt.

```py
for line_items_elem in result.document.inference.prediction.line_items:
    print(line_items_elem)
```

## Expense Locale
**locale** ([LocaleField](#localefield)): The locale of the document.

```py
print(result.document.inference.prediction.locale.value)
```

## Receipt Number
**receipt_number** ([StringField](#stringfield)): The receipt number or identifier.

```py
print(result.document.inference.prediction.receipt_number.value)
```

## Purchase Subcategory
**subcategory** ([ClassificationField](#classificationfield)): The purchase subcategory of the receipt for transport and food.

#### Possible values include:
 - 'plane'
 - 'taxi'
 - 'train'
 - 'restaurant'
 - 'shopping'
 - None

```py
print(result.document.inference.prediction.subcategory.value)
```

## Supplier Address
**supplier_address** ([StringField](#stringfield)): The address of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_address.value)
```

## Supplier Company Registrations
**supplier_company_registrations** (List[[CompanyRegistrationField](#companyregistrationfield)]): List of company registration numbers associated to the supplier.

```py
for supplier_company_registrations_elem in result.document.inference.prediction.supplier_company_registrations:
    print(supplier_company_registrations_elem.value)
```

## Supplier Name
**supplier_name** ([StringField](#stringfield)): The name of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Supplier Phone Number
**supplier_phone_number** ([StringField](#stringfield)): The phone number of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_phone_number.value)
```

## Taxes
**taxes** (List[[TaxField](#taxes)]): The list of taxes present on the receipt.

```py
for taxes_elem in result.document.inference.prediction.taxes:
    print(taxes_elem.polygon)
```

## Purchase Time
**time** ([StringField](#stringfield)): The time the purchase was made.

```py
print(result.document.inference.prediction.time.value)
```

## Tip and Gratuity
**tip** ([AmountField](#amountfield)): The total amount of tip and gratuity.

```py
print(result.document.inference.prediction.tip.value)
```

## Total Amount
**total_amount** ([AmountField](#amountfield)): The total amount paid: includes taxes, discounts, fees, tips, and gratuity.

```py
print(result.document.inference.prediction.total_amount.value)
```

## Total Net
**total_net** ([AmountField](#amountfield)): The net amount paid: does not include taxes, fees, and discounts.

```py
print(result.document.inference.prediction.total_net.value)
```

## Total Tax
**total_tax** ([AmountField](#amountfield)): The sum of all taxes.

```py
print(result.document.inference.prediction.total_tax.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
