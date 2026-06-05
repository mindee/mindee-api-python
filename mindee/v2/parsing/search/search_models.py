from mindee.v2.parsing.search.search_model import SearchModel


class SearchModels(list[SearchModel]):
    """List of models."""

    def __init__(self, raw_response: list[dict]) -> None:
        super().__init__([SearchModel(model) for model in raw_response])

    def __str__(self) -> str:
        """
        Default string representation.
        """
        if len(self) == 0:
            return "\n"

        lines = []
        for model in self:
            lines.append(f"* :Name: {model.name}")
            lines.append(f"  :ID: {model.id}")
            lines.append(f"  :Model Type: {model.model_type}")
            lines.append(f"  :Webhooks: {len(model.webhooks)}")

        return "\n".join(lines) + "\n"
