# SPDX-FileCopyrightText: 2025 Adrian Herscu
#
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass

from python_selenium.model.credentials import Credentials


@dataclass
class TerminalXCredentials(Credentials):
    pass
