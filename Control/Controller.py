import threading
import time

import pyautogui
from enum import Enum
import os
import json
from pynput import keyboard
import math


class Location(Enum):
    SETTINGS: str = 'settings'
    CURRENCY_DROP: str = 'currency_drop'
    CURRENCY_DROP_RUB: str = 'currency_drop_rub'
    PRICE_TO: str = 'price_to'
    QUANTITY_FROM: str = 'quantity_from'
    CONDITION_FROM: str = 'condition_from'
    CONDITION_TO: str = 'condition_to'
    REMOVE_BART: str = 'remove_bart'
    SHOW_ONLY_FUNCTIONAL: str = 'show_only_functional'
    SETTINGS_RESET: str = 'settings_reset'
    SETTINGS_OK: str = 'settings_ok'
    SETTINGS_CLOSE: str = 'settings_close'
    SEARCH_BAR: str = 'search_bar'
    FIRST_SEARCH_RESULT: str = 'first_search_result'
    FIRST_RESULT_PURCHASE: str = 'first_item_purchase'
    PURCHASE_DIALOG_ALL: str = 'purchase_dialog_all'
    PURCHASE_DIALOG_YES: str = 'purchase_dialog_yes'
    PURCHASE_DIALOG_NO: str = 'purchase_dialog_no'
    PURCHASE_DIALOG_CLOSE: str = 'purchase_dialog_close'
    REFRESH: str = 'refresh'
    SCREEN_CORNER: str = 'screen_corner'
    TOP_LEFT_ITEM_STASH: str = 'top_left_item_stash'
    TOP_LEFT_ITEM_SELL: str = 'top_left_item_sell'
    CHARACTER_TAB: str = 'character_tab'
    TRADER_TAB: str = 'trader_tab'
    FLEA_TAB: str = 'flea_tab'
    THERAPIST: str = 'therapist'
    MECHANIC: str = 'mechanic'
    RAGMAN: str = 'ragman'
    JAEGER: str = 'jaeger'
    SELL_TAB: str = 'sell_tab'
    DEAL: str = 'deal'
    NOT_ALL_BOUGHT_OK: str = 'not_all_bought_ok'
    PURCHASE_CONFIRMATION_YES: str = 'purchase_confirmation_yes'
    PURCHASE_CONFIRMATION_NO: str = 'purchase_confirmation_no'


def press(key):
    pyautogui.press(key)


def write(data: str):
    pyautogui.write(data)


def get_mouse_position():
    return pyautogui.position()


def move_to_point(x, y):
    pyautogui.moveTo(x, y)


def click_point(x, y, dur=0.0):
    pyautogui.click(x, y, dur)


