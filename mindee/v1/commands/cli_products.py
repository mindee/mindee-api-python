from dataclasses import dataclass
from typing import Generic

from mindee.v1 import product
from mindee.v1.parsing.common import TypeInference


@dataclass
class CommandConfig(Generic[TypeInference]):
    """Configuration for a command."""

    help: str
    doc_class: type[TypeInference]
    is_sync: bool
    is_async: bool


PRODUCTS: dict[str, CommandConfig] = {
    "custom": CommandConfig(
        help="Custom document type from API builder",
        doc_class=product.CustomV1,
        is_sync=True,
        is_async=False,
    ),
    "generated": CommandConfig(
        help="Generated products from docTI",
        doc_class=product.GeneratedV1,
        is_sync=True,
        is_async=True,
    ),
    "barcode-reader": CommandConfig(
        help="Barcode Reader",
        doc_class=product.BarcodeReaderV1,
        is_sync=True,
        is_async=False,
    ),
    "cropper": CommandConfig(
        help="Cropper",
        doc_class=product.CropperV1,
        is_sync=True,
        is_async=False,
    ),
    "financial-document": CommandConfig(
        help="Financial Document",
        doc_class=product.FinancialDocumentV1,
        is_sync=True,
        is_async=True,
    ),
    "fr-bank-account-details": CommandConfig(
        help="Bank Account Details",
        doc_class=product.fr.BankAccountDetailsV2,
        is_sync=True,
        is_async=False,
    ),
    "fr-carte-grise": CommandConfig(
        help="Carte Grise",
        doc_class=product.fr.CarteGriseV1,
        is_sync=True,
        is_async=False,
    ),
    "fr-carte-nationale-d-identite": CommandConfig(
        help="Carte Nationale d'Identité",
        doc_class=product.fr.IdCardV2,
        is_sync=True,
        is_async=False,
    ),
    "international-id": CommandConfig(
        help="International ID",
        doc_class=product.InternationalIdV2,
        is_sync=False,
        is_async=True,
    ),
    "invoice": CommandConfig(
        help="Invoice",
        doc_class=product.InvoiceV4,
        is_sync=True,
        is_async=True,
    ),
    "invoice-splitter": CommandConfig(
        help="Invoice Splitter",
        doc_class=product.InvoiceSplitterV1,
        is_sync=False,
        is_async=True,
    ),
    "multi-receipts-detector": CommandConfig(
        help="Multi Receipts Detector",
        doc_class=product.MultiReceiptsDetectorV1,
        is_sync=True,
        is_async=False,
    ),
    "passport": CommandConfig(
        help="Passport",
        doc_class=product.PassportV1,
        is_sync=True,
        is_async=False,
    ),
    "receipt": CommandConfig(
        help="Receipt",
        doc_class=product.ReceiptV5,
        is_sync=True,
        is_async=True,
    ),
    "us-bank-check": CommandConfig(
        help="Bank Check",
        doc_class=product.us.BankCheckV1,
        is_sync=True,
        is_async=False,
    ),
}
