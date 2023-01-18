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

# Parse the document as an Invoice by passing the appropriate type
api_response = input_doc.parse(documents.TypeInvoiceV4)

print(api_response.document)
```

Output:
```
----- Invoice V4 -----
Filename: a74eaa5-c8e283b-sample_invoice.jpeg
Locale: en; en; CAD;
Invoice number: 14
Reference numbers: AD29094
Invoice date: 2018-09-25
Invoice due date: 2018-09-25
Supplier name: TURNPIKE DESIGNS CO.
Supplier address: 156 University Ave, Toronto ON, Canada M5H 2H7
Supplier company registrations:
Supplier payment details:
Customer name: JIRO DOI
Customer company registrations:
Customer address: 1954 Bloon Street West Toronto, ON, M6P 3K9 Canada
Line Items:
  Code           | QTY    | Price   | Amount   | Tax (Rate)       | Description
                 | 1.00   | 65.00   | 65.00    |                  | Platinum web hosting package Dow...
                 | 3.00   | 2100.00 | 2100.00  |                  | 2 page website design Includes b...
                 | 1.00   | 250.00  | 250.00   |                  | Mobile designs Includes responsi...
Taxes: 193.20 8.00%
Total taxes: 193.20
Total amount excluding taxes: 2415.00
Total amount including taxes: 2608.20
----------------------
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
print(api_response.document)
```

### Page Level Prediction
For page level prediction, in a multi-page pdf we construct the document class by using a unique page of the pdf.

```python
# [InvoiceV4, InvoiceV4 ...]
invoice_data.pages
```

### Raw HTTP Response
This contains the full Mindee API HTTP response object in JSON format

```python
# full HTTP request object
invoice_data.http_response
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
customer_name = invoice_data.document.customer_name.value
```

- **customer_address**: Customer's address

```python
# To get the customer address (string)
customer_address = invoice_data.document.customer_address.value
```

- **customer_company_registrations**: Customer Company Registration

```python
# To get the customer company registation (string)
customer_company_registrations = invoice_data.document.customer_company_registrations

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
invoice_date = invoice_data.document.invoice_date.value
```

- **due_date**: Payment due date of the invoice.

```python
# To get the invoice due date (string)
due_date = invoice_data.document.due_date.value
```

### Locale and Currency

- **locale**: Language ISO code.

```python
# To get the total language code
language = invoice_data.document.locale.value
```

- **currency** (String): ISO currency code.

``` python
# To get the invoice currency code
currency = invoice_data.document.locale.currency
```

### Payment Information
**payment_details**: List of invoice's supplier payment details. Each object in the list contains extra attributes:

- **iban**: (String)
- **swift**: (String)
- **routing_number**: (String)
- **account_number**: (String)

```python
# To get the list of payment details
payment_details = invoice_data.document.payment_details

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
reference_numbers = invoice_data.document.reference_numbers

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
supplier_company_registrations = invoice_data.document.supplier_company_registrations

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
supplier_name = invoice_data.document.supplier_name.value
```

- **supplier_address**: Supplier address as written in the invoice.

```python
# To get the supplier address
supplier_address = invoice_data.document.supplier_address.value
```

### Taxes
**taxes**: Contains array of tax fields. Each of the tax fields has two extra attributes:

- **code** (String): Optional tax code (HST, GST... for Canadian; City Tax, State tax for US, etc..).
- **rate** (Float): Optional tax rate.

```python
# To get the list of taxes
taxes = invoice_data.document.taxes

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
total_amount = invoice_data.document.total_amount.value
```

- **total_net**: Total amount excluding taxes.

```python
# To get the total amount excluding taxes value (float), ex: 10.21
total_net = invoice_data.document.total_net.value
```

- **total_tax**: Total tax value from tax lines.

```python
# To get the total tax amount value (float), ex: 8.42
total_tax = invoice_data.document.total_tax.value
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
for line_item in invoice_data.document.line_items:
   # Show just the description
   print(line_item.description)

   # Show a summary of the entire line, each field is divided by the `|` character
   print(line_item)
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
