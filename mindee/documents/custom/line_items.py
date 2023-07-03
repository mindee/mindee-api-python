from typing import Dict, List, Sequence

from mindee.documents.custom.custom_v1_fields import ListField, ListFieldValue
from mindee.geometry import (
    Quadrilateral,
    get_bounding_box,
    get_min_max_y,
    is_point_in_y,
    merge_polygons,
)


def _array_product(array: Sequence[float]) -> float:
    """
    Get the product of a sequence of floats.

    :array: List of floats
    """
    product = 1.0
    for k in array:
        product = product * k
    return product


def _find_best_anchor(anchors: Sequence[str], fields: Dict[str, ListField]) -> str:
    """
    Find the anchor with the most rows, in the order specified by `anchors`.

    Anchor will be the name of the field.
    """
    anchor = ""
    anchor_rows = 0
    for field in anchors:
        values = fields[field].values
        if len(values) > anchor_rows:
            anchor_rows = len(values)
            anchor = field
    return anchor


def _get_empty_field() -> ListFieldValue:
    """Return sample field with empty values."""
    return ListFieldValue({"content": "", "polygon": [], "confidence": 0.0})


class Line:
    """Represent a single line."""

    row_number: int
    fields: Dict[str, ListFieldValue]
    bounding_box: Quadrilateral


def get_line_items(
    anchors: Sequence[str], columns: Sequence[str], fields: Dict[str, ListField]
) -> List[Line]:
    """
    Reconstruct line items from fields.

    :anchors: Possible fields to use as an anchor
    :columns: All fields which are columns
    :fields: List of field names to reconstruct table with
    """
    line_items: List[Line] = []
    anchor = _find_best_anchor(anchors, fields)
    if not anchor:
        print(Warning("Could not find an anchor!"))
        return line_items

    # Loop on anchor items and create an item for each anchor item.
    # This will create all rows with just the anchor column value.
    for item in fields[anchor].values:
        line_item = Line()
        line_item.fields = {f: _get_empty_field() for f in columns}
        line_item.fields[anchor] = item
        line_items.append(line_item)

    # Loop on all created rows
    for idx, line in enumerate(line_items):
        # Compute sliding window between anchor item and the next
        min_y, _ = get_min_max_y(line.fields[anchor].polygon)
        if idx != len(line_items) - 1:
            max_y, _ = get_min_max_y(line_items[idx + 1].fields[anchor].polygon)
        else:
            max_y = 1.0  # bottom of page
        # Get candidates of each field included in sliding window and add it in line item
        for field in columns:
            field_words = [
                word
                for word in fields[field].values
                if is_point_in_y(word.polygon.centroid, min_y, max_y)
            ]
            line.fields[field].content = " ".join([v.content for v in field_words])
            try:
                line.fields[field].polygon = merge_polygons(
                    [v.polygon for v in field_words]
                )
            except ValueError:
                pass
            line.fields[field].confidence = _array_product(
                [v.confidence for v in field_words]
            )
        all_polygons = [line.fields[anchor].polygon]
        for field in columns:
            try:
                all_polygons.append(line.fields[field].polygon)
            except IndexError:
                pass
        line.bounding_box = get_bounding_box(merge_polygons(all_polygons))
        line.row_number = idx
    return line_items
