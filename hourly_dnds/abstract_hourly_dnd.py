#!/usr/bin/env python3
from abc import ABC
from typing import Dict, Any, Tuple


class AbstractHourlyDND(ABC):
    """
    Abstract hourly DND class.
    """

    def hourly_exec(self) -> Tuple[str, Dict[str, Any]]:
        """
        Default public facing method.
        :return: a string response for telegram/discord along with flags containing attachment files.
        Example of the dict: {"image": true, "filepath": "/tmp/generated.png"}
        """
        pass
