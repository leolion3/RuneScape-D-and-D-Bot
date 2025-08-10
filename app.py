#!/usr/bin/env python3
from typing import Dict, List

from apscheduler.schedulers.blocking import BlockingScheduler

from daily_dnds.abstract_daily_dnd import AbstractDailyDND
from daily_dnds.rune_goldberg import rune_goldberg
from logging_framework.log_handler import log, Module
from social_media_connectors.AbstractSocialMediaAdapter import AbstractSocialMediaAdapter
from social_media_connectors.telegram_api import api as telegram_api

daily_events: Dict[str, AbstractDailyDND] = {
    'Rune Goldberg': rune_goldberg.RuneGoldberg()
}

social_media_adapters: List[AbstractSocialMediaAdapter] = [
    telegram_api
]


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
            for adapter in social_media_adapters:
                adapter.notify(message=message, flags=flags)
        except Exception as e:
            log.error(f'Error executing daily schedule for event {event_name}. Trace: {e}', module=Module.MAIN)


def hourly_schedule() -> None:
    pass


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
    scheduler.add_job(daily_schedule, 'cron', hour=3, minute=0, id='daily-schedule')
    scheduler.add_job(hourly_schedule, 'cron', minute=5, id='hourly-schedule')
    scheduler.start()
