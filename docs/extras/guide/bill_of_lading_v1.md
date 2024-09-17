---
title: Bill of Lading OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-bill-of-lading-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Bill of Lading API](https://platform.mindee.com/mindee/bill_of_lading).

The [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/bill_of_lading/default_sample.jpg) can be used for testing purposes.
![Bill of Lading sample](https://github.com/mindee/client-lib-test-data/blob/main/products/bill_of_lading/default_sample.jpg?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.BillOfLadingV1,
    input_doc,
)

# Print a brief summary of the parsed data
print(result.document)

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

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Carrier Field
The shipping company responsible for transporting the goods.

A `BillOfLadingV1Carrier` implements the following attributes:

* **name** (`str`): The name of the carrier.
* **professional_number** (`str`): The professional number of the carrier.
* **scac** (`str`): The Standard Carrier Alpha Code (SCAC) of the carrier.
Fields which are specific to this product; they are not used in any other product.

### Consignee Field
The party to whom the goods are being shipped.

A `BillOfLadingV1Consignee` implements the following attributes:

* **address** (`str`): The address of the consignee.
* **email** (`str`): The  email of the shipper.
* **name** (`str`): The name of the consignee.
* **phone** (`str`): The phone number of the consignee.
Fields which are specific to this product; they are not used in any other product.

### Items Field
The goods being shipped.

A `BillOfLadingV1CarrierItem` implements the following attributes:

* **description** (`str`): A description of the item.
* **gross_weight** (`float`): The gross weight of the item.
* **measurement** (`float`): The measurement of the item.
* **measurement_unit** (`str`): The unit of measurement for the measurement.
* **quantity** (`float`): The quantity of the item being shipped.
* **weight_unit** (`str`): The unit of measurement for weights.
Fields which are specific to this product; they are not used in any other product.

### Notify Party Field
The party to be notified of the arrival of the goods.

A `BillOfLadingV1NotifyParty` implements the following attributes:

* **address** (`str`): The address of the notify party.
* **email** (`str`): The  email of the shipper.
* **name** (`str`): The name of the notify party.
* **phone** (`str`): The phone number of the notify party.
Fields which are specific to this product; they are not used in any other product.

### Shipper Field
The party responsible for shipping the goods.

A `BillOfLadingV1Shipper` implements the following attributes:

* **address** (`str`): The address of the shipper.
* **email** (`str`): The  email of the shipper.
* **name** (`str`): The name of the shipper.
* **phone** (`str`): The phone number of the shipper.

# Attributes
The following fields are extracted for Bill of Lading V1:

## Bill of Lading Number
**bill_of_lading_number** ([StringField](#stringfield)): A unique identifier assigned to a Bill of Lading document.

```py
print(result.document.inference.prediction.bill_of_lading_number.value)
```

## Carrier
**carrier** ([BillOfLadingV1Carrier](#carrier-field)): The shipping company responsible for transporting the goods.

```py
print(result.document.inference.prediction.carrier.value)
```

## Items
**carrier_items** (List[[BillOfLadingV1CarrierItem](#items-field)]): The goods being shipped.

```py
for carrier_items_elem in result.document.inference.prediction.carrier_items:
    print(carrier_items_elem.value)
```

## Consignee
**consignee** ([BillOfLadingV1Consignee](#consignee-field)): The party to whom the goods are being shipped.

```py
print(result.document.inference.prediction.consignee.value)
```

## Date of issue
**date_of_issue** ([DateField](#datefield)): The date when the bill of lading is issued.

```py
print(result.document.inference.prediction.date_of_issue.value)
```

## Departure Date
**departure_date** ([DateField](#datefield)): The date when the vessel departs from the port of loading.

```py
print(result.document.inference.prediction.departure_date.value)
```

## Notify Party
**notify_party** ([BillOfLadingV1NotifyParty](#notify-party-field)): The party to be notified of the arrival of the goods.

```py
print(result.document.inference.prediction.notify_party.value)
```

## Place of Delivery
**place_of_delivery** ([StringField](#stringfield)): The place where the goods are to be delivered.

```py
print(result.document.inference.prediction.place_of_delivery.value)
```

## Port of Discharge
**port_of_discharge** ([StringField](#stringfield)): The port where the goods are unloaded from the vessel.

```py
print(result.document.inference.prediction.port_of_discharge.value)
```

## Port of Loading
**port_of_loading** ([StringField](#stringfield)): The port where the goods are loaded onto the vessel.

```py
print(result.document.inference.prediction.port_of_loading.value)
```

## Shipper
**shipper** ([BillOfLadingV1Shipper](#shipper-field)): The party responsible for shipping the goods.

```py
print(result.document.inference.prediction.shipper.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
