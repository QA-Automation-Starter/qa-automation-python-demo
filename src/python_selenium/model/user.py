from attr import dataclass

from python_selenium.model.credentials import Credentials


@dataclass
class User:
    credentials: Credentials
    name: str
