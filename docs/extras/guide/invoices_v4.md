---
title: Invoice OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-invoice-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Invoice API](https://platform.mindee.com/mindee/invoices).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/invoices/default_sample.jpg), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Invoice sample](https://github.com/mindee/client-lib-test-data/blob/main/products/invoices/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, PredictResponse, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and parse it.
# The endpoint name must be specified since it cannot be determined from the class.
result: PredictResponse = mindee_client.parse(product.InvoiceV4, input_doc)

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
    product.InvoiceV4,
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
:Mindee ID: 86b1833f-138b-4a01-8387-860204b0e631
:Filename: default_sample.jpg

Inference
#########
:Product: mindee/invoices v4.9
:Rotation applied: Yes

Prediction
==========
:Locale: en-CA; en; CA; CAD;
:Invoice Number: 14
:Purchase Order Number: AD29094
:Reference Numbers: AD29094
:Purchase Date: 2018-09-25
:Due Date:
:Payment Date:
:Total Net: 2145.00
:Total Amount: 2608.20
:Total Tax: 193.20
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  |               |        | 8.00     | 193.20        |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: TURNPIKE DESIGNS
:Supplier Company Registrations:
:Supplier Address: 156 University Ave, Toronto ON, Canada, M5H 2H7
:Supplier Phone Number: 4165551212
:Supplier Website:
:Supplier Email: j_coi@example.com
:Customer Name: JIRO DOI
:Customer Company Registrations:
:Customer Address: 1954 Bloor Street West Toronto, ON, M6P 3K9 Canada
:Customer ID:
:Shipping Address:
:Billing Address: 1954 Bloor Street West Toronto, ON, M6P 3K9 Canada
:Document Type: INVOICE
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Description                          | Product code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit of measure | Unit Price |
  +======================================+==============+==========+============+==============+==============+=================+============+
  | Platinum web hosting package Down... |              | 1.00     |            |              | 65.00        |                 | 65.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | 2 page website design Includes ba... |              | 3.00     |            |              | 2100.00      |                 | 2100.00    |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Mobile designs Includes responsiv... |              | 1.00     |            |              | 250.00       | 1               | 250.00     |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+

Page Predictions
================

Page 0
------
:Locale: en-CA; en; CA; CAD;
:Invoice Number: 14
:Purchase Order Number: AD29094
:Reference Numbers: AD29094
:Purchase Date: 2018-09-25
:Due Date:
:Payment Date:
:Total Net: 2145.00
:Total Amount: 2608.20
:Total Tax: 193.20
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  |               |        | 8.00     | 193.20        |
  +---------------+--------+----------+---------------+
:Supplier Payment Details:
:Supplier Name: TURNPIKE DESIGNS
:Supplier Company Registrations:
:Supplier Address: 156 University Ave, Toronto ON, Canada, M5H 2H7
:Supplier Phone Number: 4165551212
:Supplier Website:
:Supplier Email: j_coi@example.com
:Customer Name: JIRO DOI
:Customer Company Registrations:
:Customer Address: 1954 Bloor Street West Toronto, ON, M6P 3K9 Canada
:Customer ID:
:Shipping Address:
:Billing Address: 1954 Bloor Street West Toronto, ON, M6P 3K9 Canada
:Document Type: INVOICE
:Line Items:
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Description                          | Product code | Quantity | Tax Amount | Tax Rate (%) | Total Amount | Unit of measure | Unit Price |
  +======================================+==============+==========+============+==============+==============+=================+============+
  | Platinum web hosting package Down... |              | 1.00     |            |              | 65.00        |                 | 65.00      |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | 2 page website design Includes ba... |              | 3.00     |            |              | 2100.00      |                 | 2100.00    |
  +--------------------------------------+--------------+----------+------------+--------------+--------------+-----------------+------------+
  | Mobile designs Includes responsiv... |              | 1.00     |            |              | 250.00       | 1               | 250.00     |
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
List of all the line items present on the invoice.

A `InvoiceV4LineItem` implements the following attributes:

* **description** (`str`): The item description.
* **product_code** (`str`): The product code of the item.
* **quantity** (`float`): The item quantity
* **tax_amount** (`float`): The item tax amount.
* **tax_rate** (`float`): The item tax rate in percentage.
* **total_amount** (`float`): The item total amount.
* **unit_measure** (`str`): The item unit of measure.
* **unit_price** (`float`): The item unit price.

# Attributes
The following fields are extracted for Invoice V4:

## Billing Address
**billing_address** ([StringField](#stringfield)): The customer billing address.

```py
print(result.document.inference.prediction.billing_address.value)
```

## Customer Address
**customer_address** ([StringField](#stringfield)): The address of the customer.

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
**customer_name** ([StringField](#stringfield)): The name of the customer or client.

```py
print(result.document.inference.prediction.customer_name.value)
```

## Purchase Date
**date** ([DateField](#datefield)): The date the purchase was made.

```py
print(result.document.inference.prediction.date.value)
```

## Document Type
**document_type** ([ClassificationField](#classificationfield)): Document type: INVOICE or CREDIT NOTE.

#### Possible values include:
 - 'INVOICE'
 - 'CREDIT NOTE'

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
**line_items** (List[[InvoiceV4LineItem](#line-items-field)]): List of all the line items present on the invoice.

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
**payment_date** ([DateField](#datefield)): The date on which the payment is due / was full-filled.

```py
print(result.document.inference.prediction.payment_date.value)
```

## Purchase Order Number
**po_number** ([StringField](#stringfield)): The purchase order number.

```py
print(result.document.inference.prediction.po_number.value)
```

## Reference Numbers
**reference_numbers** (List[[StringField](#stringfield)]): List of all reference numbers on the invoice, including the purchase order number.

```py
for reference_numbers_elem in result.document.inference.prediction.reference_numbers:
    print(reference_numbers_elem.value)
```

## Shipping Address
**shipping_address** ([StringField](#stringfield)): Customer's delivery address.

```py
print(result.document.inference.prediction.shipping_address.value)
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

## Supplier Email
**supplier_email** ([StringField](#stringfield)): The email address of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_email.value)
```

## Supplier Name
**supplier_name** ([StringField](#stringfield)): The name of the supplier or merchant.

```py
print(result.document.inference.prediction.supplier_name.value)
```

## Supplier Payment Details
**supplier_payment_details** (List[[PaymentDetailsField](#paymentdetailsfield)]): List of payment details associated to the supplier of the invoice.

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
**taxes** (List[[TaxField](#taxes)]): List of taxes. Each item contains the detail of the tax.

```py
for taxes_elem in result.document.inference.prediction.taxes:
    print(taxes_elem.polygon)
```

## Total Amount
**total_amount** ([AmountField](#amountfield)): The total amount of the invoice: includes taxes, tips, fees, and other charges.

```py
print(result.document.inference.prediction.total_amount.value)
```

## Total Net
**total_net** ([AmountField](#amountfield)): The net amount of the invoice: does not include taxes, fees, and discounts.

```py
print(result.document.inference.prediction.total_net.value)
```

## Total Tax
**total_tax** ([AmountField](#amountfield)): The total tax: the sum of all the taxes for this invoice.

```py
print(result.document.inference.prediction.total_tax.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
