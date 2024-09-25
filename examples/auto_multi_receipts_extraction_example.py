from mindee import Client, PredictResponse, product
from mindee.extraction.multi_receipts_extractor.multi_receipts_extractor import (
    extract_receipts,
)

mindee_client = Client(api_key="my-api-key")
# mindee_client = Client() # Optionally, set from env.


def parse_receipts(input_path):
    input_doc = mindee_client.source_from_path(input_path)
    result_split: PredictResponse = mindee_client.parse(
        product.MultiReceiptsDetectorV1, input_doc, close_file=False
    )

    extracted_receipts = extract_receipts(input_doc, result_split.document.inference)
    for receipt in extracted_receipts:
        receipt_as_source = receipt.as_source()
        # receipt.save_to_file(f"./{receipt.internal_file_name}.pdf") # Optionally: save each extracted receipt
        result_receipt = mindee_client.parse(product.ReceiptV5, receipt.as_source())
        print(result_receipt.document)


if __name__ == "__main__":
    input_path = "path/to/your/file.ext"
    parse_receipts(input_path)
