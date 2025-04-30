from dataclasses import dataclass

from python_selenium.model.examples.terminalx_credentials import TerminalXCredentials


@dataclass(frozen=True)
class TerminalXUser:
    credentials: TerminalXCredentials
    name: str
