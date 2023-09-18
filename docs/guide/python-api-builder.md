The Python OCR SDK supports [custom-built API](https://developers.mindee.com/docs/build-your-first-document-parsing-api) from the API Builder. If your document isn't covered by one of Mindee's Off-the-Shelf APIs, you can create your own API using the [API Builder](https://developers.mindee.com/docs/overview).

If your document isn't covered by one of Mindee's Off-the-Shelf APIs, you can create your own API using the
[API Builder](https://developers.mindee.com/docs/overview).

For the following examples, we are using our own [W9s custom API](https://developers.mindee.com/docs/w9-forms-ocr),
created with the [API Builder](https://developers.mindee.com/docs/overview).

```python
from mindee import Client, product

# Init a new client and add your custom endpoint (document)
mindee_client = Client(api_key="my-api-key").add_endpoint(
    account_name="john",
    endpoint_name="wsnine",
    # version="1.2",  # optional, see configuring client section below
)

# Load a file from disk and parse it.
# The endpoint name must be specified since it can't be determined from the class.
result = mindee_client.doc_from_path(
    "/path/to/the/w9.jpg"
).parse(product.TypeCustomV1, endpoint_name="wnine")

# Print a brief summary of the parsed data
print(result.document)
```

## Adding the Endpoint
Below are the arguments for adding a custom endpoint using the `add_endpoint` method.

**`endpoint_name`**: The endpoint name is the API name from [Settings](https://developers.mindee.com/docs/build-your-first-document-parsing-api#settings-api-keys-and-documentation) page

**`account_name`**: Your organization's or user's name in the API Builder.

**`version`**: If set, locks the version of the model to use, you'll be required to update your code every time a new model is trained. 
 This is probably not needed for development but essential for production use.
 If not set, uses the latest version of the model.

## Parsing Documents
The client calls the `parse` method when parsing your custom document, which will return an object containing the prediction results of sent file.
The `endpoint_name` must be specified when calling the `parse` method for a custom endpoint.

```python
result = mindee_client.doc_from_path("/path/to/receipt.jpg").parse(
    product.TypeCustomV1, endpoint_name="wnine"
)

print(result.document)
```

> 📘 **Info**
>
> If your custom document has the same name as an [off-the-shelf APIs](https://developers.mindee.com/docs/what-is-off-the-shelf-api) document,
> you **must** specify your account name when calling the `parse` method:

```python
from mindee import Client, product

mindee_client = Client(api_key="johndoe-receipt-api-key").add_endpoint(
    endpoint_name="receipt",
    account_name="JohnDoe",
)

result = mindee_client.doc_from_path("/path/to/receipt.jpg").parse(
    product.TypeCustomV1,
    endpoint_name="wnine",
    account_name="JohnDoe",
)
```

## Document Fields
All the fields defined in the API Builder when creating your custom document are available.

In custom documents, each field will hold an array of all the words in the document which are related to that field.
Each word is an object that has the text content, geometry information, and confidence score.

Value fields can be accessed via the `fields` attribute.

Classification fields can be accessed via the `classifications` attribute.

> 📘 **Info**
>
> Both document level and page level objects work in the same way.

### Fields Attribute
The `fields` attribute is a dictionary with the following structure:

* key: the API name of the field, as a `str`
* value: a `ListField` object which has a `values` attribute, containing a list of all values found for the field.

Individual field values can be accessed by using the field's API name, in the examples below we'll use the `address` field.

```python
# raw data, list of each word object
print(result.document.fields["address"].values)

# list of all values
print(result.document.fields["address"].contents_list)

# default string representation
print(str(result.document.fields["address"]))

# custom string representation
print(result.document.fields["address"].contents_string(separator="_"))
```

To iterate over all the fields:
```python
for name, info in result.document.fields.items():
    print(name)
    print(info.values)
```

### Classifications Attribute
The `classifications` attribute is a dictionary with the following structure:

* key: the API name of the field, as a `str`
* value: a `ClassificationField` object which has a `value` attribute, containing a string representation of the detected classification.

```python
# raw data, list of each word object
print(result.document.classifications["doc_type"].values)
```

To iterate over all the classifications:
```python
for name, info in result.document.classifications.items():
    print(name)
    print(info.values)
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
