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
    "bill-of-lading": CommandConfig(
        help="Bill of Lading",
        doc_class=product.BillOfLadingV1,
        is_sync=False,
        is_async=True,
    ),
    "business-card": CommandConfig(
        help="Business Card",
        doc_class=product.BusinessCardV1,
        is_sync=False,
        is_async=True,
    ),
    "cropper": CommandConfig(
        help="Cropper",
        doc_class=product.CropperV1,
        is_sync=True,
        is_async=False,
    ),
    "delivery-note": CommandConfig(
        help="Delivery note",
        doc_class=product.DeliveryNoteV1,
        is_sync=False,
        is_async=True,
    ),
    "driver-license": CommandConfig(
        help="Driver License",
        doc_class=product.DriverLicenseV1,
        is_sync=False,
        is_async=True,
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
    "fr-energy-bill": CommandConfig(
        help="Energy Bill",
        doc_class=product.fr.EnergyBillV1,
        is_sync=False,
        is_async=True,
    ),
    "fr-health-card": CommandConfig(
        help="Health Card",
        doc_class=product.fr.HealthCardV1,
        is_sync=False,
        is_async=True,
    ),
    "fr-carte-nationale-d-identite": CommandConfig(
        help="Carte Nationale d'Identité",
        doc_class=product.fr.IdCardV2,
        is_sync=True,
        is_async=False,
    ),
    "fr-payslip": CommandConfig(
        help="Payslip",
        doc_class=product.fr.PayslipV3,
        is_sync=False,
        is_async=True,
    ),
    "ind-passport-india": CommandConfig(
        help="Passport - India",
        doc_class=product.ind.IndianPassportV1,
        is_sync=False,
        is_async=True,
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
    "material-certificate": CommandConfig(
        help="Material Certificate",
        doc_class=product.MaterialCertificateV1,
        is_sync=False,
        is_async=True,
    ),
    "multi-receipts-detector": CommandConfig(
        help="Multi Receipts Detector",
        doc_class=product.MultiReceiptsDetectorV1,
        is_sync=True,
        is_async=False,
    ),
    "nutrition-facts-label": CommandConfig(
        help="Nutrition Facts Label",
        doc_class=product.NutritionFactsLabelV1,
        is_sync=False,
        is_async=True,
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
    "resume": CommandConfig(
        help="Resume",
        doc_class=product.ResumeV1,
        is_sync=False,
        is_async=True,
    ),
    "us-bank-check": CommandConfig(
        help="Bank Check",
        doc_class=product.us.BankCheckV1,
        is_sync=True,
        is_async=False,
    ),
    "us-healthcare-card": CommandConfig(
        help="Healthcare Card",
        doc_class=product.us.HealthcareCardV1,
        is_sync=False,
        is_async=True,
    ),
    "us-us-mail": CommandConfig(
        help="US Mail",
        doc_class=product.us.UsMailV3,
        is_sync=False,
        is_async=True,
    ),
}
