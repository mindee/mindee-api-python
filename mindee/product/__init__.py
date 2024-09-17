from mindee.product import eu, fr, us
from mindee.product.barcode_reader import BarcodeReaderV1, BarcodeReaderV1Document
from mindee.product.bill_of_lading import (
    BillOfLadingV1,
    BillOfLadingV1Carrier,
    BillOfLadingV1CarrierItem,
    BillOfLadingV1Consignee,
    BillOfLadingV1Document,
    BillOfLadingV1NotifyParty,
    BillOfLadingV1Shipper,
)
from mindee.product.cropper import CropperV1, CropperV1Document
from mindee.product.custom import CustomV1, CustomV1Document, CustomV1Page
from mindee.product.financial_document import (
    FinancialDocumentV1,
    FinancialDocumentV1Document,
    FinancialDocumentV1LineItem,
)
from mindee.product.generated import GeneratedV1, GeneratedV1Document, GeneratedV1Page
from mindee.product.international_id import (
    InternationalIdV1,
    InternationalIdV1Document,
    InternationalIdV2,
    InternationalIdV2Document,
)
from mindee.product.invoice import InvoiceV4, InvoiceV4Document, InvoiceV4LineItem
from mindee.product.invoice_splitter import InvoiceSplitterV1, InvoiceSplitterV1Document
from mindee.product.material_certificate import (
    MaterialCertificateV1,
    MaterialCertificateV1Document,
)
from mindee.product.multi_receipts_detector import (
    MultiReceiptsDetectorV1,
    MultiReceiptsDetectorV1Document,
)
from mindee.product.nutrition_facts_label import (
    NutritionFactsLabelV1,
    NutritionFactsLabelV1AddedSugar,
    NutritionFactsLabelV1Calorie,
    NutritionFactsLabelV1Cholesterol,
    NutritionFactsLabelV1DietaryFiber,
    NutritionFactsLabelV1Document,
    NutritionFactsLabelV1Nutrient,
    NutritionFactsLabelV1Protein,
    NutritionFactsLabelV1SaturatedFat,
    NutritionFactsLabelV1ServingSize,
    NutritionFactsLabelV1Sodium,
    NutritionFactsLabelV1TotalCarbohydrate,
    NutritionFactsLabelV1TotalFat,
    NutritionFactsLabelV1TotalSugar,
    NutritionFactsLabelV1TransFat,
)
from mindee.product.passport import PassportV1, PassportV1Document
from mindee.product.proof_of_address import ProofOfAddressV1, ProofOfAddressV1Document
from mindee.product.receipt import (
    ReceiptV4,
    ReceiptV4Document,
    ReceiptV5,
    ReceiptV5Document,
    ReceiptV5LineItem,
)
from mindee.product.resume import ResumeV1, ResumeV1Document
