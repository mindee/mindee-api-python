---
title: Financial Document OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-financial-document-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Financial Document API](https://platform.mindee.com/mindee/financial_document).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/financial_document/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Financial Document sample](https://github.com/mindee/client-lib-test-data/blob/main/products/financial_document/default_sample.jpg?raw=true)

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
    product.FinancialDocumentV1,
    input_doc,
)

# Print a summary of the API result
print(result.document)

# Print the document-level summary
# print(result.document.inference.prediction)

```

You can also call this product asynchronously:

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
    product.FinancialDocumentV1,
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
:Mindee ID: 6dd26385-719b-4527-bf6f-87d9da619de5
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/financial_document v1.14
:Rotation applied: Yes

Prediction
==========
:Locale: en-US; en; US; USD;
:Invoice Number: INT-001
:Purchase Order Number: 2412/2019
:Receipt Number:
:Document Number: INT-001
:Reference Numbers: 2412/2019
:Purchase Date: 2019-11-02
:Due Date: 2019-11-17
:Payment Date: 2019-11-17
:Total Net: 195.00
:Total Amount: 204.75
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  | 195.00        |        | 5.00     | 9.75          |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: JOHN SMITH
:Supplier Company Registrations:
:Supplier Address: 4490 Oak Drive Albany, NY 12210
:Supplier Phone Number:
:Customer Name: JESSIE M HORNE
:Supplier Website:
:Supplier Email:
:Customer Company Registrations:
:Customer Address: 2019 Redbud Drive New York, NY 10011
:Customer ID: 1234567890
:Shipping Address: 2019 Redbud Drive New York, NY 10011
:Billing Address: 4312 Wood Road New York, NY 10031
:Document Type: INVOICE
:Document Type Extended: INVOICE
:Purchase Subcategory:
:Purchase Category: miscellaneous
:Total Tax: 9.75
:Tip and Gratuity:
:Purchase Time:
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Description                          | Product code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit of measure | Unit Price |
  +======================================+==============+==========+============+==============+==============+=================+============+
  | Front and rear brake cables          |              | 1.00     |            |              | 100.00       |                 | 100.00     |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | New set of pedal arms                |              | 2.00     |            |              | 50.00        |                 | 25.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Labor 3hrs                           |              | 3.00     |            |              | 45.00        |                 | 15.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+

Page Predictions
================

Page 0
------
:Locale: en-US; en; US; USD;
:Invoice Number: INT-001
:Purchase Order Number: 2412/2019
:Receipt Number:
:Document Number: INT-001
:Reference Numbers: 2412/2019
:Purchase Date: 2019-11-02
:Due Date: 2019-11-17
:Payment Date: 2019-11-17
:Total Net: 195.00
:Total Amount: 204.75
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  | 195.00        |        | 5.00     | 9.75          |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: JOHN SMITH
:Supplier Company Registrations:
:Supplier Address: 4490 Oak Drive Albany, NY 12210
:Supplier Phone Number:
:Customer Name: JESSIE M HORNE
:Supplier Website:
:Supplier Email:
:Customer Company Registrations:
:Customer Address: 2019 Redbud Drive New York, NY 10011
:Customer ID: 1234567890
:Shipping Address: 2019 Redbud Drive New York, NY 10011
:Billing Address: 4312 Wood Road New York, NY 10031
:Document Type: INVOICE
:Document Type Extended: INVOICE
:Purchase Subcategory:
:Purchase Category: miscellaneous
:Total Tax: 9.75
:Tip and Gratuity:
:Purchase Time:
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Description                          | Product code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit of measure | Unit Price |
  +======================================+==============+==========+============+==============+==============+=================+============+
  | Front and rear brake cables          |              | 1.00     |            |              | 100.00       |                 | 100.00     |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | New set of pedal arms                |              | 2.00     |            |              | 50.00        |                 | 25.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Labor 3hrs                           |              | 3.00     |            |              | 45.00        |                 | 15.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
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


### AddressField
Aside from the basic `BaseField` attributes, the address field `AddressField` also implements the following:

* **street_number** (`str`): String representation of the street number. Can be `None`.
* **street_name** (`str`): Name of the street. Can be `None`.
* **po_box** (`str`): String representation of the PO Box number. Can be `None`.
* **address_complement** (`str`): Address complement. Can be `None`.
* **city** (`str`): City name. Can be `None`.
* **postal_code** (`str`): String representation of the postal code. Can be `None`.
* **state** (`str`): State name. Can be `None`.
* **country** (`str`): Country name. Can be `None`.

Note: The `value` field of an AddressField should be a concatenation of the rest of the values.


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
* **basis** (`float`): base amount used for the tax. Can be `None`.
* **value** (`float`): the value of the tax. Can be `None`.

> Note: currently `TaxField` is not used on its own, and is accessed through a parent `Taxes` object, a list-like structure.

#### Taxes (Array)
The `Taxes` field represents a list-like collection of `TaxField` objects. As it is the representation of several objects, it has access to a custom `__str__` method that can render a `TaxField` object as a table line.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Line Items Field
List of line item present on the document.

A `FinancialDocumentV1LineItem` implements the following attributes:

* **description** (`str`): The item description.
* **product_code** (`str`): The product code referring to the item.
* **quantity** (`float`): The item quantity
* **tax_amount** (`float`): The item tax amount.
* **tax_rate** (`float`): The item tax rate in percentage.
* **total_amount** (`float`): The item total amount.
* **unit_measure** (`str`): The item unit of measure.
* **unit_price** (`float`): The item unit price.

# Attributes
The following fields are extracted for Financial Document V1:

## Billing Address
**billing_address** ([AddressField](#addressfield)): The customer's address used for billing.

```py
print(result.document.inference.prediction.billing_address.value)
```

## Purchase Category
**category** ([ClassificationField](#classificationfield)): The purchase category.

#### Possible values include:
 - 'toll'
 - 'food'
 - 'parking'
 - 'transport'
 - 'accommodation'
 - 'gasoline'
 - 'telecom'
 - 'miscellaneous'
 - 'software'
 - 'shopping'
 - 'energy'

```py
print(result.document.inference.prediction.category.value)
```

## Customer Address
**customer_address** ([AddressField](#addressfield)): The address of the customer.

```py
print(result.document.inference.prediction.customer_address.value)
```

## Customer Company Registrations
**customer_company_registrations** (List[[CompanyRegistrationField](#companyregistrationfield)]): List of company registration numbers associated to the customer.

```py
for customer_company_registrations_elem in result.document.inference.prediction.customer_company_registrations:
    print(customer_company_registrations_elem.value)
