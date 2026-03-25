from mindee.v2.commands.cli_parser import MindeeParser


def main() -> None:
    """Run the Command Line Interface."""
    parser = MindeeParser()
    parser.call_parse()


if __name__ == "__main__":
    main()
