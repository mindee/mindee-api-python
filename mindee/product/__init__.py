from mindee.product import fr, ind, us
from mindee.product.barcode_reader.barcode_reader_v1 import BarcodeReaderV1
from mindee.product.barcode_reader.barcode_reader_v1_document import (
    BarcodeReaderV1Document,
)
from mindee.product.bill_of_lading.bill_of_lading_v1 import BillOfLadingV1
from mindee.product.bill_of_lading.bill_of_lading_v1_carrier import (
    BillOfLadingV1Carrier,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_carrier_item import (
    BillOfLadingV1CarrierItem,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_consignee import (
    BillOfLadingV1Consignee,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_document import (
    BillOfLadingV1Document,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_notify_party import (
    BillOfLadingV1NotifyParty,
)
from mindee.product.bill_of_lading.bill_of_lading_v1_shipper import (
    BillOfLadingV1Shipper,
)
from mindee.product.business_card.business_card_v1 import BusinessCardV1
from mindee.product.business_card.business_card_v1_document import (
    BusinessCardV1Document,
)
from mindee.product.cropper.cropper_v1 import CropperV1
from mindee.product.cropper.cropper_v1_document import (
    CropperV1Document,
)
from mindee.product.cropper.cropper_v1_page import (
    CropperV1Page,
)
from mindee.product.custom import CustomV1, CustomV1Document, CustomV1Page
from mindee.product.delivery_note.delivery_note_v1 import DeliveryNoteV1
from mindee.product.delivery_note.delivery_note_v1_document import (
    DeliveryNoteV1Document,
)
from mindee.product.driver_license.driver_license_v1 import DriverLicenseV1
from mindee.product.driver_license.driver_license_v1_document import (
    DriverLicenseV1Document,
)
from mindee.product.financial_document.financial_document_v1 import FinancialDocumentV1
from mindee.product.financial_document.financial_document_v1_document import (
    FinancialDocumentV1Document,
)
from mindee.product.financial_document.financial_document_v1_line_item import (
    FinancialDocumentV1LineItem,
)
from mindee.product.generated import GeneratedV1, GeneratedV1Document, GeneratedV1Page
from mindee.product.international_id.international_id_v2 import InternationalIdV2
from mindee.product.international_id.international_id_v2_document import (
    InternationalIdV2Document,
)
from mindee.product.invoice.invoice_v4 import InvoiceV4
from mindee.product.invoice.invoice_v4_document import (
    InvoiceV4Document,
)
from mindee.product.invoice.invoice_v4_line_item import (
    InvoiceV4LineItem,
)
from mindee.product.invoice_splitter.invoice_splitter_v1 import InvoiceSplitterV1
from mindee.product.invoice_splitter.invoice_splitter_v1_document import (
    InvoiceSplitterV1Document,
)
from mindee.product.invoice_splitter.invoice_splitter_v1_invoice_page_group import (
    InvoiceSplitterV1InvoicePageGroup,
)
from mindee.product.material_certificate.material_certificate_v1 import (
    MaterialCertificateV1,
)
from mindee.product.material_certificate.material_certificate_v1_document import (
    MaterialCertificateV1Document,
)
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1 import (
    MultiReceiptsDetectorV1,
)
from mindee.product.multi_receipts_detector.multi_receipts_detector_v1_document import (
    MultiReceiptsDetectorV1Document,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1 import (
    NutritionFactsLabelV1,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_added_sugar import (
    NutritionFactsLabelV1AddedSugar,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_calorie import (
    NutritionFactsLabelV1Calorie,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_cholesterol import (
    NutritionFactsLabelV1Cholesterol,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_dietary_fiber import (
    NutritionFactsLabelV1DietaryFiber,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_document import (
    NutritionFactsLabelV1Document,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_nutrient import (
    NutritionFactsLabelV1Nutrient,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_protein import (
    NutritionFactsLabelV1Protein,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_saturated_fat import (
    NutritionFactsLabelV1SaturatedFat,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_serving_size import (
    NutritionFactsLabelV1ServingSize,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_sodium import (
    NutritionFactsLabelV1Sodium,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_carbohydrate import (
    NutritionFactsLabelV1TotalCarbohydrate,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_fat import (
    NutritionFactsLabelV1TotalFat,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_total_sugar import (
    NutritionFactsLabelV1TotalSugar,
)
from mindee.product.nutrition_facts_label.nutrition_facts_label_v1_trans_fat import (
    NutritionFactsLabelV1TransFat,
)
from mindee.product.passport.passport_v1 import PassportV1
from mindee.product.passport.passport_v1_document import (
    PassportV1Document,
)
from mindee.product.receipt.receipt_v5 import ReceiptV5
from mindee.product.receipt.receipt_v5_document import (
    ReceiptV5Document,
)
from mindee.product.receipt.receipt_v5_line_item import (
    ReceiptV5LineItem,
)
from mindee.product.resume.resume_v1 import ResumeV1
from mindee.product.resume.resume_v1_certificate import (
    ResumeV1Certificate,
)
from mindee.product.resume.resume_v1_document import (
    ResumeV1Document,
)
from mindee.product.resume.resume_v1_education import (
    ResumeV1Education,
)
from mindee.product.resume.resume_v1_language import (
    ResumeV1Language,
)
from mindee.product.resume.resume_v1_professional_experience import (
    ResumeV1ProfessionalExperience,
)
from mindee.product.resume.resume_v1_social_networks_url import (
    ResumeV1SocialNetworksUrl,
)
