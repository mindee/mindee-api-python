from enum import Enum


class ExecutionPriority(Enum):
    """Available priorities for workflow executions."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
