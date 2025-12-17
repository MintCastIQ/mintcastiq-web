#!/usr/bin/env python3
import argparse
import hashlib
import os
from mintcastiq.serializers import serialize_for_hash

def hash_string(input_string: str, algorithm: str = "sha256") -> str:
    """Return the hash of the input string using the chosen algorithm."""
    h = hashlib.new(algorithm)
    h.update(input_string.encode("utf-8"))
    return h.hexdigest()

def hash_file(filepath: str, algorithm: str = "sha256") -> str:
    """Return the hash of the file contents using the chosen algorithm."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_object(instance) -> str:
    """
    Generate a stable hash string for a Django model instance.
    Uses the serialize_for_hash function to get a JSON representation.
    """
    json_str = serialize_for_hash(instance)
    print("HASH PAYLOAD:", json_str)
    return hashlib.sha256(json_str.encode("utf-8")).hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Hash a string or file contents.")
    parser.add_argument("input", help="String or filename to hash")
    parser.add_argument(
        "-a", "--algorithm",
        default="sha256",
        help="Hash algorithm (default: sha256). Options include md5, sha1, sha256, sha512, etc."
    )
    parser.add_argument(
        "-f", "--file",
        action="store_true",
        help="Treat input as a filename and hash its contents"
    )
    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.input):
            print(f"File not found: {args.input}")
            return
        result = hash_file(args.input, args.algorithm)
        print(f"{args.algorithm} hash of file '{args.input}': {result}")
    else:
        result = hash_string(args.input, args.algorithm)
        print(f"{args.algorithm} hash of string '{args.input}': {result}")

if __name__ == "__main__":
    main()
