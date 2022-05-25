from dataclasses import dataclass
from enum import Enum
from typing import Optional
from unicodedata import name

import serde  # pyserde


class ItemType(Enum):
    LOGIN = 1
    IDENTITY = 4


@serde.serde
@dataclass
class UriEntry:
    uri: Optional[str]


@serde.serde
@dataclass
class Login:
    uris: Optional[list[UriEntry]]
    username: Optional[str]
    password: Optional[str]
    totp: Optional[str]


@serde.serde
@dataclass
class Identity:
    title: Optional[str]
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    address_1: Optional[str]
    address_2: Optional[str]
    address_3: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    company: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    ssn: Optional[str]
    username: Optional[str]
    passportNumber: Optional[str]
    licenseNumber: Optional[str]


@serde.serde
@dataclass
class Field:
    name: Optional[str]
    value: Optional[str]



@serde.serde
@dataclass
class Item:
    id: str
    type: ItemType
    name: Optional[str]
    favorite: Optional[str]
    notes: Optional[str]
    login: Optional[Login]
    identity: Optional[Identity]
    fields: Optional[list[Field]]

    def __lt__(self, other):
        if not(bool(self.favorite) ^ bool(other.favorite)):
            return self.name.lower() < other.name.lower()
        elif self.favorite:
            return True
        return False


@serde.serde
@dataclass
class Bitwarden:
    encrypted: bool
    items: list[Item]
