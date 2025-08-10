#!/usr/bin/env python3
from abc import ABC
from typing import Dict, Any


class AbstractSocialMediaAdapter(ABC):
    """
    Template for social media adapters.
    """

    def notify(self, message: str, flags: Dict[str, Any]) -> None:
        """
        Default public facing method, used to send D&D notifications.
        :param message: the message to send.
        :param flags: Dictionary with optional file attachments.
        :return:
        """
        pass
