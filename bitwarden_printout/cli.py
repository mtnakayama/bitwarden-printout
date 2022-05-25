from pathlib import Path

from . import convert


def cli(args: list[str]):
    _, bitwarden_json, output = args
    bitwarden_json_path = Path(bitwarden_json)
    output_path = Path(output)

    convert.convert(bitwarden_json_path, output_path)
