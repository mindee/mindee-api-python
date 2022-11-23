from mindee.fields.amount import AmountField
from mindee.fields.base import field_array_confidence


def total_incl_from_taxes_plus_excl(doc) -> None:
    """
    Set self.total_incl with Amount object.

    The total_incl Amount value is the sum of total_excl and sum of taxes
    The total_incl Amount confidence is the product of self.taxes probabilities
        multiplied by total_excl confidence
    """
    # Check total_tax, total excl exist and total incl is not set
    if not (
        doc.total_net.value is None
        or len(doc.taxes) == 0
        or doc.total_amount.value is not None
    ):
        total_incl = {
            "value": sum(tax.value if tax.value is not None else 0 for tax in doc.taxes)
            + doc.total_net.value,
            "confidence": field_array_confidence(doc.taxes) * doc.total_net.confidence,
        }
        doc.total_amount = AmountField(total_incl, reconstructed=True)


def total_excl_from_tcc_and_taxes(doc) -> None:
    """
    Set self.total_excl with Amount object.

    The total_excl Amount value is the difference between total_incl and sum of taxes
    The total_excl Amount confidence is the product of self.taxes probabilities
        multiplied by total_incl confidence
    """
    # Check total_tax, total excl and total incl exist
    if (
        doc.total_amount.value is None
        or len(doc.taxes) == 0
        or doc.total_net.value is not None
    ):
        return

    total_excl = {
        "value": doc.total_amount.value
        - sum(tax.value if tax.value is not None else 0 for tax in doc.taxes),
        "confidence": field_array_confidence(doc.taxes) * doc.total_amount.confidence,
    }
    doc.total_net = AmountField(total_excl, reconstructed=True)


def total_tax_from_tax_lines(doc) -> None:
    """
    Set self.total_tax with Amount object.

    The total_tax Amount value is the sum of all self.taxes value
    The total_tax Amount confidence is the product of self.taxes probabilities
    """
    if doc.taxes:
        total_tax = {
            "value": sum(
                tax.value if tax.value is not None else 0 for tax in doc.taxes
            ),
            "confidence": field_array_confidence(doc.taxes),
        }
        if total_tax["value"] > 0:
            doc.total_tax = AmountField(total_tax, reconstructed=True)


def total_tax_from_incl_and_excl(doc) -> None:
    """
    Set self.total_tax with Amount object.

    Check if the total tax was already set
    If not, set thta total tax amount to the diff of incl and excl
    """
    if (
        doc.total_tax.value is not None
        or doc.total_net.value is None
        or doc.total_amount.value is None
    ):
        return

    total_tax = {
        "value": doc.total_amount.value - doc.total_net.value,
        "confidence": doc.total_amount.confidence * doc.total_net.confidence,
    }
    if total_tax["value"] >= 0:
        doc.total_tax = AmountField(total_tax, reconstructed=True)
