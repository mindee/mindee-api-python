from datetime import datetime
from typing import Generic, Optional, Type

from mindee.parsing.common.execution_file import ExecutionFile
from mindee.parsing.common.execution_priority import ExecutionPriority
from mindee.parsing.common.inference import Inference
from mindee.parsing.common.page import Page
from mindee.parsing.common.prediction import TypePrediction
from mindee.parsing.common.string_dict import StringDict
from mindee.product.generated.generated_v1 import GeneratedV1Document


class Execution(Generic[TypePrediction]):
    """Workflow execution class."""

    batch_name: str
    """Identifier for the batch to which the execution belongs."""

    created_at: Optional[datetime] = None
    """The time at which the execution started."""

    file: ExecutionFile
    """File representation within a workflow execution."""

    id: str
    """Identifier for the execution."""

    inference: Optional[Inference[TypePrediction, Page[TypePrediction]]]
    """Deserialized inference object."""

    priority: Optional["ExecutionPriority"] = None
    """Priority of the execution."""

    reviewed_at: Optional[datetime]
    """The time at which the file was tagged as reviewed."""

    available_at: Optional[datetime]
    """The time at which the file was uploaded to a workflow."""

    reviewed_prediction: Optional["GeneratedV1Document"] = None
    """Reviewed fields and values."""

    status: str
    """Execution Status."""

    type: Optional[str]
    """Execution type."""

    uploaded_at: Optional[datetime] = None
    """The time at which the file was uploaded to a workflow."""

    workflow_id: str
    """Identifier for the workflow."""

    def __init__(self, inference_type: Type[Inference], json_response: StringDict):
        self.batch_name = json_response["batch_name"]
        self.created_at = self.parse_date(json_response.get("created_at", None))
        self.file = ExecutionFile(json_response["file"])
        self.id = json_response["id"]
        self.inference = (
            inference_type(json_response["inference"])
            if json_response["inference"]
            else None
        )
        self.priority = json_response.get("priority", None)
        self.reviewed_at = self.parse_date(json_response.get("reviewed_at", None))
        self.available_at = self.parse_date(json_response.get("available_at", None))
        self.reviewed_prediction = (
            GeneratedV1Document(json_response["reviewed_prediction"])
            if json_response["reviewed_prediction"]
            else None
        )
        self.status = json_response["status"]
        self.type = json_response.get("type", None)
        self.uploaded_at = self.parse_date(json_response.get("uploaded_at", None))
        self.workflow_id = json_response["workflow_id"]

    @staticmethod
    def parse_date(date_string: Optional[str]) -> Optional[datetime]:
        """Shorthand to parse the date, if present."""
        if not date_string:
            return None
        date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)
