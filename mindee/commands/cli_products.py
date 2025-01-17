from dataclasses import dataclass
from typing import Dict, Generic, Type

from mindee import product
from mindee.parsing.common import TypeInference


@dataclass
class CommandConfig(Generic[TypeInference]):
    """Configuration for a command."""

    help: str
    doc_class: Type[TypeInference]
    is_sync: bool
    is_async: bool


PRODUCTS: Dict[str, CommandConfig] = {
    # "address-proof": CommandConfig(
    #     help="Address Proof",
    #     doc_class=product.AddressProofV1,
    #     is_sync=False,
    #     is_async=True,
    # ),
    "barcode-reader": CommandConfig(
        help="Barcode-reader tool",
        doc_class=product.BarcodeReaderV1,
        is_sync=True,
        is_async=False,
    ),
    "cropper": CommandConfig(
        help="Cropper tool",
        doc_class=product.CropperV1,
        is_sync=True,
        is_async=False,
    ),
    "custom": CommandConfig(
        help="Custom document type from API builder",
        doc_class=product.CustomV1,
        is_sync=True,
        is_async=False,
    ),
    "eu-license-plate": CommandConfig(
        help="EU License Plate",
        doc_class=product.eu.LicensePlateV1,
        is_sync=True,
        is_async=False,
    ),
    "driver-license": CommandConfig(
        help="Driver License",
        doc_class=product.DriverLicenseV1,
        is_sync=False,
        is_async=True,
    ),
    "financial-document": CommandConfig(
        help="Financial Document (receipt or invoice)",
        doc_class=product.FinancialDocumentV1,
        is_sync=True,
        is_async=True,
    ),
    "fr-bank-account-details": CommandConfig(
        help="FR Bank Account Details",
        doc_class=product.fr.BankAccountDetailsV2,
        is_sync=True,
        is_async=False,
    ),
    "fr-carte-grise": CommandConfig(
        help="FR Carte Grise",
        doc_class=product.fr.CarteGriseV1,
        is_sync=True,
        is_async=False,
    ),
    "fr-health-card": CommandConfig(
        help="FR Health Card",
        doc_class=product.fr.HealthCardV1,
        is_sync=False,
        is_async=True,
    ),
    "fr-id-card": CommandConfig(
        help="FR ID Card",
        doc_class=product.fr.IdCardV2,
        is_sync=True,
        is_async=False,
    ),
    "fr-payslip": CommandConfig(
        help="FR Payslip",
        doc_class=product.fr.PayslipV3,
        is_sync=False,
        is_async=True,
    ),
    "fr-petrol-receipt": CommandConfig(
        help="FR Petrol Receipt",
        doc_class=product.fr.PetrolReceiptV1,
        is_sync=True,
        is_async=False,
    ),
    "generated": CommandConfig(
        help="Generated",
        doc_class=product.GeneratedV1,
        is_sync=True,
        is_async=True,
    ),
    "invoice": CommandConfig(
        help="Invoice",
        doc_class=product.InvoiceV4,
        is_sync=True,
        is_async=True,
    ),
    "international-id": CommandConfig(
        help="International ID",
        doc_class=product.InternationalIdV2,
        is_sync=False,
        is_async=True,
    ),
    "invoice-splitter": CommandConfig(
        help="Invoice Splitter",
        doc_class=product.InvoiceSplitterV1,
        is_sync=False,
        is_async=True,
    ),
    "material-certificate": CommandConfig(
        help="Material Certificate",
        doc_class=product.MaterialCertificateV1,
        is_sync=False,
        is_async=True,
    ),
    "multi-receipts": CommandConfig(
        help="Multi-receipts detector",
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
        help="Expense Receipt",
        doc_class=product.ReceiptV5,
        is_sync=True,
        is_async=False,
    ),
    "resume": CommandConfig(
        help="Resume",
        doc_class=product.ResumeV1,
        is_sync=False,
        is_async=True,
    ),
    "us-bank-check": CommandConfig(
        help="US Bank Check",
        doc_class=product.us.BankCheckV1,
        is_sync=True,
        is_async=False,
    ),
    "us-mail": CommandConfig(
        help="US Mail",
        doc_class=product.us.UsMailV3,
        is_sync=False,
        is_async=True,
    ),
    "us-healthcare-card": CommandConfig(
        help="US Healthcare Card",
        doc_class=product.us.HealthcareCardV1,
        is_sync=False,
        is_async=True,
    ),
    "us-w9": CommandConfig(
        help="US W9",
        doc_class=product.us.W9V1,
        is_sync=True,
        is_async=False,
    ),
}
