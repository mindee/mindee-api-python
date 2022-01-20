from mindee.documents.document_config import DocumentConfigDict
from mindee.documents.receipt import Receipt
from mindee.documents.financial_document import FinancialDocument
from mindee.documents.invoice import Invoice
from mindee.documents.passport import Passport

DOCUMENT_CONFIGS: DocumentConfigDict = {
    "receipt": Receipt.get_document_config(),
    "invoice": Invoice.get_document_config(),
    "financial_document": FinancialDocument.get_document_config(),
    "passport": Passport.get_document_config(),
}
