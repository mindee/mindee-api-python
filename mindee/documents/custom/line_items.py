from typing import Dict, List, Sequence

from mindee.geometry import (
    get_bounding_box_for_polygons,
    get_centroid,
    get_min_max_y,
    is_point_in_y,
)


def array_product(array: Sequence[float]) -> float:
    """
    Get the product of a sequence of floats.

    :array: List of floats
    """
    product = 1.0
    for k in array:
        product = product * k
    return product


def find_best_anchor(anchors: Sequence[str], fields: Dict[str, dict]) -> str:
    """
    Find the anchor with the most rows, in the order specified by `anchors`.

    Anchor will be the name of the field.
    """
    anchor = ""
    anchor_rows = 0
    for field in anchors:
        values = fields[field]["values"]
        if len(values) > anchor_rows:
            anchor_rows = len(values)
            anchor = field
    return anchor


def get_empty_field() -> dict:
    """Return sample field with empty values."""
    return {"content": "", "polygon": [], "confidence": 0.0}


def get_line_items(
    anchors: Sequence[str], columns: Sequence[str], fields: Dict[str, dict]
) -> List[dict]:
    """
    Reconstruct line items from fields.

    :anchors: Possible fields to use as an anchor
    :columns: All fields which are columns
    :fields: List of field names to reconstruct table with
    """
    line_items: List[dict] = []
    anchor = find_best_anchor(anchors, fields)
    if not anchor:
        print(Warning("Could not find an anchor!"))
        return line_items

    # Loop on anchor items and create an item for each anchor item.
    # This will create all rows with just the anchor column value.
    for item in fields[anchor]["values"]:
        line_item = {f: get_empty_field() for f in columns}
        line_item[anchor] = item
        line_items.append(line_item)

    # Loop on all created rows
    for idx, _ in enumerate(line_items):
        # Compute sliding window between anchor item and the next
        min_y, _ = get_min_max_y(line_items[idx][anchor]["polygon"])
        if idx != len(line_items) - 1:
            max_y, _ = get_min_max_y(line_items[idx + 1][anchor]["polygon"])
        else:
            max_y = 1.0  # bottom of page
        # Get candidates of each field included in sliding window and add it in line item
        for field in columns:
            field_words = [
                word
                for word in fields[field]["values"]
                if is_point_in_y(get_centroid(word["polygon"]), min_y, max_y)
            ]
            line_items[idx][field]["content"] = " ".join(
                [v["content"] for v in field_words]
            )
            try:
                line_items[idx][field]["polygon"] = get_bounding_box_for_polygons(
                    [v["polygon"] for v in field_words]
                )
            except ValueError:
                pass
            line_items[idx][field]["confidence"] = array_product(
                [v["confidence"] for v in field_words]
            )
        # Create coordinates and id attributes for frontend SDK of line item
        all_polygons = [line_items[idx][anchor]["polygon"]]
        for field in columns:
            try:
                all_polygons.append(line_items[idx][field]["polygon"])
            except IndexError:
                pass
        line_items[idx]["bounding_box"] = get_bounding_box_for_polygons(all_polygons)
        line_items[idx]["id"] = idx
    return line_items
