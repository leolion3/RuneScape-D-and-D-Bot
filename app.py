#!/usr/bin/env python3
from typing import Dict, List, Any

from apscheduler.schedulers.blocking import BlockingScheduler

from daily_dnds.abstract_daily_dnd import AbstractDailyDND
from daily_dnds.rune_goldberg import rune_goldberg
from hourly_dnds.abstract_hourly_dnd import AbstractHourlyDND
from hourly_dnds.wilderness_flash_events import wilderness_flash_events
from logging_framework.log_handler import log, Module
from social_media_connectors.AbstractSocialMediaAdapter import AbstractSocialMediaAdapter
from social_media_connectors.telegram_api import api as telegram_api

daily_events: Dict[str, AbstractDailyDND] = {
    'Rune Goldberg': rune_goldberg.RuneGoldberg()
}

hourly_events: Dict[str, AbstractHourlyDND] = {
    'Wilderness Flash Events': wilderness_flash_events.WildernessFlashEvents()
}

social_media_adapters: List[AbstractSocialMediaAdapter] = [
    telegram_api
]


def _check_flags_and_notify(event_name: str, message: str, flags: Dict[str, Any]):
    if message is None or not len(message.strip()):
        log.info(f'Event {event_name} did not return a notification. Skipping.', module=Module.MAIN)
        return
    for adapter in social_media_adapters:
        adapter.notify(message=message, flags=flags, delete_previous_key=event_name)


def daily_schedule() -> None:
    """
    Fetches daily D&Ds.
    :return:
    """
    global daily_events
    for event_name, dnd in daily_events.items():
        try:
            log.info(f'Executing daily routine for event: {event_name}', module=Module.MAIN)
            message, flags = dnd.daily_exec()
            _check_flags_and_notify(event_name, message, flags)
        except Exception as e:
            log.error(f'Error executing daily schedule for event {event_name}. Trace: {e}', module=Module.MAIN)


def hourly_schedule() -> None:
    """
    Fetches hourly D&Ds.
    :return:
    """
    global hourly_events
    for event_name, dnd in hourly_events.items():
        try:
            log.info(f'Executing hourly routine for event: {event_name}', module=Module.MAIN)
            message, flags = dnd.hourly_exec()
            _check_flags_and_notify(event_name, message, flags)
        except Exception as e:
            log.error(f'Error executing hourly schedule for event {event_name}. Trace: {e}', module=Module.MAIN)


def exec_test_run() -> None:
    log.info('Executing daily schedule test...', module=Module.MAIN)
    daily_schedule()
    log.info('Executing hourly schedule test...', module=Module.MAIN)
    hourly_schedule()


if __name__ == '__main__':
    log.info('Starting application....', module=Module.MAIN)
    exec_test_run()
    log.info('Testrun finished, started scheduler...', module=Module.MAIN)
    scheduler = BlockingScheduler()
    # 6 AM to ensure community events have correct information.
    scheduler.add_job(daily_schedule, 'cron', hour=6, minute=0, id='daily-schedule')
    # 30 minutes to next hour.
    scheduler.add_job(hourly_schedule, 'cron', minute=30, id='hourly-schedule')
    scheduler.start()
