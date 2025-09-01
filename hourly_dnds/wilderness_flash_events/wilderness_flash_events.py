#!/usr/bin/env python3
import time
import json
import os.path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Dict, Tuple, Any, Optional, List
from hourly_dnds.abstract_hourly_dnd import AbstractHourlyDND
from logging_framework.log_handler import log, Module

import config
import requests


class WildernessFlashEvents(AbstractHourlyDND):
    """
    Handles wilderness flash events.
    """

    config_file_path: str = os.path.join(os.path.dirname(__file__), "config.json")

    START_EPOCH_MS: int = 1754542800000
    FULL_PERIOD_HOURS: int = 14
    ITEM_PERIOD_HOURS: int = 1

    ROTATION: List[str] = [
        "Spider Swarm",
        "Unnatural Outcrop",
        "Stryke the Wyrm",
        "Demon Stragglers",
        "Butterfly Swarm",
        "King Black Dragon Rampage",
        "Forgotten Soldiers",
        "Surprising Seedlings",
        "Hellhound Pack",
        "Infernal Star",
        "Lost Souls",
        "Ramokee Incursion",
        "Displaced Energy",
        "Evil Bloodwood Tree",
    ]

    def _get_events_dictionary(self) -> Dict[str, str]:
        """
        Build rotation from the fixed start timestamp.
        Returns a dictionary of event → next occurrence (UTC, %H:%M).
        """
        events: Dict[str, str] = {}

        start_time = datetime.fromtimestamp(self.START_EPOCH_MS / 1000, tz=timezone.utc)
        now = datetime.now(timezone.utc)

        for i, name in enumerate(self.ROTATION):
            # time of this event in the very first cycle
            event_time = start_time + timedelta(hours=i * self.ITEM_PERIOD_HOURS)

            # compute how many full cycles have passed since anchor
            elapsed = now - event_time
            cycles = int(elapsed.total_seconds() // (self.FULL_PERIOD_HOURS * 3600))
            if elapsed.total_seconds() % (self.FULL_PERIOD_HOURS * 3600) != 0:
                cycles += 1

            # roll forward to the next occurrence
            next_time = event_time + timedelta(hours=cycles * self.FULL_PERIOD_HOURS)
            events[name] = next_time.strftime("%H:%M")

        return events

    @staticmethod
    def _get_next_event(events: Dict[str, str]) -> Tuple[str, str]:
        """
        Get the next wilderness flash event.
        """
        now = datetime.now(timezone.utc)
        for event_name, event_timestamp in events.items():
            event_time = datetime.strptime(event_timestamp, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day, tzinfo=timezone.utc
            )
            if event_time < now:
                event_time += timedelta(days=1)
            if now <= event_time <= now + timedelta(hours=1):
                return event_name, event_timestamp
        raise Exception("Could not fetch next wilderness flash event.")

    def print_all_events(self) -> None:
        """
        Print all upcoming events in human-readable format (UTC).
        """
        events = self._get_events_dictionary()
        print("Upcoming Wilderness Flash Events (UTC):")
        for name, ts in events.items():
            print(f"- {name}: {ts.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    def hourly_exec(self) -> Tuple[str, Dict[str, Any]]:
        """
        Default public facing method.
        :return: a notification for the next wilderness flash event if it is on the favourite list.
        """
        flash_events: Dict[str, str] = self._get_events_dictionary()
        log.debug(
            'Event schedule:', flash_events,
            '| Current time:', datetime.now(tz=timezone.utc).strftime("%m/%d/%Y %H:%M:%S"),
            module=Module.FLASH_EVENTS
        )

        next_event, event_timestamp = self._get_next_event(flash_events)
        if self._favourites_only:
            if not self._is_favourite(next_event):
                log.debug(f'Next flash event is {next_event} '
                          f'but not on favourite list, skipping notification.', module=Module.FLASH_EVENTS)
                return '', {}
            else:
                log.debug(f'Next flash event is {next_event}, sending notification...',
                          module=Module.FLASH_EVENTS)

        # --- compute accurate countdown ---
        now_utc = datetime.now(tz=timezone.utc)
        cet = ZoneInfo("Europe/Berlin")
        event_time_utc = datetime.strptime(event_timestamp, "%H:%M").replace(
            year=now_utc.year, month=now_utc.month, day=now_utc.day, tzinfo=timezone.utc
        )
        if event_time_utc < now_utc:
            event_time_utc += timedelta(days=1)

        event_time_cet = event_time_utc.astimezone(cet)
        now_cet = now_utc.astimezone(cet)
        delta_minutes = int((event_time_cet - now_cet).total_seconds() // 60)
        log.debug(
            f'Next flash event is {next_event}, sending notification in {delta_minutes} minutes...',
            module=Module.FLASH_EVENTS
        )
        return f'The next flash event is "{next_event}", starting in {delta_minutes} minutes at {event_time_cet.strftime("%H:%M")} CET', {}

    def _is_favourite(self, event_name: str) -> bool:
        """
        Check if the given event is on the favourite list.
        :param event_name: the event to check.
        :return: true if the event is on the favourite list, false otherwise.
        """
        return event_name.lower() in self._favourites

    def _load_config_file(self) -> List[str]:
        """
        Load the config file if favourite events are enabled.
        :return: a list of favourite events.
        """
        try:
            json_data: Dict[str, Any] = json.load(open(self.config_file_path, "r", encoding="utf-8"))
            events: List[str] = json_data.get('favourite_events', [])
            log.debug('Loaded wilderness flash favourites:', events, module=Module.FLASH_EVENTS)
            return [e.lower() for e in events]
        except Exception as e:
            log.error('Error loading favourite events from config file. Disabling favourites.',
                      module=Module.FLASH_EVENTS)
            log.error('Trace:', e, module=Module.FLASH_EVENTS)
            self._favourites_only = False
        return []

    def __init__(self):
        """
        Default constructor.
        """
        self._favourites_only: bool = config.wilderness_flash_events_favourites_only
        if self._favourites_only:
            self._favourites: List[str] = self._load_config_file()

    @staticmethod
    def _append_event_if_valid(event: Optional[str], _time: Optional[str], events: Dict[str, str]) -> None:
        if event is not None and _time is not None:
            events[event] = _time


if __name__ == '__main__':
    wilderness_flash = WildernessFlashEvents()
    print(wilderness_flash.hourly_exec())
