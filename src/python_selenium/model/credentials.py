from attr import dataclass


@dataclass
class Credentials:
    username: str
    password: str

    @classmethod
    def from_(cls, colon_separated: str):
        return cls(*colon_separated.split(":"))