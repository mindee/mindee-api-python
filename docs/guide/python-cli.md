## Command Line Usage
The CLI tool is provided mainly for quick tests and debugging.

### General help

```shell
python3 -m mindee --help
```

### Example command help

```shell
python3 -m mindee invoice parse --help
```

### Example parse command for Off-the-Shelf document

```shell
python3 -m mindee invoice parse --key xxxxxxx /path/to/invoice.pdf
```

### Example enqueue command for Off-the-Shelf document (async)

```shell
python3 -m mindee invoice-splitter enqueue --key xxxxxxx /path/to/invoice-splitter.pdf
```

### Example parse-queued command for Off-the-Shelf document (async)

```shell
python3 -m mindee invoice-splitter parse-queued --key xxxxxxx id-of-the-job
```

### Works with environment variables

```shell
export MINDEE_API_KEY=xxxxxx
python3 -m mindee invoice parse /path/to/invoice.pdf
```

### Example parse command for a custom document

```shell
python3 -m mindee custom -u pikachu -k xxxxxxx pokemon_card /path/to/card.jpg
```

### Printing the raw parsed data instead of the summary

```shell
python3 -m mindee invoice parse -o parsed /path/to/invoice.pdf
```

### Extracting all the words using OCR

```shell
python3 -m mindee invoice parse -t /path/to/invoice.pdf
```

### In the Git repo, there's a helper script for it

```shell
./mindee-cli.sh -h
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
