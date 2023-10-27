---
title: Financial Document OCR Python
---
The Python OCR SDK supports the [Financial Document API](https://platform.mindee.com/mindee/financial_document).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/financial_document/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Financial Document sample](https://github.com/mindee/client-lib-test-data/blob/main/products/financial_document/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.FinancialDocumentV1, input_doc)

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
:Mindee ID: 81c1d637-3a84-41d9-b40a-f72ca2a58826
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/financial_document v1.1
:Rotation applied: Yes

Prediction
==========
:Locale: en; en; USD;
:Invoice Number:
:Reference Numbers:
:Purchase Date: 2014-07-07
:Due Date: 2014-07-07
:Total Net: 40.48
:Total Amount: 53.82
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  |               | TAX    |          | 3.34          |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: LOGANS
:Supplier Company Registrations:
:Supplier Address: 2513 s stemmons freeway lewisville tx 75067
:Supplier Phone Number: 9724596042
:Customer Name:
:Customer Company Registrations:
:Customer Address:
:Document Type: EXPENSE RECEIPT
:Purchase Subcategory: restaurant
:Purchase Category: food
:Total Tax: 3.34
:Tip and Gratuity: 10.00
:Purchase Time: 20:20
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+------------+
  | Description                          | Product Code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit Price |
  +======================================+==============+==========+============+==============+==============+============+
  | TAX                                  |              |          |            |              | 3.34         |            |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+------------+

Page Predictions
================

Page 0
------
:Locale: en; en; USD;
:Invoice Number:
:Reference Numbers:
:Purchase Date: 2014-07-07
:Due Date: 2014-07-07
:Total Net: 40.48
:Total Amount: 53.82
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  |               | TAX    |          | 3.34          |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: LOGANS
:Supplier Company Registrations:
:Supplier Address: 2513 s stemmons freeway lewisville tx 75067
:Supplier Phone Number: 9724596042
:Customer Name:
:Customer Company Registrations:
:Customer Address:
:Document Type: EXPENSE RECEIPT
:Purchase Subcategory: restaurant
:Purchase Category: food
:Total Tax: 3.34
:Tip and Gratuity: 10.00
:Purchase Time: 20:20
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+------------+
  | Description                          | Product Code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit Price |
  +======================================+==============+==========+============+==============+==============+============+
  | TAX                                  |              |          |            |              | 3.34         |            |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+------------+
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
* **reconstructed** (`bool`): indicates whether or not an object was reconstructed (not extracted as the API gave it).

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

### PaymentDetailsField
Aside from the basic `BaseField` attributes, the payment details field `PaymentDetailsField` also implements the following:

* **account_number** (`str`): number of an account, expressed as a string. Can be `None`.
* **iban** (`str`): International Bank Account Number. Can be `None`.
* **routing_number** (`str`): routing number of an account. Can be `None`.
* **swift** (`str`): the account holder's bank's SWIFT Business Identifier Code (BIC). Can be `None`.

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
List of line item details.

A `FinancialDocumentV1LineItem` implements the following attributes:

* **description** (`str`): The item description.
* **product_code** (`str`): The product code referring to the item.
* **quantity** (`float`): The item quantity
* **tax_amount** (`float`): The item tax amount.
* **tax_rate** (`float`): The item tax rate in percentage.
* **total_amount** (`float`): The item total amount.
* **unit_price** (`float`): The item unit price.

# Attributes
The following fields are extracted for Financial Document V1:

## Purchase Category
**category** ([ClassificationField](#classificationfield)): The purchase category among predefined classes.

```py
print(result.document.inference.prediction.category.value)
```

## Customer Address
**customer_address** ([StringField](#stringfield)): The address of the customer.

```py
print(result.document.inference.prediction.customer_address.value)
```

## Customer Company Registrations
**customer_company_registrations** (List[[CompanyRegistrationField](#companyregistrationfield)]): List of company registrations associated to the customer.

```py
for customer_company_registrations_elem in result.document.inference.prediction.customer_company_registrations:
    print(customer_company_registrations_elem.value)
```

## Customer Name
**customer_name** ([StringField](#stringfield)): The name of the customer.

```py
print(result.document.inference.prediction.customer_name.value)
```

## Purchase Date
**date** ([DateField](#datefield)): The date the purchase was made.

```py
print(result.document.inference.prediction.date.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): One of: 'INVOICE', 'CREDIT NOTE', 'CREDIT CARD RECEIPT', 'EXPENSE RECEIPT'.

```py
print(result.document.inference.prediction.document_type.value)
```

## Due Date
**due_date** ([DateField](#datefield)): The date on which the payment is due.

```py
print(result.document.inference.prediction.due_date.value)
```

## Invoice Number
**invoice_number** ([StringField](#stringfield)): The invoice number or identifier.

```py
print(result.document.inference.prediction.invoice_number.value)
```

## Line Items
**line_items** (List[[FinancialDocumentV1LineItem](#line-items-field)]): List of line item details.

```py
for line_items_elem in result.document.inference.prediction.line_items:
    print(line_items_elem.value)
```

## Locale
**locale** ([LocaleField](#localefield)): The locale detected on the document.

```py
print(result.document.inference.prediction.locale.value)
```

## Reference Numbers
**reference_numbers** (List[[StringField](#stringfield)]): List of Reference numbers, including PO number.

```py
for reference_numbers_elem in result.document.inference.prediction.reference_numbers:
    print(reference_numbers_elem.value)
```

## Purchase Subcategory
**subcategory** ([ClassificationField](#classificationfield)): The purchase subcategory among predefined classes for transport and food.

```py
print(result.document.inference.prediction.subcategory.value)
```

## Supplier Address
**supplier_address** ([StringField](#stringfield)): The address of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_address.value)
```

## Supplier Company Registrations
**supplier_company_registrations** (List[[CompanyRegistrationField](#companyregistrationfield)]): List of company registrations associated to the supplier.

```py
for supplier_company_registrations_elem in result.document.inference.prediction.supplier_company_registrations:
    print(supplier_company_registrations_elem.value)
```

## Supplier Name
**supplier_name** ([StringField](#stringfield)): The name of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Supplier Payment Details
**supplier_payment_details** (List[[PaymentDetailsField](#paymentdetailsfield)]): List of payment details associated to the supplier.

```py
for supplier_payment_details_elem in result.document.inference.prediction.supplier_payment_details:
    print(supplier_payment_details_elem.value)
```

## Supplier Phone Number
**supplier_phone_number** ([StringField](#stringfield)): The phone number of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_phone_number.value)
```

## Taxes
**taxes** (List[[TaxField](#taxes)]): List of tax lines information.

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
**tip** ([AmountField](#amountfield)): The total amount of tip and gratuity

```py
print(result.document.inference.prediction.tip.value)
```

## Total Amount
**total_amount** ([AmountField](#amountfield)): The total amount paid: includes taxes, tips, fees, and other charges.

```py
print(result.document.inference.prediction.total_amount.value)
```

## Total Net
**total_net** ([AmountField](#amountfield)): The net amount paid: does not include taxes, fees, and discounts.

```py
print(result.document.inference.prediction.total_net.value)
```

## Total Tax
**total_tax** ([AmountField](#amountfield)): The total amount of taxes.

```py
print(result.document.inference.prediction.total_tax.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
