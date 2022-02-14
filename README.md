# Mindee API Helper Library for Python

## Quick Start
Here's the TL;DR of getting started.

First, get an [API Key](https://developers.mindee.com/docs/make-your-first-request#create-an-api-key)

Then, install this library:
```shell script
pip install mindee
```

Finally, Python away!

### Off-the-Shelf Document
```python
from mindee import Client

# Init a new client and configure the Invoice API
mindee_client = Client().config_invoice("my-invoice-api-key")

# Load a file from disk and parse it
api_response = mindee_client.doc_from_path("/path/to/the/invoice.pdf").parse("invoice")

# Print a brief summary of the parsed data
print(api_response.invoice)
```

### Custom Document (API Builder)
```python
from mindee import Client

# Init a new client and configure your custom document
mindee_client = Client().config_custom_doc(
      document_type="pokemon-card",
      singular_name="card",
      plural_name="cards",
      account_name="pikachu",
      api_key="pokemon-card-api-key"
)

# Load a file from disk and parse it
api_response = mindee_client.doc_from_path("/path/to/the/card.jpg").parse("pokemon-card")

# Print a brief summary of the parsed data
print(api_response.card)
```

## Further Reading
There's more to it than that for those that need more features, or want to
customize the experience.

All the juicy details are described in the
**[Official Documentation](https://developers.mindee.com/docs/getting-started)**.

## License
Copyright © Mindee

Distributed under the MIT License.