class Controller:

    def __init__(self):
        self.locations = {}
        self.config = {}
        self.resolution = '1080p'
        config_file_path = str(os.path.dirname(__file__)) + '\\config.json'

        with open(config_file_path, 'r') as json_file:
            self.config = json.load(json_file)

        self.resolution = self.config['Settings']['default_resolution']
        self.default_buy_attempts = self.config['Menu']['buy_attempts']
        self.default_buy_loops = self.config['Menu']['buy_loops']
        self.default_repeat_count = self.config['Menu']['repeat_count']
        self.default_loop_wait_time = self.config['Menu']['loop_wait_time']

        location_file_path = str(os.path.dirname(__file__)) + '\\locations.json'
        with open(location_file_path, 'r') as json_file:
            self.locations = json.load(json_file)

        self.key_listener = keyboard.Listener(on_press=self.esc_pressed)
        self.key_listener.start()
        self.stop = False

    def esc_pressed(self, key):
        if key == keyboard.Key.f1:
            self.stop = True

    def internal_sleep(self, amt):
        if not self.stop:
            values = math.modf(amt)
            fraction = values[0]
            seconds = values[1]
            # print('sleep: (seconds:' + str(seconds) + ', fraction:' + str(fraction) + ')')
            if seconds > 1:
                for i in range(int(seconds)):
                    if not self.stop:
                        time.sleep(1)
            else:
                time.sleep(seconds)
            time.sleep(fraction)

    def reset_stop(self):
        self.stop = False

    def click(self, location: str, x_change=0, y_change=0, dur=0.0):
        if not self.stop:
            cord = self.get_location(location)
            pyautogui.click(cord[0] + x_change, cord[1] + y_change, duration=dur)

    def move_to(self, location: str, dur=0.0):
        if not self.stop:
            cord = self.get_location(location)
            pyautogui.moveTo(cord[0], cord[1], duration=dur)

    def get_location(self, location: str):
        return self.locations[self.resolution][location.value]

    def get_sale_item_distance(self):
        return self.config['Data']['sale_item_size_' + self.resolution]

    def sell_all(self):
        if not self.stop:
            self.sell_items_to_trader(Location.THERAPIST, False)
            self.sell_items_to_trader(Location.RAGMAN, False)
            self.click(Location.FLEA_TAB)

    def sell_items_to_trader(self, trader: str, return_to_flea=True):
        if not self.stop:
            self.click(Location.TRADER_TAB)
            self.internal_sleep(.1)
            self.click(trader)
            self.internal_sleep(.1)
            self.click(Location.SELL_TAB)
            self.internal_sleep(.4)
            width = self.config['Settings']['default_sale_zone']['sell_width']
            height = self.config['Settings']['default_sale_zone']['sell_height']
            move_size = self.get_sale_item_distance()
            start_row_index = self.config['Settings']['default_sale_zone']['starting_row_index']
            start_column_index = self.config['Settings']['default_sale_zone']['starting_column_index']

            x_adjust = 0
            y_adjust = 0
            pyautogui.keyDown('ctrl')
            for row in range(height):
                if self.stop:
                    break
                for col in range(width):
                    if self.stop:
                        break
                    self.click(Location.TOP_LEFT_ITEM_SELL, x_adjust, y_adjust)
                    x_adjust += move_size
                y_adjust += move_size
                x_adjust = 0
            pyautogui.keyUp('ctrl')
            self.click(Location.DEAL)
            self.internal_sleep(.2)
            if return_to_flea:
                self.click(Location.FLEA_TAB)

    def buy_item(self, times: int, buy_all: bool):
        if not self.stop:
            first = True
            for i in range(times):
                if not self.stop:
                    self.click(Location.FIRST_RESULT_PURCHASE)
                    if buy_all:
                        self.click(Location.PURCHASE_DIALOG_ALL)
                    self.click(Location.PURCHASE_DIALOG_YES)
                    self.internal_sleep(.5)
                    self.click(Location.PURCHASE_CONFIRMATION_YES)
                    self.internal_sleep(.2)
                    self.click(Location.NOT_ALL_BOUGHT_OK)
                    self.internal_sleep(.1)

    def reset_settings(self):
        if not self.stop:
            self.click(Location.SETTINGS)
            self.click(Location.SETTINGS_RESET)
            self.internal_sleep(.1)

    def settings(self, price_to: str, condition_from: str = None, rub=True, remove_bart=True, only_functional=True):
        if not self.stop:
            self.internal_sleep(.05)
            self.click(Location.SETTINGS)
            self.click(Location.SETTINGS_RESET)
            self.internal_sleep(.2)
            self.click(Location.SETTINGS)
            self.internal_sleep(.15)
            if rub:
                self.click(Location.CURRENCY_DROP)
                self.internal_sleep(.05)
                self.click(Location.CURRENCY_DROP_RUB)
            if condition_from is not None:
                self.click(Location.CONDITION_FROM)
                pyautogui.write(condition_from)
            self.click(Location.QUANTITY_FROM)
            pyautogui.write('1')
            self.click(Location.PRICE_TO)
            pyautogui.write(price_to)
            if not remove_bart:
                self.click(Location.REMOVE_BART)
            if only_functional:
                self.click(Location.SHOW_ONLY_FUNCTIONAL)
            self.click(Location.SETTINGS_OK)

    def search(self, name: str):
        if not self.stop:
            self.click(Location.SEARCH_BAR)
            pyautogui.write(name)
            pyautogui.press('enter')
            self.internal_sleep(1.5)
            self.click(Location.FIRST_SEARCH_RESULT)

    def buy(self, name: str, price_from: str, min_condition: str = None, buy_count: int = 1):
        if not self.stop:
            self.reset_settings()
            self.internal_sleep(1.1)
            self.search(name)
            self.settings(price_from, min_condition)
            self.click(Location.REFRESH)
            self.internal_sleep(.7)
            self.buy_item(buy_count, True)
