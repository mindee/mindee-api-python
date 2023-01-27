## Command Line Usage
The CLI tool is provided mainly for quick tests and debugging.

### General help

```shell
python3 -m mindee --help
```

### Example command help

```shell
python3 -m mindee invoice --help
```

### Example parse command for Off-the-Shelf document

```shell
python3 -m mindee invoice --invoice-key xxxxxxx /path/to/invoice.pdf
```

### Works with environment variables

```shell
export MINDEE_API_KEY=xxxxxx
python3 -m mindee invoice /path/to/invoice.pdf
```

### Example parse command for a custom document

```shell
python3 -m mindee custom -u pikachu -k xxxxxxx pokemon_card /path/to/card.jpg
```

### You can get the full parsed output as well

```shell
python3 -m mindee invoice -o parsed /path/to/invoice.pdf
```

### In the Git repo, there's a helper script for it

```shell
./mindee-cli.sh -h
```

## Questions?
[Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
