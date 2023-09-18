def taxes_match_total_incl(doc) -> bool:
    """
    Check invoice matching rule between taxes and total_incl.

    :return: True if rule matches, False otherwise
    """
    # Ensure taxes and total_incl exist
    if not doc.taxes or not doc.total_amount.value:
        return False

    # Reconstruct total_incl from taxes
    total_vat = 0.0
    reconstructed_total = 0.0
    for tax in doc.taxes:
        if tax.value is None or tax.rate is None or tax.rate == 0:
            return False
        total_vat += tax.value
        reconstructed_total += tax.value + 100 * tax.value / tax.rate

    # Sanity check
    if total_vat <= 0:
        return False

    # Crate epsilon
    eps = 1 / (100 * total_vat)
    if (
        doc.total_amount.value * (1 - eps) - 0.02
        <= reconstructed_total
        <= doc.total_amount.value * (1 + eps) + 0.02
    ):
        for tax in doc.taxes:
            tax.confidence = 1
        doc.total_tax.confidence = 1.0
        doc.total_amount.confidence = 1.0
        return True
    return False


def taxes_match_total_excl(doc) -> bool:
    """
    Check invoice matching rule between taxes and total_excl.

    :return: True if rule matches, False otherwise
    """
    # Check taxes and total excl exist
    if len(doc.taxes) == 0 or doc.total_net.value is None:
        return False

    # Reconstruct total excl from taxes
    total_vat = 0.0
    reconstructed_total = 0.0
    for tax in doc.taxes:
        if tax.value is None or tax.rate is None or tax.rate == 0:
            return False
        total_vat += tax.value
        reconstructed_total += 100 * tax.value / tax.rate

    # Sanity check
    if total_vat <= 0:
        return False

    # Crate epsilon
    eps = 1 / (100 * total_vat)
    # Check that reconstructed total excl matches total excl
    if (
        doc.total_net.value * (1 - eps) - 0.02
        <= reconstructed_total
        <= doc.total_net.value * (1 + eps) + 0.02
    ):
        for tax in doc.taxes:
            tax.confidence = 1
        doc.total_tax.confidence = 1.0
        doc.total_net.confidence = 1.0
        return True
    return False


def taxes_plus_total_excl_match_total_incl(doc) -> bool:
    """
    Check invoice matching rule.

    Rule is: sum(taxes) + total_excluding_taxes = total_including_taxes
    :return: True if rule matches, False otherwise
    """
    # Check total_tax, total excl and total incl exist
    if (
        doc.total_net.value is None
        or len(doc.taxes) == 0
        or doc.total_amount.value is None
    ):
        return False

    # Reconstruct total_incl
    total_vat = 0.0
    for tax in doc.taxes:
        if tax.value is not None:
            total_vat += tax.value
    reconstructed_total = total_vat + doc.total_net.value

    # Sanity check
    if total_vat <= 0:
        return False

    # Check that reconstructed total incl matches total excl + taxes sum
    if (
        doc.total_amount.value - 0.01
        <= reconstructed_total
        <= doc.total_amount.value + 0.01
    ):
        for tax in doc.taxes:
            tax.confidence = 1
        doc.total_tax.confidence = 1.0
        doc.total_net.confidence = 1.0
        doc.total_amount.confidence = 1.0
        return True
    return False
