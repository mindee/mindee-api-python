from mindee import Client, product
from mindee.extraction.multi_receipts_extractor.multi_receipts_extractor import (
    extract_receipts,
)


def parse_receipts(input_path):
    mindee_client = Client(api_key="my-api-key-here")
    # mindee_client = Client()  # Optionally, set from env.
    input_doc = mindee_client.source_from_path(input_path)

    result_split = mindee_client.parse(
        product.MultiReceiptsDetectorV1, input_doc, close_file=False
    )

    extracted_receipts = extract_receipts(input_doc, result_split.document.inference)

    for idx, receipt in enumerate(extracted_receipts, 1):
        result_receipt = mindee_client.parse(product.ReceiptV5, receipt.as_source())
        print(f"Receipt {idx}:")
        print(result_receipt.document)
        print("-" * 40)

        # Uncomment to save each extracted receipt
        # save_path = f"./receipt_{idx}.pdf"
        # receipt.save_to_file(save_path)


if __name__ == "__main__":
    input_file = "path/to/my/file.ext"
    parse_receipts(input_file)
