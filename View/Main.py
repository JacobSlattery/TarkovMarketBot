import time
import random
import PySimpleGUI as SimpleGui

from Control import Controller
from Control.Controller import Location


def image_viewer_column():
    return [

        [SimpleGui.Text("Choose an image from list on left:")],
        [SimpleGui.Text(size=(40, 1), key="-TOUT-")],
        [SimpleGui.Image(key="-IMAGE-")],

    ]


def first_column():
    return [
        [
            SimpleGui.Text("Image Folder"),
            SimpleGui.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            SimpleGui.FolderBrowse(),
        ],
        [
            SimpleGui.Listbox(
                values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
            )
        ],
    ]


def get_layout():
    layout = [

        [

            SimpleGui.Column(first_column()),

            SimpleGui.VSeperator(),

            SimpleGui.Column(image_viewer_column()),

        ]

    ]
    return layout


BUY_ATTEMPTS = 'Buy Attempts:'
BUY_LOOP_COUNT = 'Buy Loops:'
REPEAT_COUNT = 'Repeat Count:'
LOOP_WAIT_TIME_SECONDS = 'Loop Wait Time (Seconds):'
CONTINUAL_BUY = 'Continual Buy:'
CONTINUAL_BUY_MIN_CONDITION = 'Min Condition'
CONTINUAL_BUY_ATTEMPTS = 'Attempts'
MAX_PRICE = 'Max Price'

REFRESH = 'Refresh'
BUY = 'Buy'
FULL_LOOP = 'Loop'
GOTO_FLEA = 'Goto Flea'

SELL_ALL = 'All'
SELL_THERAPIST = 'Therapist'
SELL_RAGMAN = 'Ragman'

SURV12 = 'Surv12'
DEVTAC_RONIN = 'DevTac Ronin'
SILVER_BADGE = 'Silver Badge'
OLD_FIRESTEEL = 'Old Firesteel'
VERITAS_GUITAR_PICK = 'Veritas Guitar Pick'
SSSH_94 = 'SSSh-94'

SEARCH = 'Search'

controller = Controller.Controller()


def launch():
    first_row_keys = [REFRESH, BUY, FULL_LOOP, GOTO_FLEA]
    second_row_keys = [SELL_ALL, SELL_THERAPIST, SELL_RAGMAN]
    third_row_keys = [SURV12, DEVTAC_RONIN, SILVER_BADGE, OLD_FIRESTEEL, SSSH_94, VERITAS_GUITAR_PICK]
    buttons_1 = [SimpleGui.Button(name) for name in first_row_keys]
    buttons_2 = [SimpleGui.Button(name) for name in second_row_keys]
    buttons_3 = [SimpleGui.Button(name) for name in third_row_keys]

    buttons_keys = first_row_keys + second_row_keys + third_row_keys + [SEARCH]
    layout = [[SimpleGui.Text(BUY_ATTEMPTS),
               SimpleGui.InputText(controller.default_buy_attempts, size=(3, 1), key=BUY_ATTEMPTS),
               SimpleGui.Text(BUY_LOOP_COUNT),
               SimpleGui.InputText(controller.default_buy_loops, size=(3, 1), key=BUY_LOOP_COUNT),
               SimpleGui.Text(REPEAT_COUNT),
               SimpleGui.InputText(controller.default_repeat_count, size=(3, 1), key=REPEAT_COUNT),
               SimpleGui.Text(LOOP_WAIT_TIME_SECONDS),
               SimpleGui.InputText(controller.default_loop_wait_time, size=(7, 1), key=LOOP_WAIT_TIME_SECONDS)],
              [SimpleGui.Text('Actions:')],
              buttons_1,
              [SimpleGui.Text('Sell:')],
              buttons_2,
              [SimpleGui.Text('Buy:')],
              buttons_3,
              [SimpleGui.Text('Continual Buy:')],
              [SimpleGui.Text('Item:'),
               SimpleGui.InputText(size=(30, 1), key=CONTINUAL_BUY),
               SimpleGui.Text('Max Price:'),
               SimpleGui.InputText('1', size=(8, 1), key=MAX_PRICE),
               SimpleGui.Text('Min Condition:'),
               SimpleGui.InputText(size=(3, 1), key=CONTINUAL_BUY_MIN_CONDITION),
               SimpleGui.Text('Attempts:'),
               SimpleGui.InputText('2', size=(9, 1), key=CONTINUAL_BUY_ATTEMPTS),
               SimpleGui.Button(SEARCH)]]

    window = SimpleGui.Window('Market Assist', layout, use_default_focus=False)

    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        if event in buttons_keys:
            handle_button(event, values, window)

    window.close()


