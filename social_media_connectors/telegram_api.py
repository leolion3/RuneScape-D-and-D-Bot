#!/usr/bin/env python3
from typing import Dict, Any, Optional, List
from social_media_connectors.AbstractSocialMediaAdapter import AbstractSocialMediaAdapter
from logging_framework.log_handler import log, Module

import requests
import config


class TelegramAPI(AbstractSocialMediaAdapter):
    """
    Handles telegram API calls.
    """

    def _delete_messages(self, messages: List[int]) -> None:
        for msg_id in messages:
            r = requests.post(self._telegram_delete_url, data={
                "chat_id": self._chat_id,
                "message_id": msg_id
            })
            if r.status_code != 200:
                log.error("Failed to delete Telegram message:", r.text, module=Module.TEL)

    def _check_and_delete_previous(self, delete_previous_key: Optional[str], new_message_id: int) -> None:
        if delete_previous_key is None:
            return
        val = self._deletable_message_dict.get(delete_previous_key, None)
        if val is not None:
            self._delete_messages(val)
        self._deletable_message_dict[delete_previous_key] = [new_message_id]

    def notify(
            self,
            message: str,
            flags: Dict[str, Any],
            delete_previous_key: Optional[str] = None
    ) -> None:
        """
        Send the given message to telegram.
        :param message: the message to send.
        :param flags: optional flags containing attachments.
        :param delete_previous_key: optional key name for deleting previously sent message. Key name = event type.
        :return:
        """
        if not ('image' in flags.keys() and flags['image']):
            r = requests.get(self._telegram_chat_url + message)
        else:
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
            return
        response_json = r.json()
        if not response_json.get("ok"):
            return
        msg_id = response_json.get("result", {}).get("message_id", None)
        if msg_id is None:
            log.error('Message id not found.', module=Module.TEL)
            return
        self._check_and_delete_previous(delete_previous_key=delete_previous_key, new_message_id=msg_id)

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
        self._telegram_delete_url: str = f"https://api.telegram.org/bot{self._api_key}/deleteMessage"
        self._deletable_message_dict: Dict[str, List[int]] = {}


api: TelegramAPI = TelegramAPI()
