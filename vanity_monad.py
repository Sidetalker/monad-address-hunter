#!/usr/bin/env python3
"""
Vanity address hunter for Monad-compatible EVM addresses.
Generates random private keys until an address matches any provided prefix.
"""

import argparse
import secrets
import sys
from typing import Iterable, List, Sequence, Tuple

from eth_keys import keys


def normalize_prefix(prefix: str) -> str:
    cleaned = prefix.strip().lower()
    if not cleaned:
        raise ValueError("Empty prefix provided")
    if not cleaned.startswith("0x"):
        cleaned = "0x" + cleaned
    return cleaned


def normalize_prefixes(prefixes: Iterable[str]) -> List[str]:
    normalized = []
    for raw in prefixes:
        normalized.append(normalize_prefix(raw))
    if not normalized:
        raise ValueError("At least one prefix is required")
    return normalized


def generate_wallet() -> Tuple[keys.PrivateKey, str]:
    private_key = keys.PrivateKey(secrets.token_bytes(32))
    address = private_key.public_key.to_address().lower()
    return private_key, address


def find_vanity_match(
    prefixes: Sequence[str],
    log_interval: int = 1_000,
    max_attempts: int | None = None,
) -> Tuple[int, keys.PrivateKey, str, str]:
    attempts = 0
    target_prefixes = tuple(prefixes)

    while True:
        attempts += 1
        private_key, address = generate_wallet()

        for prefix in target_prefixes:
            if address.startswith(prefix):
                return attempts, private_key, address, prefix

        if attempts % log_interval == 0:
            print(f"Tested {attempts} seeds...", flush=True)

        if max_attempts is not None and attempts >= max_attempts:
            raise RuntimeError(
                f"Reached max attempts ({max_attempts}) without finding a match"
            )


def format_result(attempts: int, address: str, private_key: keys.PrivateKey, prefix: str) -> str:
    return (
        f"\nMatch found after {attempts} attempts!\n"
        f"Target prefix: {prefix}\n"
        f"Address:      {address}\n"
        f"Private key:  0x{private_key.to_bytes().hex()}\n"
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Brute-force Monad EVM vanity addresses until a prefix matches",
    )
    parser.add_argument(
        "prefixes",
        nargs="+",
        help="One or more desired hexadecimal prefixes (with or without 0x)",
    )
    parser.add_argument(
        "--log-interval",
        type=int,
        default=1_000,
        help="How many attempts between progress updates (default: 1000)",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        help="Optional limit for attempts to help with testing",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])

    try:
        prefixes = normalize_prefixes(args.prefixes)
    except ValueError as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1

    print("Starting vanity search...")
    print("Target prefixes: " + ", ".join(prefixes))

    try:
        attempts, private_key, address, matched_prefix = find_vanity_match(
            prefixes, log_interval=args.log_interval, max_attempts=args.max_attempts
        )
    except RuntimeError as exc:
        sys.stderr.write(f"{exc}\n")
        return 2

    print(format_result(attempts, address, private_key, matched_prefix))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
