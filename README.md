# Monad Vanity Address Hunter

A small terminal tool that brute-forces Monad-compatible EVM addresses until one of the requested prefixes is found.

## Setup

Install dependencies (Python 3.10+ recommended):

```bash
pip install -r requirements.txt
```

## Usage

Run the script with one or more hexadecimal prefixes (with or without the `0x` prefix). The search stops as soon as any prefix matches.

```bash
python vanity_monad.py 0xmon 0x1bad
```

Optional flags:

- `--log-interval`: number of attempts between progress messages (default: 1000)
- `--max-attempts`: optional cap useful for testing

Example output:

```
Starting vanity search...
Target prefixes: 0xmon, 0x1bad
Tested 1000 seeds...
...
Match found after 5322 attempts!
Target prefix: 0xmon
Address:      0xmon...
Private key:  0x<private-key-hex>
```

Keep the tool offline when hunting real wallets and store any private keys securely.
