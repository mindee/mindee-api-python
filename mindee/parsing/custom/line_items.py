from typing import Dict, List, Sequence

from mindee.error.mindee_error import MindeeError
from mindee.geometry.bbox import BBox, extend_bbox, get_bbox
from mindee.geometry.minmax import MinMax, get_min_max_y
from mindee.geometry.quadrilateral import get_bounding_box
from mindee.parsing.custom.list import ListFieldV1, ListFieldValueV1


def _find_best_anchor(anchors: Sequence[str], fields: Dict[str, ListFieldV1]) -> str:
    """
    Find the anchor with the most rows, in the order specified by `anchors`.

    Anchor will be the name of the field.
    """
    anchor = ""
    anchor_rows = 0
    for field in anchors:
        values = fields[field].values
        if values and len(values) > anchor_rows:
            anchor_rows = len(values)
            anchor = field
    return anchor


class CustomLineV1:
    """Represent a single line."""

    row_number: int
    """Index of the row of a given line."""
    fields: Dict[str, ListFieldValueV1]
    """Fields contained in the line."""
    bbox: BBox
    """Simplified bounding box of the line."""

    def __init__(self, row_number: int):
        self.row_number = row_number
        self.bbox = BBox(1, 1, 0, 0)
        self.fields = {}

    def update_field(self, field_name: str, field_value: ListFieldValueV1) -> None:
        """
        Updates a field value if it exists.

        :param field_name: name of the field to update.
        :param field_value: value of the field to set.
        """
        if field_name in self.fields:
            existing_field = self.fields[field_name]
            existing_content = existing_field.content
            merged_content: str = ""
            if len(existing_content) > 0:
                merged_content += existing_content + " "
            merged_content += field_value.content
            merged_polygon = get_bounding_box(
                [*existing_field.polygon, *field_value.polygon]
            )
            merged_confidence = existing_field.confidence * field_value.confidence
        else:
            merged_content = field_value.content
            merged_confidence = field_value.confidence
            merged_polygon = get_bounding_box(field_value.polygon)

        self.fields[field_name] = ListFieldValueV1(
            {
                "content": merged_content,
                "confidence": merged_confidence,
                "polygon": merged_polygon,
            }
        )


def is_box_in_line(
    line: CustomLineV1, bbox: BBox, height_line_tolerance: float
) -> bool:
    """
    Checks if the bbox fits inside the line.

    :param anchor_name: name of the anchor.
    :param fields: fields to build lines from.
    :param height_line_tolerance: line height tolerance for custom line reconstruction.
    """
    if abs(bbox.y_min - line.bbox.y_min) <= height_line_tolerance:
        return True
    return abs(line.bbox.y_min - bbox.y_min) <= height_line_tolerance


def prepare(
    anchor_name: str, fields: Dict[str, ListFieldV1], height_line_tolerance: float
) -> List[CustomLineV1]:
    """
    Prepares lines before filling them.

    :param anchor_name: name of the anchor.
    :param fields: fields to build lines from.
    :param height_line_tolerance: line height tolerance for custom line reconstruction.
    """
    lines_prepared: List[CustomLineV1] = []
    try:
        anchor_field: ListFieldV1 = fields[anchor_name]
    except KeyError as exc:
        raise MindeeError("No lines have been detected.") from exc

    current_line_number: int = 1
    current_line = CustomLineV1(current_line_number)
    if anchor_field and len(anchor_field.values) > 0:
        current_value: ListFieldValueV1 = anchor_field.values[0]
        current_line.bbox = extend_bbox(
            current_line.bbox,
            current_value.polygon,
        )

        for i in range(1, len(anchor_field.values)):
            current_value = anchor_field.values[i]
            current_field_box = get_bbox(current_value.polygon)
            if not is_box_in_line(
                current_line, current_field_box, height_line_tolerance
            ):
                lines_prepared.append(current_line)
                current_line_number += 1
                current_line = CustomLineV1(current_line_number)
            current_line.bbox = extend_bbox(
                current_line.bbox,
                current_value.polygon,
            )
        if (
            len(
                [
                    line
                    for line in lines_prepared
                    if line.row_number == current_line_number
                ]
            )
            == 0
        ):
            lines_prepared.append(current_line)
    return lines_prepared


def get_line_items(
    anchors: Sequence[str],
    field_names: Sequence[str],
    fields: Dict[str, ListFieldV1],
    height_line_tolerance: float = 0.01,
) -> List[CustomLineV1]:
    """
    Reconstruct line items from fields.

    :anchors: Possible fields to use as an anchor
    :columns: All fields which are columns
    :fields: List of field names to reconstruct table with
    """
    line_items: List[CustomLineV1] = []
    fields_to_transform: Dict[str, ListFieldV1] = {}
    for field_name, field_value in fields.items():
        if field_name in field_names:
            fields_to_transform[field_name] = field_value
    anchor = _find_best_anchor(anchors, fields_to_transform)
    if not anchor:
        print(Warning("Could not find an anchor!"))
        return line_items
    lines_prepared: List[CustomLineV1] = prepare(
        anchor, fields_to_transform, height_line_tolerance
    )

    for current_line in lines_prepared:
        for field_name, field in fields_to_transform.items():
            for list_field_value in field.values:
                min_max_y: MinMax = get_min_max_y(list_field_value.polygon)
                if (
                    abs(min_max_y.max - current_line.bbox.y_max)
                    <= height_line_tolerance
                    and abs(min_max_y.min - current_line.bbox.y_min)
                    <= height_line_tolerance
                ):
                    current_line.update_field(field_name, list_field_value)

    return lines_prepared
