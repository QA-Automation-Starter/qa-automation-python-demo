from typing import Any

from python_selenium.utils.exception_utils import *


def should_swallow_exception():
    def trouble(p: Any) -> str:
        raise Exception("trouble")

    assert safely(lambda: trouble(7)).value_or("nada") == "nada"