```

## Customer ID
**customer_id** ([StringField](#stringfield)): The customer account number or identifier from the supplier.

```py
print(result.document.inference.prediction.customer_id.value)
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

## Document Number
**document_number** ([StringField](#stringfield)): The document number or identifier (invoice number or receipt number).

```py
print(result.document.inference.prediction.document_number.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): The type of the document: INVOICE or CREDIT NOTE if it is an invoice, CREDIT CARD RECEIPT or EXPENSE RECEIPT if it is a receipt.

#### Possible values include:
 - 'INVOICE'
 - 'CREDIT NOTE'
 - 'CREDIT CARD RECEIPT'
 - 'EXPENSE RECEIPT'

```py
print(result.document.inference.prediction.document_type.value)
```

## Document Type Extended
**document_type_extended** ([ClassificationField](#classificationfield)): Document type extended.

#### Possible values include:
 - 'CREDIT NOTE'
 - 'INVOICE'
 - 'OTHER'
 - 'OTHER_FINANCIAL'
 - 'PAYSLIP'
 - 'PURCHASE ORDER'
 - 'QUOTE'
 - 'RECEIPT'
 - 'STATEMENT'

```py
print(result.document.inference.prediction.document_type_extended.value)
```

## Due Date
**due_date** ([DateField](#datefield)): The date on which the payment is due.

```py
print(result.document.inference.prediction.due_date.value)
```

## Invoice Number
**invoice_number** ([StringField](#stringfield)): The invoice number or identifier only if document is an invoice.

```py
print(result.document.inference.prediction.invoice_number.value)
```

## Line Items
**line_items** (List[[FinancialDocumentV1LineItem](#line-items-field)]): List of line item present on the document.

```py
for line_items_elem in result.document.inference.prediction.line_items:
    print(line_items_elem)
```

## Locale
**locale** ([LocaleField](#localefield)): The locale of the document.

```py
print(result.document.inference.prediction.locale.value)
```

## Payment Date
**payment_date** ([DateField](#datefield)): The date on which the payment is due / fullfilled.

```py
print(result.document.inference.prediction.payment_date.value)
```

## Purchase Order Number
**po_number** ([StringField](#stringfield)): The purchase order number, only if the document is an invoice.

```py
print(result.document.inference.prediction.po_number.value)
```

## Receipt Number
**receipt_number** ([StringField](#stringfield)): The receipt number or identifier only if document is a receipt.

```py
print(result.document.inference.prediction.receipt_number.value)
```

## Reference Numbers
**reference_numbers** (List[[StringField](#stringfield)]): List of Reference numbers, including PO number, only if the document is an invoice.

```py
for reference_numbers_elem in result.document.inference.prediction.reference_numbers:
    print(reference_numbers_elem.value)
```

## Shipping Address
**shipping_address** ([AddressField](#addressfield)): The customer's address used for shipping.

```py
print(result.document.inference.prediction.shipping_address.value)
```

## Purchase Subcategory
**subcategory** ([ClassificationField](#classificationfield)): The purchase subcategory for transport, food and shooping.

#### Possible values include:
 - 'plane'
 - 'taxi'
 - 'train'
 - 'restaurant'
 - 'shopping'
 - 'other'
 - 'groceries'
 - 'cultural'
 - 'electronics'
 - 'office_supplies'
 - 'micromobility'
 - 'car_rental'
 - 'public'
 - 'delivery'
 - None

```py
print(result.document.inference.prediction.subcategory.value)
```

## Supplier Address
**supplier_address** ([AddressField](#addressfield)): The address of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_address.value)
```

## Supplier Company Registrations
**supplier_company_registrations** (List[[CompanyRegistrationField](#companyregistrationfield)]): List of company registration numbers associated to the supplier.

```py
for supplier_company_registrations_elem in result.document.inference.prediction.supplier_company_registrations:
    print(supplier_company_registrations_elem.value)
```

## Supplier Email
**supplier_email** ([StringField](#stringfield)): The email of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_email.value)
```

## Supplier Name
**supplier_name** ([StringField](#stringfield)): The name of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Supplier Payment Details
**supplier_payment_details** (List[[PaymentDetailsField](#paymentdetailsfield)]): List of payment details associated to the supplier (only for invoices).

```py
for supplier_payment_details_elem in result.document.inference.prediction.supplier_payment_details:
    print(supplier_payment_details_elem.value)
```

## Supplier Phone Number
**supplier_phone_number** ([StringField](#stringfield)): The phone number of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_phone_number.value)
```

## Supplier Website
**supplier_website** ([StringField](#stringfield)): The website URL of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_website.value)
```

## Taxes
**taxes** (List[[TaxField](#taxes)]): List of all taxes on the document.

```py
for taxes_elem in result.document.inference.prediction.taxes:
    print(taxes_elem.polygon)
```

## Purchase Time
**time** ([StringField](#stringfield)): The time the purchase was made (only for receipts).

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
**total_tax** ([AmountField](#amountfield)): The sum of all taxes present on the document.

```py
print(result.document.inference.prediction.total_tax.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
