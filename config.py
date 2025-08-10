#!/usr/bin/env python3
import os
from typing import Optional
from logging_framework.log_handler import log, Module

import dotenv

dotenv.load_dotenv()

# See https://googlechromelabs.github.io/chrome-for-testing
chromium_executable_path: str = os.getenv('CHROMIUM_EXECUTABLE_PATH', './chrome-win32/chrome.exe')
# Html2Image requires a temp path in linux with rw permissions, so use /tmp
linux_tmp_path_hti: bool = True

if os.name == "nt":
    linux_tmp_path_hti = False

telegram_api_key: Optional[str] = None
telegram_chat_id: Optional[str] = None
telegram_enabled = os.getenv('TELEGRAM_ENABLED', 'false').lower() == 'true'
if telegram_enabled:
    telegram_api_key = os.getenv('TELEGRAM_API_KEY')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not len(telegram_api_key) or not len(telegram_chat_id):
        log.error('Telegram API Key and Chat ID are required if telegram is enabled. Disabling telegram api.')
        telegram_enabled = False
