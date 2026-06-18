import pytest

from mindee.v2.commands import (
    BaseInferenceCommand,
    ClassificationCommand,
    CropCommand,
    ExtractionCommand,
    MindeeArgumentParser,
    MindeeParser,
    OcrCommand,
    OutputType,
    SplitCommand,
)
from tests.utils import V2_PRODUCT_DATA_DIR, clear_envvars


@pytest.fixture
def parser() -> MindeeParser:
    """Build a fully wired MindeeParser without parsing args yet."""
    p = MindeeParser.__new__(MindeeParser)
    p.parser = MindeeArgumentParser(description="Mindee_API")
    from mindee.v2.commands.cli_parser import (
        _build_inference_commands,
        _default_client_factory,
    )
    from mindee.v2.commands.search_models_command import (
        SearchModelsCommand,
    )

    p._inference_commands = {cmd.name: cmd for cmd in _build_inference_commands()}
    p._search_models_command = SearchModelsCommand()
    p._client_factory = _default_client_factory
    p._build_parser()
    return p


def test_top_level_subcommands_registered(parser: MindeeParser):
    """All V2 inference subcommands + search-models + v1 are reachable."""
    expected = {
        "classification",
        "crop",
        "extraction",
        "ocr",
        "split",
        "search-models",
        "v1",
    }
    actions = [a for a in parser.parser._actions if a.dest == "cmd"]
    assert actions, "cmd subparsers action missing"
    assert expected.issubset(set(actions[0].choices.keys()))


def test_extraction_command_exposes_full_flag_set(parser: MindeeParser):
    """Extraction must expose --rag, --raw-text, --confidence, --polygon, --text-context."""
    ns = parser.parser.parse_args(
        [
            "extraction",
            "--api-key",
            "dummy",
            "--model-id",
            "model-1",
            "--alias",
            "my-alias",
            "--rag",
            "--raw-text",
            "--confidence",
            "--polygon",
            "--text-context",
            "ctx",
            "--output",
            "full",
            "path/to/file.pdf",
        ]
    )
    assert ns.cmd == "extraction"
    assert ns.api_key == "dummy"
    assert ns.model_id == "model-1"
    assert ns.alias == "my-alias"
    assert ns.rag is True
    assert ns.raw_text is True
    assert ns.confidence is True
    assert ns.polygon is True
    assert ns.text_context == "ctx"
    assert ns.output == OutputType.FULL.value
    assert ns.path == "path/to/file.pdf"


def test_extraction_short_flags(parser: MindeeParser):
    """Extraction must accept the short form of every documented flag."""
    ns = parser.parser.parse_args(
        [
            "extraction",
            "-k",
            "dummy",
            "-m",
            "model-1",
            "-a",
            "alias",
            "-g",
            "-r",
            "-c",
            "-p",
            "-t",
            "ctx",
            "-o",
            "raw",
            "path/to/file.pdf",
        ]
    )
    assert ns.rag is True
    assert ns.raw_text is True
    assert ns.confidence is True
    assert ns.polygon is True
    assert ns.text_context == "ctx"
    assert ns.output == OutputType.RAW.value


@pytest.mark.parametrize(
    "command",
    ["classification", "crop", "ocr", "split"],
)
def test_non_extraction_commands_omit_extraction_only_flags(
    parser: MindeeParser, command: str
):
    """Non-extraction commands must reject --rag/--raw-text/--confidence/--polygon/--text-context."""
    with pytest.raises(SystemExit):
        parser.parser.parse_args(
            [command, "--model-id", "x", "--rag", "path/to/file.pdf"]
        )


def test_search_models_flags(parser: MindeeParser):
    ns = parser.parser.parse_args(
        [
            "search-models",
            "--api-key",
            "dummy",
            "--name",
            "invoice",
            "--model-type",
            "extraction",
            "--raw-json",
        ]
    )
    assert ns.cmd == "search-models"
    assert ns.api_key == "dummy"
    assert ns.name == "invoice"
    assert ns.model_type == "extraction"
    assert ns.raw_json is True


def test_search_models_rejects_invalid_model_type(parser: MindeeParser):
    with pytest.raises(SystemExit):
        parser.parser.parse_args(["search-models", "--model-type", "nope"])


def test_v1_group_dispatches_to_v1_product(parser: MindeeParser):
    """The `v1` group preserves the existing V1 product subcommand shape."""
    ns = parser.parser.parse_args(
        [
            "v1",
            "invoice",
            "--key",
            "dummy",
            "--output-type",
            "summary",
            str(
                V2_PRODUCT_DATA_DIR
                / "extraction"
                / "financial_document"
                / "complete.json"
            ),
        ]
    )
    assert ns.cmd == "v1"
    assert ns.product_name == "invoice"
    assert ns.api_key == "dummy"
    assert ns.output_type == "summary"


def test_extraction_dispatches_to_inference_command(monkeypatch, parser: MindeeParser):
    """call_parse delegates to the InferenceCommand.execute for V2 product cmds."""
    captured = {}

    def fake_execute(args, factory):
        captured["cmd"] = "extraction"
        captured["model_id"] = args.model_id
        return 0

    monkeypatch.setattr(
        parser._inference_commands["extraction"], "execute", fake_execute
    )
    parser.parsed_args = parser.parser.parse_args(
        ["extraction", "-k", "x", "-m", "m1", "some/path.pdf"]
    )
    parser.call_parse()
    assert captured == {"cmd": "extraction", "model_id": "m1"}


def test_search_models_dispatches_to_search_command(monkeypatch, parser: MindeeParser):
    captured = {}

    def fake_execute(args, factory):
        captured["name"] = args.name
        captured["model_type"] = args.model_type
        return 0

    monkeypatch.setattr(parser._search_models_command, "execute", fake_execute)
    parser.parsed_args = parser.parser.parse_args(
        ["search-models", "-n", "inv", "-m", "extraction"]
    )
    parser.call_parse()
    assert captured == {"name": "inv", "model_type": "extraction"}


def test_v1_group_delegates_to_v1_mindee_parser(monkeypatch, parser: MindeeParser):
    """`v1` command instantiates the V1 MindeeParser with the parsed args."""
    seen = {}

    class _FakeV1Parser:
        def __init__(self, parsed_args):
            seen["args"] = parsed_args

        def call_parse(self):
            seen["called"] = True

    monkeypatch.setattr(
        "mindee.v2.commands.cli_parser.V1MindeeParser",
        _FakeV1Parser,
        raising=True,
    )
    clear_envvars(monkeypatch)
    parser.parsed_args = parser.parser.parse_args(
        ["v1", "invoice", "--key", "dummy", "path/to/file.pdf"]
    )
    parser.call_parse()
    assert seen["called"] is True
    assert seen["args"].product_name == "invoice"
    assert seen["args"].api_key == "dummy"


def test_each_inference_command_is_self_contained(parser: MindeeParser):
    """Every V2 inference command is its own subclass of BaseInferenceCommand.

    Locks in the per-product class architecture: the dispatcher must hold
    distinct ``BaseInferenceCommand`` instances rather than a single
    config-driven command, so future products that don't fit the
    document-extraction shape can simply not extend this base.
    """
    expected = {
        "classification": ClassificationCommand,
        "crop": CropCommand,
        "extraction": ExtractionCommand,
        "ocr": OcrCommand,
        "split": SplitCommand,
    }
    for name, cls in expected.items():
        cmd = parser._inference_commands[name]
        assert isinstance(cmd, BaseInferenceCommand)
        assert isinstance(cmd, cls)
        assert cmd.name == name
