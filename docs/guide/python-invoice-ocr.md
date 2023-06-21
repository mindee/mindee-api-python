The Python  OCR SDK supports the [invoice API](https://developers.mindee.com/docs/invoice-ocr) for extracting data from invoices.

Using this sample below, we are going to illustrate how to extract the data that we want using the OCR SDK.

![sample invoice](https://raw.githubusercontent.com/mindee/client-lib-test-data/main/invoice/invoice_1p.jpg)

## Quick Start
```python
from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the Invoice by passing the appropriate type
result = input_doc.parse(documents.TypeInvoiceV4)

# Print a brief summary of the parsed data
print(result.document)
```

Output:
```
Invoice V4 Prediction
=====================
:Filename:
:Locale: fr; fr; EUR;
:Invoice number: 0042004801351
:Reference numbers: AD29094
:Invoice date: 2020-02-17
:Invoice due date: 2020-02-17
:Supplier name: TURNPIKE DESIGNS CO.
:Supplier address: 156 University Ave, Toronto ON, Canada M5H 2H7
:Supplier company registrations: 501124705; FR33501124705
:Supplier payment details: FR7640254025476501124705368;
:Customer name: JIRO DOI
:Customer company registrations: FR00000000000; 111222333
:Customer address: 1954 Bloon Street West Toronto, ON, M6P 3K9 Canada
:Line Items:
  Code           | QTY    | Price   | Amount   | Tax (Rate)       | Description
                 |        |         | 4.31     |  (2.10%)         | PQ20 ETIQ ULTRA RESIS METAXXDC
                 | 1.00   | 65.00   | 75.00    | 10.00            | Platinum web hosting package Dow...
  XXX81125600010 | 1.00   | 250.01  | 275.51   | 25.50 (10.20%)   | a long string describing the ite...
  ABC456         | 200.30 | 8.101   | 1622.63  | 121.70 (7.50%)   | Liquid perfection
                 |        |         |          |                  | CARTOUCHE L NR BROTHER TN247BK
:Taxes:
  +---------------+--------+----------+---------------+
  | Base          | Code   | Rate (%) | Amount        |
  +===============+========+==========+===============+
  |               |        | 20.00    | 97.98         |
  +---------------+--------+----------+---------------+
:Total tax: 97.98
:Total net: 489.97
:Total amount: 587.95
```

## Invoice Data Structure
The invoice object JSON data structure consists of:

- [Document level prediction](#document-level-prediction)
- [Page level prediction](#page-level-prediction)
- [Raw HTTP response](#raw-http-response)

### Document Level Prediction
For document level prediction, we construct the document class by using the different pages put in a single document.
The method used for creating a single invoice object with multiple pages relies on field confidence scores.

Basically, we iterate over each page, and for each field, we keep the one that has the highest probability.

For example, if you send a three-page invoice, the document level will provide you with one tax, one total, and so on.

```python
print(result.document)
```

### Page Level Prediction
For page level prediction, in a multi-page pdf we construct the document class by using a unique page of the pdf.

```python
# [InvoiceV4, InvoiceV4 ...]
result.pages
```

### Raw HTTP Response
This contains the full Mindee API HTTP response object in JSON format

```python
# full HTTP request object
result.http_response
```

## Extracted Fields
Each invoice object contains a set of different fields. Each field contains the four following attributes:

- **value** (Str or Float depending on the field type): corresponds to the field value. Set to None if the `>field` was not extracted.
- **confidence** (Float): the confidence score of the field prediction.
- **bounding_box** (Array[Float]): contains the relative vertices coordinates of the bounding box containing the `>field` in the image.
  If the field is not written, the bbox is an empty array.
- **reconstructed** (Bool): True if the field was reconstructed using other fields.

### Additional Attributes
Depending on the field type, there might be additional attributes that will be extracted.

- [Customer Information](#customer-information)
- [Dates](#dates)
- [Locale and Currency](#locale-and-currency)
- [Payment Information](#payment-information)
- [Reference Numbers](#reference-numbers)
- [Supplier Information](#supplier-information)
- [Taxes](#taxes)
- [Total Amounts](#total-amounts)
- [Line Items](#line-items)


### Customer Information

- **customer_name**: Customer name

```python
# To get the customer name (string)
customer_name = result.document.customer_name.value
```

- **customer_address**: Customer's address

```python
# To get the customer address (string)
customer_address = result.document.customer_address.value
```

- **customer_company_registrations**: Customer Company Registration

```python
# To get the customer company registation (string)
customer_company_registrations = result.document.customer_company_registrations

for customer_company_registration in customer_company_registrations:
    # To get the type of number
    customer_company_registration_number_type = customer_company_registration.type

    # To get the company number
    customer_company_registration_number_value = customer_company_registration.value
```   

### Dates
**date_object**: Contains the date of issuance of the invoice. Each date field comes with extra attributes:

- **invoice_date**: Datetime object from python datetime date library.

```python
# To get the invoice date of issuance (string)
invoice_date = result.document.invoice_date.value
```

- **due_date**: Payment due date of the invoice.

```python
# To get the invoice due date (string)
due_date = result.document.due_date.value
```

### Locale and Currency

- **locale**: Language ISO code.

```python
# To get the total language code
language = result.document.locale.value
```

- **currency** (String): ISO currency code.

``` python
# To get the invoice currency code
currency = result.document.locale.currency
```

### Payment Information
**payment_details**: List of invoice's supplier payment details. Each object in the list contains extra attributes:

- **iban**: (String)
- **swift**: (String)
- **routing_number**: (String)
- **account_number**: (String)

```python
# To get the list of payment details
payment_details = result.document.payment_details

# Loop on each object
for payment_detail in payment_details:
   # To get the IBAN
   iban = payment_detail.iban

   # To get the swift
   swift = payment_detail.swift

   # To get the routing number
   routing_number = payment_detail.routing_number

   # To get the account_number
   account_number = payment_detail.account_number
```

### Reference numbers
**reference_numbers**: List of Reference numbers including PO number:

- **iban**: (String)
- **swift**: (String)
- **routing_number**: (String)
- **account_number**: (String)

```python
# To get the list of payment details
reference_numbers = result.document.reference_numbers

# Loop on each object
for reference_number in reference_numbers:
   print(reference_number.value)
```

### Supplier Information

**supplier_company_registrations**:  List of detected supplier's company registration number. Each object in the list contains extra attribute:

- **type** (String Generic): Type of company registration number among predefined categories.
- **value** (String): Value of the company identifier

```python
# To get the list of company numbers
supplier_company_registrations = result.document.supplier_company_registrations

# Loop on each object
for company_registration in supplier_company_registrations:
   # To get the type of number
   company_registration_type = company_registration.type

   # To get the company number
   company_registration_value = company_registration.value
```

- **supplier**: Supplier name as written in the invoice (logo or supplier Infos).

```python
# To get the supplier name
supplier_name = result.document.supplier_name.value
```

- **supplier_address**: Supplier address as written in the invoice.

```python
# To get the supplier address
supplier_address = result.document.supplier_address.value
```

### Taxes
**taxes**: Contains array of tax fields. Each of the tax fields has two extra attributes:

- **code** (String): Optional tax code (HST, GST... for Canadian; City Tax, State tax for US, etc..).
- **rate** (Float): Optional tax rate.

```python
# To get the list of taxes
taxes = result.document.taxes

# Loop on each Tax field
for tax in taxes:
   # To get the tax amount
   tax_amount = tax.value

   # To get the tax code for from a tax object
   tax_code = tax.code

   # To get the tax rate
   tax_rate = tax.rate
```

### Total Amounts

- **total_amount**: Total amount including taxes.

```python
# To get the total amount including taxes value (float), ex: 14.24
total_amount = result.document.total_amount.value
```

- **total_net**: Total amount excluding taxes.

```python
# To get the total amount excluding taxes value (float), ex: 10.21
total_net = result.document.total_net.value
```

- **total_tax**: Total tax value from tax lines.

```python
# To get the total tax amount value (float), ex: 8.42
total_tax = result.document.total_tax.value
```

### Line Items
**line_items**: List containing the details of line items. Each object in the list contains extra attributes:

- **product_code**: (String)
- **description**: (String)
- **quantity**: (float)
- **total_amount**: (float)
- **tax_rate**: (float)
- **tax_amount**: (float)
- **unit_price**: (float)
- **confidence**: (float)


```python
# Loop on line items
for line_item in result.document.line_items:
   # Show just the description
   print(line_item.description)

   # Show a summary of the entire line, each field is divided by the `|` character
   print(line_item)
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
