from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator
from uuid import uuid4

from requests import Response

from python_selenium.utils.string_utils import to_string


@dataclass
@to_string()
class SwaggerPetstorePet:
    name: str
    status: str

    @staticmethod
    def random() -> SwaggerPetstorePet:
        return SwaggerPetstorePet(name=str(uuid4()), status="available")

    @staticmethod
    def from_(response: Response) -> Iterator[SwaggerPetstorePet]:
        return (SwaggerPetstorePet(**pet) for pet in response.json())
