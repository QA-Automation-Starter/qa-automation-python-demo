from dataclasses import dataclass

from python_selenium.model.examples.terminalx_credentials import TerminalXCredentials


@dataclass
class TerminalXUser:
    credentials: TerminalXCredentials
    name: str
