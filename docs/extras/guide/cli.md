## Command Line Usage

The CLI tool is provided mainly for quick tests and debugging.

### General help

```shell
python3 -m mindee --help
```

### Example command help

```shell
python3 -m mindee parse --help
```

### Example parse command for Off-the-Shelf document

```shell
python3 -m mindee parse invoice --key xxxxxxx /path/to/invoice.pdf
```

### Works with environment variables

```shell
export MINDEE_API_KEY=xxxxxx
python3 -m mindee parse invoice /path/to/invoice.pdf
```

### Example parse command for a custom document

```shell
python3 -m mindee parse custom -a pikachu -k xxxxxxx pokemon_card /path/to/card.jpg
```

### Example async parse command

```shell
python3 -m mindee parse invoice-splitter 
```


### Full parsed output

```shell
python3 -m mindee invoice -o parsed /path/to/invoice.pdf
```

### Running the script through shell

A helper script allows you to start the command directly:

```shell
./mindee-cli.sh -h
```


**Questions?**  
<img alt="Slack Logo Icon" style="display:inline!important" src="https://files.readme.io/5b83947-Slack.png" width="20" height="20">  [Join our Slack](https://join.slack.com/t/mindee-community/shared_invite/zt-1jv6nawjq-FDgFcF2T5CmMmRpl9LLptw)
