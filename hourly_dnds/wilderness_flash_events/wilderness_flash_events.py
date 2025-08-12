#!/usr/bin/env python3
import json
import os.path
from datetime import datetime, timedelta
from typing import Dict, Tuple, Any, Generator, Optional, List
from hourly_dnds.abstract_hourly_dnd import AbstractHourlyDND
from logging_framework.log_handler import log, Module

import config
import requests


class WildernessFlashEvents(AbstractHourlyDND):
    """
    Handles wilderness flash events.
    """

    config_file_path: str = os.path.join(os.path.dirname(__file__), "config.json")

    def hourly_exec(self) -> Tuple[str, Dict[str, Any]]:
        """
        Default public facing method.
        :return: a notification for the next wilderness flash event if it is on the favourite list.
        """
        html: str = self._base_request()
        flash_events: Dict[str, str] = self._get_events_dictionary(html)
        next_event, event_timestamp = self._get_next_event(flash_events)
        if self._favourites_only:
            if not self._is_favourite(next_event):
                log.debug(f'Next flash event is {next_event} '
                         f'but not on favourite list, skipping notification.', module=Module.FLASH_EVENTS)
                return '', {}
            else:
                log.debug(f'Next flash event is {next_event}, sending notification...',
                          module=Module.FLASH_EVENTS)
        return f'The next flash event is "{next_event}", starting at {event_timestamp}', {}

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
    def _base_request() -> str:
        """
        Base request to fetch upcoming events from rs wiki.
        :return: the html code.
        """
        url = 'https://runescape.wiki/w/Template:Wilderness_Flash_Events/rotations'
        return requests.get(url).text

    @staticmethod
    def _get_events_table(html: str) -> str:
        """
        Get the wilderness flash events table from the rs wiki.
        :param html: the wiki html code.
        :return: the html table's content as a string.
        """
        return html.split('<table')[1].split('</table')[0]

    @staticmethod
    def _get_table_rows(html_table: str) -> Generator[str]:
        rows = html_table.split('<tr')[:-2]
        for row in rows:
            yield row

    @staticmethod
    def _get_cell(table_row: str) -> Generator[str]:
        tds = table_row.split('<td')
        for td in tds:
            yield td

    @staticmethod
    def _is_event_name(td_txt: str) -> bool:
        return '</a>' in td_txt

    @staticmethod
    def _get_event_name_from_td(td_txt: str) -> str:
        return td_txt.split('</a>')[0].split('>')[2]

    @staticmethod
    def _is_event_time(td_txt: str) -> bool:
        return '<small>' in td_txt

    @staticmethod
    def _get_event_time_from_td(td_txt: str) -> str:
        return td_txt.split('<small>')[1].split('<')[0]

    @staticmethod
    def _append_event_if_valid(event: Optional[str], time: Optional[str], events: Dict[str, str]) -> None:
        if event is not None and time is not None:
            events[event] = time

    def _get_event_name_and_time(self, td_row: str) -> Tuple[str, str]:
        event = None
        time = None
        for td in self._get_cell(td_row):
            if self._is_event_name(td) and event is None:
                event = self._get_event_name_from_td(td)
                continue
            if self._is_event_time(td) and time is None:
                time = self._get_event_time_from_td(td)
            if event is not None and time is not None:
                break
        return event, time

    def _get_events_dictionary(self, html: str) -> Dict[str, str]:
        """
        Get a dictionary of upcoming wilderness flash events mapped to timestamps.
        :param html: the html code from the rs wiki.
        :return: a dictionary mapping of each event to its upcoming time.
        """
        events = {}
        table = self._get_events_table(html=html)
        for row in self._get_table_rows(table):
            event, time = self._get_event_name_and_time(row)
            self._append_event_if_valid(
                event=event,
                time=time,
                events=events
            )
        return events

    @staticmethod
    def _get_next_event(events: Dict[str, str]) -> Tuple[str, str]:
        """
        Gets the next wilderness flash event.
        :return: the name of the next wilderness flash event.
        """
        now: datetime = datetime.now()
        for event_name, event_timestamp in events.items():
            event_time = datetime.strptime(event_timestamp, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            if event_time < now:
                event_time += timedelta(days=1)
            if now <= event_time <= now + timedelta(hours=1):
                return event_name, event_timestamp
        log.error('Error fetching next flash event. No event found.', module=Module.FLASH_EVENTS)
        raise Exception('Could not fetch next wilderness flash event.')


if __name__ == '__main__':
    wilderness_flash = WildernessFlashEvents()
    print(wilderness_flash.hourly_exec())
