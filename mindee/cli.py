from mindee.commands.cli_parser import MindeeParser


def main() -> None:
    """Run the Command Line Interface."""
    parser = MindeeParser()
    parser.call_endpoint()
