from mindee import PredictResponse, Client, product
from mindee.image_extraction.multi_receipts_extractor.mult_receipts_extractor import extract_receipts

# Init a new client
mindee_client = Client()

# Load a file from disk
input_doc = mindee_client.source_from_path("path/to/your/file.ext")
result_split: PredictResponse = mindee_client.parse(
    product.MultiReceiptsDetectorV1,
    input_doc,
    close_file=False
)

extracted_receipts = extract_receipts(input_doc, result_split.document.inference)
for receipt in extracted_receipts:
    receipt_as_source = receipt.as_source()
    # receipt.save_to_file(f"./local_test/{receipt.internal_file_name}.pdf") # Optionally: save each extracted receipt
    result_receipt = mindee_client.parse(product.ReceiptV5, receipt.as_source())
    print(result_receipt.document)