def full_loop(buy_count=1, buy_loop_count=1, loop_count=1, loop_time_space=0):
    first_loop = True
    print('Launching Loop Count ' + str(loop_count))
    for i in range(loop_count):
        if not controller.stop:
            print('Loop ' + str(i))
            if not first_loop:
                if not loop_time_space == 0:
                    if loop_time_space < 10:
                        controller.internal_sleep(loop_time_space + random.randint(0, 2))
                    else:
                        num = round(loop_time_space * 0.15)
                        num = num + 1
                        controller.internal_sleep(loop_time_space + random.randint(0, num))
            for j in range(buy_loop_count):
                controller.buy('Surv12 field', '44900', '99', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 5))
                controller.buy('DevTac R', '101000', '99', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 6))
                controller.buy('Silver Badge', '37000', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 5))
                controller.buy('Old firesteel', '39000', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 7))
                controller.buy('SSSh-94', '45500', '99', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 5))
                controller.buy('Veritas guitar pick', '33900', buy_count=buy_count)
                controller.internal_sleep(random.randint(0, 5))
            controller.sell_all()
            first_loop = False


def handle_button(btn, values, window):
    starting_point = Controller.get_mouse_position()
    controller.click(Location.SCREEN_CORNER)
    buy_attempts = int(values[BUY_ATTEMPTS])
    buy_loops = int(values[BUY_LOOP_COUNT])
    repeat_count = int(values[REPEAT_COUNT])
    loop_time_space = int(values[LOOP_WAIT_TIME_SECONDS])
    search_item = values[CONTINUAL_BUY]
    min_condition: int = None
    if not values[CONTINUAL_BUY_MIN_CONDITION] == '':
        print(values[CONTINUAL_BUY_MIN_CONDITION])
    continual_buy_attempts = int(values[CONTINUAL_BUY_ATTEMPTS])
    max_price = int(values[MAX_PRICE])
    if btn == REFRESH:
        controller.click(Location.REFRESH)
        controller.move_to(Location.PURCHASE_DIALOG_YES)
    elif btn == BUY:
        controller.buy_item(1, True)
    elif btn == FULL_LOOP:
        full_loop(buy_attempts, buy_loops, repeat_count, loop_time_space)
    elif btn == GOTO_FLEA:
        controller.click(Location.FLEA_TAB)
    elif btn == SELL_THERAPIST:
        controller.sell_items_to_trader(Location.THERAPIST)
    elif btn == SELL_RAGMAN:
        controller.sell_items_to_trader(Location.RAGMAN)
    elif btn == SELL_ALL:
        controller.sell_all()
    elif btn == SURV12:
        controller.buy('Surv12 field', '44900', '99', buy_count=buy_attempts)
    elif btn == DEVTAC_RONIN:
        controller.buy('DevTac R', '101000', '99', buy_count=buy_attempts)
    elif btn == SILVER_BADGE:
        controller.buy('Silver Badge', '37000', buy_count=buy_attempts)
    elif btn == OLD_FIRESTEEL:
        controller.buy('Old firesteel', '39000', buy_count=buy_attempts)
    elif btn == SSSH_94:
        controller.buy('SSSh-94', '45500', '99', buy_count=buy_attempts)
    elif btn == VERITAS_GUITAR_PICK:
        controller.buy('Veritas guitar pick', '33900', buy_count=buy_attempts)
    elif btn == SEARCH:
        controller.buy(search_item, str(max_price), min_condition)
        for i in range(continual_buy_attempts - 1):
            controller.internal_sleep(2 + (random.randint(0, 10) * .1))
            controller.click(Location.REFRESH)
            controller.internal_sleep(.7)
            controller.buy_item(1, True)

    controller.reset_stop()
    Controller.move_to_point(starting_point.x, starting_point.y)
    window.force_focus()
    window[BUY].set_focus()
    Controller.move_to_point(starting_point.x, starting_point.y)

