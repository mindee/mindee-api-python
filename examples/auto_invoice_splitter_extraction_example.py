import os

from mindee import Client
from mindee.extraction.pdf_extractor import PdfExtractor
from mindee.input import PathInput
from mindee.product import InvoiceSplitterV1, InvoiceV4

mindee_client = Client(api_key="my-api-key")
# mindee_client = Client() # Optionally, set from env.


def parse_invoice(file_path):
    input_source = PathInput(file_path)

    if input_source.is_pdf() and input_source.count_doc_pages() > 1:
        parse_multi_page(input_source)
    else:
        parse_single(input_source)


def parse_single(input_source):
    invoice_result = mindee_client.parse(InvoiceV4, input_source)
    print(invoice_result.document)


def parse_multi_page(input_source):
    pdf_extractor = PdfExtractor(input_source)
    invoice_splitter_response = mindee_client.enqueue_and_parse(
        InvoiceSplitterV1, input_source, close_file=False
    )
    page_groups = (
        invoice_splitter_response.document.inference.prediction.invoice_page_groups
    )
    extracted_pdfs = pdf_extractor.extract_invoices(page_groups, strict=False)

    for extracted_pdf in extracted_pdfs:
        # Optional: Save the files locally
        # extracted_pdf.write_to_file("output/path")

        invoice_result = mindee_client.parse(InvoiceV4, extracted_pdf.as_input_source())
        print(invoice_result.document)


if __name__ == "__main__":
    parse_invoice(input_path)
