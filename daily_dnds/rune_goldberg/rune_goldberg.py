#!/usr/bin/env python3
import os
import base64
import uuid

import requests
from PIL import Image
from typing import List, Tuple, Any, Dict
from html2image import Html2Image

import config
from logging_framework.log_handler import log, Module
from daily_dnds.abstract_daily_dnd import AbstractDailyDND

_generated_filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generated.png')
_runes_filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'runes')
_html_filepath: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')


class RuneGoldberg(AbstractDailyDND):
    """
    Fetch the daily rune goldberg rune combinations.
    """

    @staticmethod
    def _get_base() -> str:
        """
        Make a request to warbandtracker to get the daily runes combinations.
        :return: the html response.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 OPR/120.0.0.0'
        }
        url = 'https://warbandtracker.com/goldberg'
        return requests.get(url, headers=headers).text

    @staticmethod
    def _get_html_table(html: str) -> str:
        """
        Generates the html for the  rune combination table.
        :param html: the html from the rune goldberg tracker website.
        :return: the html template with the runes in place.
        """
        global _runes_filepath, _html_filepath
        splitter: str = '<h2>Correct Rune Combinations</h2>'
        table: str = html.split(splitter)[1].split('</div>')[0]
        for rune in os.listdir(_runes_filepath):
            if rune in table:
                with open(os.path.join(_runes_filepath, rune), 'rb') as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode('utf-8')
                table = table.replace(f'runes/{rune}', f"data:image/gif;base64,{b64}")
        with open(_html_filepath, 'r', encoding='utf-8') as f:
            data = f.read()
        return data.replace('[PLACEHOLDER]', table)

    @staticmethod
    def _get_daily_runes(html: str) -> List[str]:
        """
        Get the daily rune combinations.
        :param html: the html from the rune goldberg tracker website.
        :return: the four available runes as a list. The first is the first rune, the latter 3 the second rune.
        """
        runes = []
        for val in html.split('.gif'):
            if len(runes) >= 4:
                break
            if 'rune' in val:
                _possible = val.split('rune')[0]
                if 'input' in _possible or 'html' in _possible:
                    continue
                _rune = _possible.split('title=\'')[1].split('\'')[0]
                if 'Rune' in _rune:
                    runes.append(_rune)
        return runes

    def _render_html(self, html: str) -> None:
        """
        Renders the daily runes table.
        :param html: the html from the rune goldberg tracker website.
        :return:
        """
        global _generated_filepath
        output_path = uuid.uuid4().hex + os.path.basename(_generated_filepath)
        new_html: str = self._get_html_table(html=html)
        if config.linux_tmp_path_hti:
            hti = Html2Image(size=(600, 400), browser_executable=config.chromium_executable_path, temp_path='./tmp',
                             custom_flags=['--headless=new', '--virtual-time-budget=10000', '--hide-scrollbars',
                                           '--no-sandbox', '--verbose'])
        else:
            hti = Html2Image(size=(600, 400), browser_executable=config.chromium_executable_path,
                             custom_flags=['--headless=new', '--virtual-time-budget=10000', '--hide-scrollbars',
                                           '--no-sandbox', '--verbose'])
        hti.screenshot(html_str=new_html, save_as=output_path)
        img = Image.open(output_path)
        width, _ = img.size
        crop_width, crop_height = 498, 198
        left = (width - crop_width) // 2 - 8
        top = 8
        right = left + crop_width
        bottom = top + crop_height
        cropped_img = img.crop((left, top, right, bottom))
        cropped_img.save(_generated_filepath)
        os.remove(output_path)

    def daily_exec(self) -> Tuple[str, Dict[str, Any]]:
        """
        Default public facing method.
        :return: the daily rune combinations along with a screenshot of the rune's html table.
        """
        global _generated_filepath
        html: str = self._get_base()
        render_success: bool = False
        try:
            self._render_html(html=html)
            render_success = True
        except Exception as e:
            log.error('Error rendering as html. Trace: ' + str(e), module=Module.RUNE_GOLD)
        base: str = '========== Rune Goldberg Report =========='
        runes: List[str] = self._get_daily_runes(html)
        first: str = 'First Rune: ' + runes[0]
        second: str = f'Second Runes: {", ".join(runes[1:])}'
        end: str = '=========================================='
        return f'{base}\n\n{first}\n{second}\n\n\n{end}', {"image": render_success, 'filepath': _generated_filepath}
