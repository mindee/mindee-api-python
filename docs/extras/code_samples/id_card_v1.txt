from mindee import Client, documents

# Init a new client
mindee_client = Client(api_key="my-api-key")

# Load a file from disk
input_doc = mindee_client.doc_from_path("/path/to/the/file.ext")

# Parse the Carte Nationale d'Identité by passing the appropriate type
result = input_doc.parse(documents.fr.TypeIdCardV1)

# Print a brief summary of the parsed data
print(result.document)
