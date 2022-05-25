import dataclasses

import dominate
from dominate.util import text, raw
from dominate.tags import (div, h1, h2, h3, link, style)

from .bitwarden_schema import Bitwarden, Field, Identity, Login


def to_html(bitwarden: Bitwarden):

    doc = dominate.document(title='Dominate your HTML')

    with doc.head:
        link(
            rel="stylesheet",
            href='https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'  # noqa
        )
        style(raw(r"""
@media print {
  .item {
    break-inside: avoid;
  }
}
html {
    font-family: "Source Code Pro", "Consolas", "Courier New", monospace;
}
body {
    margin: 0 auto;
    width: 6.5in;
}
h3 {
    font-size: 10pt;
    margin: 1em 0 0 0;
}
h3::after {
    content: ": ";
}
.notes-text {
    white-space: pre;
}
.inline-title {
    display: inline;
}
.inline-title:not(:first-of-type)::before {
    content: "\A";
    white-space: pre;
}
.user-text {
    font-size: 10pt;
    overflow-wrap: break-word;
}
"""))

    with doc:
        h1("Bitwarden Backup Keys")
        with div(cls='items'):
            for item in bitwarden.items:
                with div(cls='item user-text'):
                    name = item.name if item.name else item.id
                    h2(name)
                    if item.login:
                        add_login_html(item.login)
                    if item.identity:
                        add_identity_html(item.identity)
                    if item.fields:
                        add_fields_html(item.fields)
                    if item.notes:
                        h3('Notes')
                        div(item.notes, cls='notes-text')

    return doc


def add_login_html(login: Login):
    for key in ['username', 'password', 'totp']:
        value = getattr(login, key)
        if value:
            add_key_value(format_key_name(key), value)


def add_identity_html(identity: Identity):
    for key, value in dataclasses.asdict(identity).items():
        if value:
            add_key_value(format_key_name(key), value)


def add_fields_html(fields: list[Field]):
    for field in fields:
        name = field.name if field.name else ''
        value = field.value if field.value else ''
        add_key_value(name, value)


def add_key_value(key: str, value: str):
    h3(f'{key}', cls='inline-title')
    text(value)


def format_key_name(key: str) -> str:
    """Format a key to be human readable."""
    if key == 'ssn':
        return 'SSN'
    return key.replace('_', ' ').capitalize()
