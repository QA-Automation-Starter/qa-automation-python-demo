from attr import dataclass


@dataclass
class Credentials:
    username: str
    password: str
