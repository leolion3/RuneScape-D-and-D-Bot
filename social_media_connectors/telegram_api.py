#!/usr/bin/env python3
from typing import Dict, Any, Optional
from social_media_connectors.AbstractSocialMediaAdapter import AbstractSocialMediaAdapter
from logging_framework.log_handler import log, Module

import requests
import config


class TelegramAPI(AbstractSocialMediaAdapter):
    """
    Handles telegram API calls.
    """

    def notify(self, message: str, flags: Dict[str, Any]) -> None:
        """
        Send the given message to telegram.
        :param message: the message to send.
        :param flags: optional flags containing attachments.
        :return:
        """
        if not ('image' in flags.keys() and flags['image']):
            requests.get(self._telegram_chat_url + message)
            return
        filepath: str = flags['filepath']
        image_data: Optional[bytes] = open(filepath, 'rb').read()
        files = {
            'photo': image_data
        }
        data = {
            'chat_id': self._chat_id,
            'caption': message
        }
        r = requests.post(self._telegram_attachment_url, files=files, data=data)
        if r.status_code != 200:
            log.error('Telegram API Error. Status code:', str(r.status_code), r.text, module=Module.TEL)

    def __init__(self):
        """
        Default constructor.
        :return:
        """
        self._api_key: str = config.telegram_api_key
        self._chat_id: str = config.telegram_chat_id
        self._telegram_attachment_url: str = f"https://api.telegram.org/bot{self._api_key}/sendPhoto"
        self._telegram_chat_url: str = (f"https://api.telegram.org/bot{self._api_key}/sendMessage"
                                        f"?chat_id={self._chat_id}&text=")


api: TelegramAPI = TelegramAPI()
