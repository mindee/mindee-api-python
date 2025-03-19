---
title: FR Energy Bill OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-fr-energy-bill-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [Energy Bill API](https://platform.mindee.com/mindee/energy_bill_fra).

Using the [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/energy_bill_fra/default_sample.pdf), we are going to illustrate how to extract the data that we want using the OCR SDK.
![Energy Bill sample](https://github.com/mindee/client-lib-test-data/blob/main/products/energy_bill_fra/default_sample.pdf?raw=true)

# Quick-Start
```py
from mindee import Client, product, AsyncPredictResponse

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.source_from_path("/path/to/the/file.ext")

# Load a file from disk and enqueue it.
result: AsyncPredictResponse = mindee_client.enqueue_and_parse(
    product.fr.EnergyBillV1,
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
:Mindee ID: 17f0ccef-e3fe-4a28-838d-d704489d6ce7
:Filename: default_sample.pdf

Inference
#########
:Product: mindee/energy_bill_fra v1.0
:Rotation applied: No

Prediction
==========
:Invoice Number: 10123590373
:Contract ID: 1234567890
:Delivery Point: 98765432109876
:Invoice Date: 2021-01-29
:Due Date: 2021-02-15
:Total Before Taxes: 1241.03
:Total Taxes: 238.82
:Total Amount: 1479.85
:Energy Supplier:
  :Address: TSA 12345, 12345 DEMOCITY CEDEX, 75001 PARIS
  :Name: EDF
:Energy Consumer:
  :Address: 12 AVENUE DES RÊVES, RDC A 123 COUR FAUSSE A, 75000 PARIS
  :Name: John Doe
:Subscription:
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Description                          | End Date   | Start Date | Tax Rate | Total     | Unit Price |
  +======================================+============+============+==========+===========+============+
  | Abonnement électricité               | 2021-02-28 | 2021-01-01 | 5.50     | 59.00     | 29.50      |
  +--------------------------------------+------------+------------+----------+-----------+------------+
:Energy Usage:
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Description                          | End Date   | Start Date | Tax Rate | Total     | Unit Price |
  +======================================+============+============+==========+===========+============+
  | Consommation (HT)                    | 2021-01-27 | 2020-11-28 | 20.00    | 898.43    | 10.47      |
  +--------------------------------------+------------+------------+----------+-----------+------------+
:Taxes and Contributions:
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Description                          | End Date   | Start Date | Tax Rate | Total     | Unit Price |
  +======================================+============+============+==========+===========+============+
  | Contribution au Service Public de... | 2021-01-27 | 2020-11-28 | 20.00    | 193.07    | 2.25       |
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Départementale sur la Conso Final... | 2020-12-31 | 2020-11-28 | 20.00    | 13.98     | 0.3315     |
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Communale sur la Conso Finale Ele... | 2021-01-27 | 2021-01-01 | 20.00    | 28.56     | 0.6545     |
  +--------------------------------------+------------+------------+----------+-----------+------------+
  | Contribution Tarifaire d'Achemine... | 2020-12-31 | 2020-11-28 | 20.00    | 27.96     | 0.663      |
  +--------------------------------------+------------+------------+----------+-----------+------------+
:Meter Details:
  :Meter Number: 620
  :Meter Type: electricity
  :Unit of Measure: kWh
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

### DateField
Aside from the basic `BaseField` attributes, the date field `DateField` also implements the following: 

* **date_object** (`Date`): an accessible representation of the value as a python object. Can be `None`.

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Energy Consumer Field
The entity that consumes the energy.

A `EnergyBillV1EnergyConsumer` implements the following attributes:

* **address** (`str`): The address of the energy consumer.
* **name** (`str`): The name of the energy consumer.
Fields which are specific to this product; they are not used in any other product.

### Energy Supplier Field
The company that supplies the energy.

A `EnergyBillV1EnergySupplier` implements the following attributes:

* **address** (`str`): The address of the energy supplier.
* **name** (`str`): The name of the energy supplier.
Fields which are specific to this product; they are not used in any other product.

### Energy Usage Field
Details of energy consumption.

A `EnergyBillV1EnergyUsage` implements the following attributes:

* **consumption** (`float`): The price per unit of energy consumed.
* **description** (`str`): Description or details of the energy usage.
* **end_date** (`str`): The end date of the energy usage.
* **start_date** (`str`): The start date of the energy usage.
* **tax_rate** (`float`): The rate of tax applied to the total cost.
* **total** (`float`): The total cost of energy consumed.
* **unit** (`str`): The unit of measurement for energy consumption.

#### Possible values include:
 - kWh
 - m3
 - L

* **unit_price** (`float`): The price per unit of energy consumed.
Fields which are specific to this product; they are not used in any other product.

### Meter Details Field
Information about the energy meter.

A `EnergyBillV1MeterDetail` implements the following attributes:

* **meter_number** (`str`): The unique identifier of the energy meter.
* **meter_type** (`str`): The type of energy meter.

#### Possible values include:
 - electricity
 - gas
 - water
 - None

* **unit** (`str`): The unit of power for energy consumption.
Fields which are specific to this product; they are not used in any other product.

### Subscription Field
The subscription details fee for the energy service.

A `EnergyBillV1Subscription` implements the following attributes:

* **description** (`str`): Description or details of the subscription.
* **end_date** (`str`): The end date of the subscription.
* **start_date** (`str`): The start date of the subscription.
* **tax_rate** (`float`): The rate of tax applied to the total cost.
* **total** (`float`): The total cost of subscription.
* **unit_price** (`float`): The price per unit of subscription.
Fields which are specific to this product; they are not used in any other product.

### Taxes and Contributions Field
Details of Taxes and Contributions.

A `EnergyBillV1TaxesAndContribution` implements the following attributes:

* **description** (`str`): Description or details of the Taxes and Contributions.
* **end_date** (`str`): The end date of the Taxes and Contributions.
* **start_date** (`str`): The start date of the Taxes and Contributions.
* **tax_rate** (`float`): The rate of tax applied to the total cost.
* **total** (`float`): The total cost of Taxes and Contributions.
* **unit_price** (`float`): The price per unit of Taxes and Contributions.

# Attributes
The following fields are extracted for Energy Bill V1:

## Contract ID
**contract_id** ([StringField](#stringfield)): The unique identifier associated with a specific contract.

```py
print(result.document.inference.prediction.contract_id.value)
```

## Delivery Point
**delivery_point** ([StringField](#stringfield)): The unique identifier assigned to each electricity or gas consumption point. It specifies the exact location where the energy is delivered.

```py
print(result.document.inference.prediction.delivery_point.value)
```

## Due Date
**due_date** ([DateField](#datefield)): The date by which the payment for the energy invoice is due.

```py
print(result.document.inference.prediction.due_date.value)
```

## Energy Consumer
**energy_consumer** ([EnergyBillV1EnergyConsumer](#energy-consumer-field)): The entity that consumes the energy.

```py
print(result.document.inference.prediction.energy_consumer.value)
```

## Energy Supplier
**energy_supplier** ([EnergyBillV1EnergySupplier](#energy-supplier-field)): The company that supplies the energy.

```py
print(result.document.inference.prediction.energy_supplier.value)
```

## Energy Usage
**energy_usage** (List[[EnergyBillV1EnergyUsage](#energy-usage-field)]): Details of energy consumption.

```py
for energy_usage_elem in result.document.inference.prediction.energy_usage:
    print(energy_usage_elem.value)
```

## Invoice Date
**invoice_date** ([DateField](#datefield)): The date when the energy invoice was issued.

```py
print(result.document.inference.prediction.invoice_date.value)
```

## Invoice Number
**invoice_number** ([StringField](#stringfield)): The unique identifier of the energy invoice.

```py
print(result.document.inference.prediction.invoice_number.value)
```

## Meter Details
**meter_details** ([EnergyBillV1MeterDetail](#meter-details-field)): Information about the energy meter.

```py
print(result.document.inference.prediction.meter_details.value)
```

## Subscription
**subscription** (List[[EnergyBillV1Subscription](#subscription-field)]): The subscription details fee for the energy service.

```py
for subscription_elem in result.document.inference.prediction.subscription:
    print(subscription_elem.value)
```

## Taxes and Contributions
**taxes_and_contributions** (List[[EnergyBillV1TaxesAndContribution](#taxes-and-contributions-field)]): Details of Taxes and Contributions.

```py
for taxes_and_contributions_elem in result.document.inference.prediction.taxes_and_contributions:
    print(taxes_and_contributions_elem.value)
```

## Total Amount
**total_amount** ([AmountField](#amountfield)): The total amount to be paid for the energy invoice.

```py
print(result.document.inference.prediction.total_amount.value)
```

## Total Before Taxes
**total_before_taxes** ([AmountField](#amountfield)): The total amount to be paid for the energy invoice before taxes.

```py
print(result.document.inference.prediction.total_before_taxes.value)
```

## Total Taxes
**total_taxes** ([AmountField](#amountfield)): Total of taxes applied to the invoice.

```py
print(result.document.inference.prediction.total_taxes.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
