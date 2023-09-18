The Python  OCR SDK supports the [receipt API](https://developers.mindee.com/docs/receipt-ocr) for extracting data from receipts.

Using this sample below, we are going to illustrate how to extract the data that we want using the OCR SDK.

![sample receipt](https://raw.githubusercontent.com/mindee/client-lib-test-data/main/receipt/receipt.jpg)

## Quick Start
```python
from mindee import Client, product

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the Receipt by passing the appropriate type
result = input_doc.parse(product.TypeReceiptV5)

# Print a brief summary of the parsed data
print(result.document)
```

Output:
```
Receipt V5 Prediction
=====================
:Filename:
:Expense Locale: en-GB; en; GB; GBP;
:Expense Category: food
:Expense Sub Category: restaurant
:Document Type: EXPENSE RECEIPT
:Purchase Date: 2016-02-26
:Purchase Time: 15:20
:Total Amount: 10.20
:Total Excluding Taxes: 8.50
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
:Supplier Address: 34 kingley street w1b 5qh
:Supplier Phone Number: 02074940834
:Line Items:
  +--------------------------------------+----------+--------------+------------+
  | Description                          | Quantity | Total Amount | Unit Price |
  +======================================+==========+==============+============+
  | meantime pale                        | 2.00     | 10.20        |            |
  +--------------------------------------+----------+--------------+------------+
```

## Receipt Data Structure
The receipt object JSON data structure consists of:

- [Document level prediction](#document-level-prediction)
- [Page level prediction](#page-level-prediction)
- [Raw HTTP response](#raw-http-response)

### Document Level Prediction
For document level prediction, we construct the document class by combining the different pages in a single document.
This method used for creating a single receipt object from multiple pages relies on **field confidence scores**.

Basically, we iterate over each page, and for each field, we keep the one that has the highest probability.

For example, if you send a three-page receipt, document level will provide you one tax, one total, and so on.

```python
# returns a unique object from class ReceiptV4
result.document
```

### Page Level Prediction
We create the document class by iterating over each page one by one. Each page in the PDF is treated as a unique page.

For example, if you send a three-page receipt, page level prediction will provide you with three tax, three total and so on.

```python
result.pages # [ReceiptV4, ReceiptV4 ...]
```
### Raw HTTP Response
Contains the full Mindee API HTTP response object in JSON format

```python
result.http_response # full HTTP request object
```

## Extracted Fields
Each receipt object contains a set of different fields. Each field contains the four following attributes:
- **value** (Str or Float depending on the field type): corresponds to the field value. Set to None if the `>field` was not extracted.
- **probability** (Float): the confidence score of the field prediction.
- **bounding_box** (Array[Float]): contains the relative vertices coordinates of the bounding box containing the `>field` in the image.
  If the field is not written, the bbox is an empty array.
- **reconstructed** (Bool): True if the field was reconstructed using other fields.


### Additional Attributes
Depending on the field type specified, additional attributes can be extracted in the receipt object.

Using the above [receipt example](https://files.readme.io/6882f91-receipt23.png), the following are the basic fields that can be extracted.
- [Document Type](#document-type)
- [Categories](#categories)
- [Date](#date)
- [Locale](#locale)
- [Orientation](#orientation)
- [Supplier Information](#supplier-information)
- [Taxes](#taxes)
- [Line Items](#line-items)
- [Time](#time)
- [Total Amounts](#total-amounts)
- [Tip](#tip)

### Document Type
- **document_type** (string): Whether the document is an expense receipt or a credit card receipt.

```python
document_type = result.document.document_type.value
print("document type: ", document_type)
```

### Categories
- **category** (string): Receipt category among predefined classes, as seen on the receipt.

```python
category = result.document.category.value
print("purchase category: ", category)
```

- **subcategory** (string): The receipt sub-category among predefined classes, as seen on the receipt.

```python
subcategory = result.document.subcategory.value
print("purchase subcategory: ", subcategory)
```

### Date
- **date** (string): Payment date as seen on the receipt.
    - **value** (string): [ISO 8601 date](https://en.wikipedia.org/wiki/ISO_8601) format (yyyy-mm-dd). European and imperial dates are both supported.
    - **raw** (string): In any format as seen on the receipt.

```python
receipt_date = result.document.date.value
print("Date on receipt: ", receipt_date)
```

### Locale
- **locale** (string): Concatenation of language and country codes.

```python
locale = result.document.locale.value
print("Locale code: ", locale)
```

- **locale.language** (string): Language code in [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1) format as seen on the receipt.

```python
language = result.document.locale.language
print("Language code: ", language)
```

- **locale.currency** (string): Currency code in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217) format as seen on the receipt.

```python
currency = result.receipt.locale.currency
print("Currency code: ", currency)
```

- **locale.country** (string): Country code in [ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1) alpha-2 format as seen on the receipt.

```python
country = result.document.locale.country
print("Country code: ", Country)
```

### Orientation
- **orientation** (number): The orientation field is only available at the page level as it describes whether the page image should be rotated to be upright.
  The rotation value is also conveniently available in the JSON response at: `document > inference > pages [ ] > orientation > value`.
  If the page requires rotation for correct display, the orientation field gives a prediction among these 3 possible outputs:
    - 0 degree: the page is already upright
    - 90 degrees: the page must be rotated clockwise to be upright
    - 270 degrees: the page must be rotated counterclockwise to be upright

```python
orientation = result.document.orientation
print("Degree: ", orientation)
```

### Supplier Information
- **supplier** (string): Supplier name as written in the receipt.

```python
supplier_name = result.document.supplier.value
print("Supplier Name: ", supplier_name)
```

### Taxes
- **taxes** (list): Contains tax fields as seen on the receipt.
    - **value** (float): The tax amount.
    - **code** (string): The tax code (HST, GST... for Canadian; City Tax, State tax for US, etc..).
    - **rate** (float): The tax rate.
    - **basis** (float): The amount used to calculate the tax.

```python
taxes = result.document.taxes

# Loop on each Tax field
for tax in taxes:
   print(f"  tax amount: {tax.value}, tax_code: {tax.code}, tax_rate: {tax.rate}")
```

### Line Items
- **line_items** (list): Full extraction of lines, including: description, quantity, unit price and total.
  - **description** (str): The item description.
  - **quantity** (float): The item quantity.
  - **total_amount** (float): The item total amount.
  - **unit_price** (float): The item unit price.

```python
line_items = result.document.line_items

# Loop on each line
for line_item in line_items:
    print(line_item.description)
    print(line_item.quantity)
    print(line_item.total_amount)
    print(line_item.unit_price)
```

### Time
- **time** (string): Time of purchase as seen on the receipt
    - **value** (string): Time of purchase with 24 hours formatting (hh:mm).
    - **raw** (string): In any format as seen on the receipt.

```python
time = result.document.time.value
print("Time: ", time)
```

### Total Amounts
- **total_amount** (number): Total amount including taxes

```python
total_amount = result.document.total_amount.value
print("total with tax", total_amount)
```

- **total_net** (number): Total amount paid excluding taxes

```python
total_net = result.document.total_net.value
print("total without tax", total_net)
```

- **total_tax** (number): Total tax value from tax lines

```python
total_tax = result.document.total_tax.value
print("total tax", total_tax)
```

### Tip
- **tip** (number): Total amount of tip and gratuity.

```python
tip = result.document.tip.value
print("Tip: ", supplier_name)
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
