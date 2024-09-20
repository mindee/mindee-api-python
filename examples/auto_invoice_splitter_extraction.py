import os

from mindee import Client
from mindee.extraction.pdf_extractor import PdfExtractor
from mindee.input import PathInput
from mindee.product import InvoiceSplitterV1, InvoiceV4

api_key = os.getenv("MINDEE_API_KEY")
mindee_client = Client(api_key=api_key)

input_path = "path/to/your/file.ext"
input_source = PathInput(input_path)

if input_source.is_pdf():
    pdf_extractor = PdfExtractor(input_source)
    if pdf_extractor.get_page_count() > 1:
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

            invoice_result = mindee_client.parse(
                InvoiceV4, extracted_pdf.as_input_source()
            )
            print(invoice_result.document)
    else:
        invoice_result = mindee_client.parse(InvoiceV4, input_source)
        print(invoice_result.document)
else:
    invoice_result = mindee_client.parse(InvoiceV4, input_source)
    print(invoice_result.document)
