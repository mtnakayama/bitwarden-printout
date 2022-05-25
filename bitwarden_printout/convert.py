from pathlib import Path
import json

import serde  # pyserde

from .bitwarden_schema import Bitwarden
from . import html


def convert(bitwarden_json_path: Path, output_path: Path):
    with open(bitwarden_json_path, 'r') as bitwarden_json_file:
        bitwarden_json = json.load(bitwarden_json_file)

    bitwarden = serde.from_dict(Bitwarden, bitwarden_json)
    bitwarden.items.sort()

    # plain_text(bitwarden)
    html_doc = html.to_html(bitwarden)
    print(html_doc)

    with open(output_path, 'w', encoding='utf-8') as output:
        output.write(str(html_doc))


def plain_text(bitwarden: Bitwarden):
    for item in bitwarden.items:
        print(item.name)
        if item.login:
            if item.login.username:
                print("Username:", item.login.username)
            if item.login.password:
                print("Password:", item.login.password)
