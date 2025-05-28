---
title: US US Mail OCR Python
category: 622b805aaec68102ea7fcbc2
slug: python-us-us-mail-ocr
parentDoc: 609808f773b0b90051d839de
---
The Python OCR SDK supports the [US Mail API](https://platform.mindee.com/mindee/us_mail).

The [sample below](https://github.com/mindee/client-lib-test-data/blob/main/products/us_mail/default_sample.jpg) can be used for testing purposes.
![US Mail sample](https://github.com/mindee/client-lib-test-data/blob/main/products/us_mail/default_sample.jpg?raw=true)

# Quick-Start
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
    product.us.UsMailV3,
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

### StringField
The text field `StringField` only has one constraint: its **value** is an `Optional[str]`.

## Specific Fields
Fields which are specific to this product; they are not used in any other product.

### Recipient Addresses Field
The addresses of the recipients.

A `UsMailV3RecipientAddress` implements the following attributes:

* **city** (`str`): The city of the recipient's address.
* **complete** (`str`): The complete address of the recipient.
* **is_address_change** (`bool`): Indicates if the recipient's address is a change of address.
* **postal_code** (`str`): The postal code of the recipient's address.
* **private_mailbox_number** (`str`): The private mailbox number of the recipient's address.
* **state** (`str`): Second part of the ISO 3166-2 code, consisting of two letters indicating the US State.
* **street** (`str`): The street of the recipient's address.
* **unit** (`str`): The unit number of the recipient's address.
Fields which are specific to this product; they are not used in any other product.

### Sender Address Field
The address of the sender.

A `UsMailV3SenderAddress` implements the following attributes:

* **city** (`str`): The city of the sender's address.
* **complete** (`str`): The complete address of the sender.
* **postal_code** (`str`): The postal code of the sender's address.
* **state** (`str`): Second part of the ISO 3166-2 code, consisting of two letters indicating the US State.
* **street** (`str`): The street of the sender's address.

# Attributes
The following fields are extracted for US Mail V3:

## Return to Sender
**is_return_to_sender** ([BooleanField](#booleanfield)): Whether the mailing is marked as return to sender.

```py
print(result.document.inference.prediction.is_return_to_sender.value)
```

## Recipient Addresses
**recipient_addresses** (List[[UsMailV3RecipientAddress](#recipient-addresses-field)]): The addresses of the recipients.

```py
for recipient_addresses_elem in result.document.inference.prediction.recipient_addresses:
    print(recipient_addresses_elem.value)
```

## Recipient Names
**recipient_names** (List[[StringField](#stringfield)]): The names of the recipients.

```py
for recipient_names_elem in result.document.inference.prediction.recipient_names:
    print(recipient_names_elem.value)
```

## Sender Address
**sender_address** ([UsMailV3SenderAddress](#sender-address-field)): The address of the sender.

```py
print(result.document.inference.prediction.sender_address.value)
```

## Sender Name
**sender_name** ([StringField](#stringfield)): The name of the sender.

```py
print(result.document.inference.prediction.sender_name.value)
```

# Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-2d0ds7dtz-DPAF81ZqTy20chsYpQBW5g)
