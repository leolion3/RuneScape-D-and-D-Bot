#!/usr/bin/env python3
from abc import ABC
from typing import Dict, Any, Optional


class AbstractSocialMediaAdapter(ABC):
    """
    Template for social media adapters.
    """

    def notify(self, message: str, flags: Dict[str, Any], delete_previous_key: Optional[str] = None) -> None:
        """
        Default public facing method, used to send D&D notifications.
        :param message: the message to send.
        :param flags: Dictionary with optional file attachments.
        :param delete_previous_key: optional key name for deleting previously sent message. Key name = event type.
        :return:
        """
        pass
