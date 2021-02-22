import win32gui
import win32com.client
import pyautogui
import cv2
import time
import os
import numpy as np
from enum import Enum
from Card import *

# is my turn, in ratio
FOLD_RELATIVE_X_COR  = 0.725
FOLD_RELATIVE_Y_COR  = 0.903
ALLIN_RELATIVE_X_COR = 0.906
ALLIN_RELATIVE_Y_COR = 0.903
# dealer, in ratio
LEFT_SIDE_DEALER_PART =  0.3
RIGHT_SIDE_DEALER_PART = 0.8
TOP_SIDE_DEALER_PART = 0.3
BOTTOM_SIDE_DEALER_PART = 0.6
# blinds, in ratio
LEFT_SIDE_BLINDS_PART =  0.3
RIGHT_SIDE_BLINDS_PART = 0.75
TOP_SIDE_BLINDS_PART = 0.3
BOTTOM_SIDE_BLINDS_PART = 0.6
# all in , in coordinates
TOP_X_ALLIN = 382
TOP_Y_ALLIN = 146
LEFT_X_ALLIN = 45
LEFT_Y_ALLIN = 320
RIGHT_X_ALLIN = 720
RIGHT_Y_ALLIN = 320


# crop cards, absolute coordinates
CARD_LEN_X = 46
CARD_LEN_Y = 65

CARD_LEFT_X_COR = 274
CARD_LEFT_Y_COR = 345

CARD_RIGHT_X_COR = 326
CARD_RIGHT_Y_COR = 345

SUIT_X_COR = 17
SUIT_Y_COR = 33

SUIT_X_LEN = 27
SUIT_Y_LEN = 28

NUMBER_X_COR = 4
NUMBER_Y_COR = 4

NUMBER_X_LEN = 16
NUMBER_Y_LEN = 22

#
CROP_ALLIN_RELATIVE_X_COR = 0.81
CROP_ALLIN_RELATIVE_Y_COR = 0.83
# time constants
SLEEP_TIME_BEFORE_SCREENSHOT = 0.01
SLEEP_TIME_AFTER_SCREENSHOT = 0.1
# general
TOTAL_SUM_OF_LOCATIONS = 6

PHOTO_DISCOVERY_THRESHOLD = 0.1

my_turn_screenshot_str = "./pictures\Constants\MyTurnAllInButton.png"
not_my_turn_screenshot_str = "./pictures\Constants\MyTurnAllInButtonNot.png"
empty_my_turn_screenshot_str = "./pictures\Constants\EmptyAllInButton.png"
dealer_im_path = "./pictures\Constants\DealerButton.png"
small_blind_im_path = "./pictures\Constants\RedTableSmallBlind.png"
big_blind_im_path = "./pictures\Constants\RedTableBigBlind.png"
all_in_text_im_path = "./pictures\Constants\ALLinText.png"


my_turn_image = cv2.imread(my_turn_screenshot_str, 0)
not_my_turn_image = cv2.imread(not_my_turn_screenshot_str, 0)
empty_my_turn_image = cv2.imread(empty_my_turn_screenshot_str, 0)
dealer_button_image = cv2.imread(dealer_im_path, 0)
small_blind_image = cv2.imread(small_blind_im_path, 0)
big_blind_image = cv2.imread(big_blind_im_path, 0)
all_in_text_image = cv2.imread(all_in_text_im_path, 0)


number_switcher = {
    "Ace.png": Number.Ace,
    "Duce.png": Number.Duce,
    "Three.png": Number.Three,
    "Four.png": Number.Four,
    "Five.png": Number.Five,
    "Six.png": Number.Six,
    "Seven.png": Number.Seven,
    "Eight.png": Number.Eight,
    "Nine.png": Number.Nine,
    "Ten.png": Number.Ten,
    "Jack.png": Number.Jack,
    "Queen.png": Number.Queen,
    "King.png": Number.King,
}

suit_switcher = {
    "Club.png": Suits.Club,
    "Diamond.png": Suits.Diamond,
    "Heart.png": Suits.Heart,
    "Spade.png": Suits.Spade,
}

ranges_switcher = {
    "5 suit"    : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],
    "5 unsuit"  : [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2],

    "10 suit"    : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    "10 unsuit"  : [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4],

    "15 suit"    : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6],
    "15 unsuit"  : [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5],

    "20 suit"    : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 9],
    "20 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6],

    "25 suit"    : [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 8],
    "25 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 8],

    "30 suit"    : [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 4, 5],
    "30 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 8],

    "35 suit"    : [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 6, 2],
    "35 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 8],

    "40 suit"    : [1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 2, 5, 1],
    "40 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 7],

    "45 suit"    : [1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 3, 3, 1],
    "45 unsuit"  : [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 4, 5],

    "50 suit"    : [1, 0, 0, 2, 0, 1, 0, 1, 0, 2, 3, 2, 1],
    "50 unsuit"  : [1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 5, 4],

    "55 suit"    : [1, 0, 0, 2, 0, 1, 1, 0, 1, 2, 3, 1, 1],
    "55 unsuit"  : [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 5, 3],

    "60 suit"    : [1, 0, 1, 1, 1, 0, 1, 0, 2, 2, 2, 1, 1],
    "60 unsuit"  : [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 6, 2],

    "65 suit"    : [1, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1, 1, 1],
    "65 unsuit"  : [1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 6, 1],

    "70 suit"    : [1, 0, 1, 2, 0, 1, 1, 1, 2, 1, 1, 1, 1],
    "70 unsuit"  : [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 3, 4, 1],

}


CUTOFF_OPEN_UNSUIT = ranges_switcher["25 unsuit"]
CUTOFF_OPEN_SUIT =   ranges_switcher["25 suit"]

DEALER_OPEN_UNSUIT = ranges_switcher["30 unsuit"]
DEALER_OPEN_SUIT =   ranges_switcher["30 suit"]

DEALER_DEFEND_UNSUIT = ranges_switcher["5 unsuit"]
DEALER_DEFEND_SUIT =   ranges_switcher["5 suit"]

SMALLBLIND_OPEN_UNSUIT = ranges_switcher["55 unsuit"]
SMALLBLIND_OPEN_SUIT =   ranges_switcher["55 suit"]

SMALLBLIND_DEFEND_CUTOFF_UNSUIT = ranges_switcher["10 unsuit"]
SMALLBLIND_DEFEND_CUTOFF_SUIT =   ranges_switcher["10 suit"]

SMALLBLIND_DEFEND_DEALER_UNSUIT = ranges_switcher["15 unsuit"]
SMALLBLIND_DEFEND_DEALER_SUIT =   ranges_switcher["15 suit"]

SMALLBLIND_DEFEND_TWO_UNSUIT = ranges_switcher["5 unsuit"]
SMALLBLIND_DEFEND_TWO_SUIT =   ranges_switcher["5 suit"]

BIGBLIND_DEFEND_CUTOFF_UNSUIT = ranges_switcher["15 unsuit"]
BIGBLIND_DEFEND_CUTOFF_SUIT =   ranges_switcher["15 suit"]

BIGBLIND_DEFEND_DEALER_UNSUIT = ranges_switcher["20 unsuit"]
BIGBLIND_DEFEND_DEALER_SUIT =   ranges_switcher["20 suit"]

BIGBLIND_DEFEND_SMALLBLIND_UNSUIT = ranges_switcher["35 unsuit"]
BIGBLIND_DEFEND_SMALLBLIND_SUIT =   ranges_switcher["35 suit"]

BIGBLIND_DEFEND_TWO_CUTOFF_DEALER_UNSUIT = ranges_switcher["5 unsuit"]
BIGBLIND_DEFEND_TWO_CUTOFF_DEALER_SUIT =   ranges_switcher["5 suit"]

BIGBLIND_DEFEND_TWO_CUTOFF_SMALLBLIND_UNSUIT = ranges_switcher["5 unsuit"]
BIGBLIND_DEFEND_TWO_CUTOFF_SMALLBLIND_SUIT =   ranges_switcher["5 suit"]

BIGBLIND_DEFEND_TWO_SMALLBLIND_DEALER_UNSUIT = ranges_switcher["5 unsuit"]
BIGBLIND_DEFEND_TWO_SMALLBLIND_DEALER_SUIT =   ranges_switcher["5 suit"]

BIGBLIND_DEFEND_THREE_UNSUIT = ranges_switcher["5 unsuit"]
BIGBLIND_DEFEND_THREE_SUIT =   ranges_switcher["5 suit"]


photo_discovering_method = cv2.TM_SQDIFF_NORMED


class Location(Enum):
    Bottom = 0
    Left = 1
    Top = 2
    Right = 3


class Position(Enum):
    CutOff = 0
    Dealer = 1
    SmallBlind = 2
    BigBlind = 3
    SittingOut = -1


class Action(Enum):
    UnDecided = 0
    Fold = 1
    AllIn = 2


class PreviousAction(Enum):
    Empty = 0
    OneRaiseCutoff = 1
    OneRaiseDealer = 2
    OneRaiseSmallBlind = 3
    TwoRaiseCutoffDealer = 4
    TwoRaiseCutoffSmallblind = 5
    TwoRaiseDealerSmallblind = 6
    ThreeRaise = 6


class Table:
    processing_idle = True

    def __init__(self, name, hwnd, coordinates):
        self.name = name
        self.short_name = squeeze_table_name(self.name)
        self.hwnd = hwnd

        self.curr_hand_num = 0

        self.curr_position = -1
        self.curr_dealer_location = -1
        self.curr_small_blind_location = -1
        self.curr_big_blind_location = -1

        self.curr_location_position_mapping = dict()
        self.curr_position_action_mapping = dict()

        self.previous_action = -1
        self.curr_action = Action.UnDecided

        self.waiting_for_my_turn = False
        self.acted = True

        self.card_a = None
        self.card_b = None

        self.screen_shot = None

        self.top_left_x_cor = coordinates[0]
        self.top_left_y_cor = coordinates[1]
        self.bottom_right_x_cor = coordinates[2]
        self.bottom_right_y_cor = coordinates[3]

        self.x_length = self.bottom_right_x_cor - self.top_left_x_cor
        self.y_length = self.bottom_right_y_cor - self.top_left_y_cor

        self.all_in_cor = None

    def get_hwnd(self):
        return self.hwnd

    def fg_table(self):
        win32gui.SetForegroundWindow(self.hwnd)
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')

    def is_table_visible(self):
        return win32gui.IsWindowVisible(self.hwnd)

    def table_screen_shot(self):        # TODO: mabye return the picture instead of close and reopen
        self.fg_table()

        time.sleep(SLEEP_TIME_BEFORE_SCREENSHOT)
        raw_screenshot_str = "./pictures/Running/"+self.short_name+"_raw.png"
        pyautogui.screenshot(raw_screenshot_str)
        time.sleep(SLEEP_TIME_AFTER_SCREENSHOT)

        im = cv2.imread(raw_screenshot_str, 0)
        im = im[self.top_left_y_cor:self.bottom_right_y_cor, self.top_left_x_cor:self.bottom_right_x_cor]
        time.sleep(SLEEP_TIME_AFTER_SCREENSHOT)

        os.remove(raw_screenshot_str)
        time.sleep(0.1)                         # TODO: change to const

        self.screen_shot = im[:]

    def is_my_turn(self):
        if not self.waiting_for_my_turn:
            return False

        self.processing_idle = False
        self.table_screen_shot()
        table_croped_screenshot = self.screen_shot
        my_turn_state_image = table_croped_screenshot[int(self.y_length * CROP_ALLIN_RELATIVE_Y_COR):, int(self.x_length * CROP_ALLIN_RELATIVE_X_COR):]

        my_turn_score = compare_photos_cards(my_turn_state_image, my_turn_image)
        not_my_turn_score = compare_photos_cards(my_turn_state_image, not_my_turn_image)
        empty_my_turn_score = compare_photos_cards(my_turn_state_image, empty_my_turn_image)

        if my_turn_score < not_my_turn_score and my_turn_score < empty_my_turn_score:
            self.processing_idle = True
            self.waiting_for_my_turn = False
            return True
        elif not_my_turn_score < my_turn_score and not_my_turn_score < empty_my_turn_score:
            self.processing_idle = True
            return False
        elif empty_my_turn_score < my_turn_score and empty_my_turn_score < not_my_turn_score:
            self.processing_idle = True
            return False
        else:
            self.processing_idle = True
            return False

    def find_button_location(self):
        self.processing_idle = False

        validatee_button_location = -10
        last_dealer_location = self.curr_dealer_location

        while True:
            self.table_screen_shot()
            table_croped_screenshot = self.screen_shot

            result = cv2.matchTemplate(dealer_button_image, table_croped_screenshot, photo_discovering_method)

            mn, _, mnLoc, _ = cv2.minMaxLoc(result)
            MPx, MPy = mnLoc

            if MPx < self.x_length * LEFT_SIDE_DEALER_PART:
                self.curr_dealer_location = Location.Left
            elif MPx > self.x_length * RIGHT_SIDE_DEALER_PART:
                self.curr_dealer_location = Location.Right
            elif MPy < self.y_length * TOP_SIDE_DEALER_PART:
                self.curr_dealer_location = Location.Top
            elif MPy > self.y_length * BOTTOM_SIDE_DEALER_PART:
                self.curr_dealer_location = Location.Bottom
            else:
                print("-E- impossible dealer location at:", mnLoc)
                exit()

            if validatee_button_location == self.curr_dealer_location:
                break

            validatee_button_location = self.curr_dealer_location

        if not last_dealer_location == self.curr_dealer_location:
            #self.update_new_hand()
            self.processing_idle = True
            return True

        self.processing_idle = True
        return False

    def update_new_hand(self):
        self.waiting_for_my_turn = True
        self.acted = False
        self.curr_hand_num += 1
        self.curr_action = Action.UnDecided
        self.previous_action = -1

    def find_blinds_locations(self):       # FIXME: deal with no showdown and as a result 'blind' appear in the middle

        self.processing_idle = False

        validate_bb_location = -10
        validate_sb_location = -10

        while True:
            table_croped_screenshot = self.screen_shot

            result = cv2.matchTemplate(small_blind_image, table_croped_screenshot, photo_discovering_method)

            mn, _, mnLoc, _ = cv2.minMaxLoc(result)
            MPx, MPy = mnLoc

            if MPx < self.x_length * LEFT_SIDE_BLINDS_PART:
                self.curr_small_blind_location = Location.Left
            elif MPx > self.x_length * RIGHT_SIDE_BLINDS_PART:
                self.curr_small_blind_location = Location.Right
            elif MPy < self.y_length * TOP_SIDE_BLINDS_PART:
                self.curr_small_blind_location = Location.Top
            elif MPy > self.y_length * BOTTOM_SIDE_BLINDS_PART:
                self.curr_small_blind_location = Location.Bottom
            else:
                if self.curr_hand_num == 1:
                    pass
                else:
                    print("-E- impossible small blind location at:", mnLoc, self.curr_hand_num)
                    exit()

            result = cv2.matchTemplate(big_blind_image, table_croped_screenshot, photo_discovering_method)

            mn, _, mnLoc, _ = cv2.minMaxLoc(result)
            MPx, MPy = mnLoc

            if MPx < self.x_length * LEFT_SIDE_BLINDS_PART:
                self.curr_big_blind_location = Location.Left
            elif MPx > self.x_length * RIGHT_SIDE_BLINDS_PART:
                self.curr_big_blind_location = Location.Right
            elif MPy < self.y_length * TOP_SIDE_BLINDS_PART:
                self.curr_big_blind_location = Location.Top
            elif MPy > self.y_length * BOTTOM_SIDE_BLINDS_PART:
                self.curr_big_blind_location = Location.Bottom
            else:
                print("-E- impossible big blind location at:", mnLoc)
                exit()

            if validate_bb_location == self.curr_big_blind_location and validate_sb_location == self.curr_small_blind_location:
                break

            validate_sb_location = self.curr_small_blind_location
            validate_bb_location = self.curr_big_blind_location

            self.table_screen_shot()

        self.processing_idle = True

    def figure_table_structure(self):

        for location in Location:
            self.curr_location_position_mapping[location] = -10

        self.curr_location_position_mapping[self.curr_dealer_location] = Position.Dealer
        self.curr_location_position_mapping[self.curr_small_blind_location] = Position.SmallBlind
        self.curr_location_position_mapping[self.curr_big_blind_location] = Position.BigBlind

        # classic case no jumps in the order of blinds and button
        if self.curr_dealer_location.value == (self.curr_small_blind_location.value - 1) % 4 == \
                (self.curr_big_blind_location.value - 2) % 4:
            remain_location = Location(TOTAL_SUM_OF_LOCATIONS - self.curr_big_blind_location.value -
                                       self.curr_small_blind_location.value - self.curr_dealer_location.value)
            self.curr_location_position_mapping[remain_location] = Position.CutOff
            # ^^^ FIXME: maybe cutoff is sitting out

        # one sitting out in the middle, not cutoff
        elif (self.curr_dealer_location.value == (self.curr_small_blind_location.value - 1) % 4 ==
                (self.curr_big_blind_location.value - 3) % 4) or \
                (self.curr_dealer_location.value == (self.curr_small_blind_location.value - 2) % 4 ==
                 (self.curr_big_blind_location.value - 3) % 4):
            remain_location = Location(TOTAL_SUM_OF_LOCATIONS - self.curr_big_blind_location.value -
                                       self.curr_small_blind_location.value - self.curr_dealer_location.value)
            self.curr_location_position_mapping[remain_location] = Position.SittingOut

        # two players sitting out
        elif self.curr_dealer_location == self.curr_small_blind_location:

            if (self.curr_big_blind_location.value - 1) % 4 == self.curr_dealer_location.value:
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value + 1)%4)] = Position.SittingOut
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value + 2)%4)] = Position.SittingOut

            elif (self.curr_big_blind_location.value - 2) % 4 == self.curr_dealer_location.value:
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value + 1) % 4)] = Position.SittingOut
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value - 1) % 4)] = Position.SittingOut

            elif (self.curr_big_blind_location.value + 1) % 4 == self.curr_dealer_location.value:
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value + 2) % 4)] = Position.SittingOut
                self.curr_location_position_mapping[Location((self.curr_big_blind_location.value - 1) % 4)] = Position.SittingOut

            else:
                assert False, "-E- impossible table structure"

    def read_cards(self):
        self.processing_idle = False

        self.click_on_cards()
        time.sleep(1.0)                         # TODO: convert to const time
        self.table_screen_shot()

        im = self.screen_shot

        left_card_im = im[CARD_LEFT_Y_COR:CARD_LEFT_Y_COR + CARD_LEN_Y, CARD_LEFT_X_COR:CARD_LEFT_X_COR + CARD_LEN_X]
        right_card_im = im[CARD_RIGHT_Y_COR:CARD_RIGHT_Y_COR + CARD_LEN_Y, CARD_RIGHT_X_COR:CARD_RIGHT_X_COR + CARD_LEN_X]

        time.sleep(0.1)                         # TODO: convert to const time
        self.click_on_cards()                   # TODO: convert to click on close cards

        self.card_a = parse_card(left_card_im)
        self.card_b = parse_card(right_card_im)

        self.processing_idle = True

    def click_on_cards(self):
        pyautogui.click(self.top_left_x_cor + 400, self.top_left_y_cor + 500)   # TODO: convert to consts

    def click_on_allin(self):
        pyautogui.click(self.top_left_x_cor + 715, self.top_left_y_cor + 555)   # TODO: convert to consts

    def click_on_fold(self):
        pyautogui.click(self.top_left_x_cor + 575, self.top_left_y_cor + 555)   # TODO: convert to consts

    def read_previous_actions(self):    # TODO: finish
        self.processing_idle = False

        validate_actions = -10
        while True:
            self.table_screen_shot()
            table_croped_screenshot = self.screen_shot

            result = cv2.matchTemplate(all_in_text_image, table_croped_screenshot, photo_discovering_method)

            coordinates = np.where(np.array(result) <= PHOTO_DISCOVERY_THRESHOLD)

            for position in Position:
                self.curr_position_action_mapping[position] = Action.UnDecided  # TODO: distinct between Fold and undecided

            for idx in range(len(coordinates[0])):
                Px = coordinates[1][idx]
                Py = coordinates[0][idx]

                if Px == RIGHT_X_ALLIN and Py == RIGHT_Y_ALLIN:
                    self.curr_position_action_mapping[self.curr_location_position_mapping[Location.Right]] = Action.AllIn
                elif Px == LEFT_X_ALLIN and Py == LEFT_Y_ALLIN:
                    self.curr_position_action_mapping[self.curr_location_position_mapping[Location.Left]] = Action.AllIn
                if Px == TOP_X_ALLIN and Py == TOP_Y_ALLIN:
                    self.curr_position_action_mapping[self.curr_location_position_mapping[Location.Top]] = Action.AllIn

            if self.curr_position_action_mapping[Position.CutOff] == Action.AllIn:
                if self.curr_position_action_mapping[Position.Dealer] == Action.AllIn:
                    if self.curr_position_action_mapping[Position.SmallBlind] == Action.AllIn:
                        self.previous_action = PreviousAction.ThreeRaise
                    else:   # SB out
                        self.previous_action = PreviousAction.TwoRaiseCutoffDealer
                else:       # DE out
                    if self.curr_position_action_mapping[Position.SmallBlind] == Action.AllIn:
                        self.previous_action = PreviousAction.TwoRaiseCutoffSmallblind
                    else:   # SB out
                        self.previous_action = PreviousAction.OneRaiseCutoff
            else:           # CO out
                if self.curr_position_action_mapping[Position.Dealer] == Action.AllIn:
                    if self.curr_position_action_mapping[Position.SmallBlind] == Action.AllIn:
                        self.previous_action = PreviousAction.TwoRaiseDealerSmallblind
                    else:   # SB out
                        self.previous_action = PreviousAction.OneRaiseDealer
                else:       # DE out
                    if self.curr_position_action_mapping[Position.SmallBlind] == Action.AllIn:
                        self.previous_action = PreviousAction.OneRaiseSmallBlind
                    else:   # SB out
                        self.previous_action = PreviousAction.Empty

            if validate_actions == self.previous_action:
                break
            validate_actions = self.previous_action

        self.all_in_cor = coordinates[:]
        self.processing_idle = True

    def act(self):
        self.processing_idle = False
        action = get_action(self.curr_location_position_mapping[Location.Bottom], self.previous_action, self.card_a, self.card_b)
        if action == Action.AllIn:
            self.click_on_allin()
        elif action == Action.Fold:
            self.click_on_fold()
        else:
            assert False, "-E- impossible act"
        self.curr_action = action
        self.acted = True
        self.processing_idle = True

    def record_hand(self):
        pass

    def get_all_in_cor(self):
        return self.all_in_cor

    def get_screen_shot(self):
        return self.screen_shot

    def get_short_name(self):
        return self.short_name

    def get_is_acted(self):
        return self.acted

    def __str__(self):
        table_str = "="*50+"\n"
        table_str += "="*10 + self.name + "\n"
        table_str += "=" * 2 + "Hand Number: " + str(self.curr_hand_num) + "\n"
        table_str += "=" * 2 + "Location Position Mapping: " + "\n"
        for location in Location:
            if location == Location.Bottom:
                table_str += Color.BOLD + "=" * 4 + str(location) + ": " + "\t" + str(self.curr_location_position_mapping[location]) + Color.END + "\n"
            else:
                table_str += "=" * 4 + str(location) + ": " + "\t" + str(self.curr_location_position_mapping[location]) + "\n"
        table_str += "=" * 2 + "Cards: " + str(self.card_a) + str(self.card_b) + "\n"
        table_str += Color.BOLD + "=" * 2 + "Previous Action: " + str(self.previous_action) + Color.END + "\n"
        table_str += "=" * 2 + "Action: " + str(self.curr_action) + "\n"

        # TODO: other cards
        # TODO: result
        table_str += "=" * 50 + "\n"
        return table_str


def find_running_tables_window():
    def tables_collector(hwnd, tables_list, sub_string="AoF"):
        if sub_string in win32gui.GetWindowText(hwnd):
            tables_list.append(hwnd)

    aof_tables_list = []
    win32gui.EnumWindows(tables_collector, aof_tables_list)

    return aof_tables_list


def set_running_tables(tables_list):
    running_tables_list = []
    for table in tables_list:
        new_table = Table(name=win32gui.GetWindowText(table), hwnd=table, coordinates=win32gui.GetWindowRect(table))
        running_tables_list.append(new_table)
    return running_tables_list


def squeeze_table_name(table_name):
    squeezed_name = ""
    splited = table_name.split()
    squeezed_name += splited[0]+"_"+splited[1]+"_"+splited[2]
    return squeezed_name


def find_shape(im_shape):
    min_val = 1.0
    min_name = ''
    for filename in os.listdir("./pictures\Cards\Shapes"):
        curr_shape = cv2.imread("./pictures\Cards\Shapes/"+filename, 0)
        new_metrice = compare_photos_cards(im_shape, curr_shape)
        if new_metrice < min_val:
            min_val = compare_photos_cards(im_shape, curr_shape)
            min_name = filename

    assert min_name in suit_switcher
    return suit_switcher[min_name]


def find_number(im_number):     # TODO: find more elegant way to classify instead of double folders
    min_val = 1.0
    min_name = ''

    for filename in os.listdir("./pictures/Cards/Numbers_Left"):
        curr_shape = cv2.imread("./pictures/Cards/Numbers_Left/"+filename, 0)
        new_metrice = compare_photos_cards(im_number, curr_shape)
        if new_metrice < min_val:
            min_val = new_metrice
            min_name = filename

    for filename in os.listdir("./pictures/Cards/Numbers_Right"):
        curr_shape = cv2.imread("./pictures/Cards/Numbers_Right/"+filename, 0)
        new_metrice = compare_photos_cards(im_number, curr_shape)
        if new_metrice < min_val:
            min_val = new_metrice
            min_name = filename

    assert min_name in number_switcher
    return number_switcher[min_name]


def compare_photos_cards(im_a, im_b):
    im_a = (im_a > 100)
    im_b = (im_b > 100)
    res = (abs(im_a ^ im_b))
    res_sum = (sum(sum(res)))
    len_x = int(im_a.shape[1])
    len_y = int(im_a.shape[0])
    return res_sum/(len_x*len_y*255)


def parse_card(im_card):
    im_shape = im_card[SUIT_Y_COR:SUIT_Y_COR+SUIT_Y_LEN, SUIT_X_COR:SUIT_X_COR+SUIT_X_LEN]
    suit = find_shape(im_shape)

    im_number = im_card[NUMBER_Y_COR:NUMBER_Y_COR+NUMBER_Y_LEN, NUMBER_X_COR:NUMBER_X_COR+NUMBER_X_LEN]
    number = find_number(im_number)

    return Card(number, suit)


def strategy_get_action(strategy_vector, holding_cards):
    if holding_cards[0].number.value > holding_cards[1].number.value:
        max_value = holding_cards[0].number.value
        min_value = holding_cards[1].number.value
    else:
        max_value = holding_cards[1].number.value
        min_value = holding_cards[0].number.value

    sum = 0
    for idx, val in enumerate(strategy_vector):
        sum += val
        if idx == max_value - 2:
            break
    assert sum <= 13

    if min_value + sum > max_value:
        return Action.AllIn
    return Action.Fold


def get_action(position, prev_action, card_a, card_b):
    Suited = (card_b.suit == card_a.suit)
    if prev_action == PreviousAction.Empty:
        if position == Position.CutOff:
            if Suited:
                return strategy_get_action(CUTOFF_OPEN_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(CUTOFF_OPEN_UNSUIT, [card_a, card_b])
        elif position == Position.Dealer:
            if Suited:
                return strategy_get_action(DEALER_OPEN_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(DEALER_OPEN_UNSUIT, [card_a, card_b])
        elif position == Position.SmallBlind:
            if Suited:
                return strategy_get_action(SMALLBLIND_OPEN_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(SMALLBLIND_OPEN_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible opening position"

    elif prev_action == PreviousAction.OneRaiseCutoff:
        if position == Position.Dealer:
            if Suited:
                return strategy_get_action(DEALER_DEFEND_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(DEALER_DEFEND_UNSUIT, [card_a, card_b])
        elif position == Position.SmallBlind:
            if Suited:
                return strategy_get_action(SMALLBLIND_DEFEND_CUTOFF_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(SMALLBLIND_DEFEND_CUTOFF_UNSUIT, [card_a, card_b])
        elif position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_CUTOFF_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_CUTOFF_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible one-raise-cutoff position"

    elif prev_action == PreviousAction.OneRaiseDealer:
        if position == Position.SmallBlind:
            if Suited:
                return strategy_get_action(SMALLBLIND_DEFEND_DEALER_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(SMALLBLIND_DEFEND_DEALER_UNSUIT, [card_a, card_b])
        elif position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_DEALER_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_DEALER_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible one-raise-delaer position"

    elif prev_action == PreviousAction.OneRaiseSmallBlind:
        if position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_SMALLBLIND_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_SMALLBLIND_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible one-raise-smallblind position"

    elif prev_action == PreviousAction.TwoRaiseCutoffDealer:
        if position == Position.SmallBlind:
            if Suited:
                return strategy_get_action(SMALLBLIND_DEFEND_TWO_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(SMALLBLIND_DEFEND_TWO_UNSUIT, [card_a, card_b])
        elif position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_CUTOFF_DEALER_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_CUTOFF_DEALER_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible two-raises-cutoff-dealer position"

    elif prev_action == PreviousAction.TwoRaiseCutoffSmallblind:
        if position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_CUTOFF_SMALLBLIND_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_CUTOFF_SMALLBLIND_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible two-raises-cutoff-smallblind position"

    elif prev_action == PreviousAction.TwoRaiseDealerSmallblind:
        if position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_SMALLBLIND_DEALER_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_TWO_SMALLBLIND_DEALER_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible two-raises-dealer-smallblind position"

    elif prev_action == PreviousAction.ThreeRaise:
        if position == Position.BigBlind:
            if Suited:
                return strategy_get_action(BIGBLIND_DEFEND_THREE_SUIT, [card_a, card_b])
            else:
                return strategy_get_action(BIGBLIND_DEFEND_THREE_UNSUIT, [card_a, card_b])
        else:
            assert False, "-E- impossible three-raise position"

    else:
        assert False, "-E- impossible previous action"


aof_tables_list = find_running_tables_window()
running_tables = set_running_tables(aof_tables_list)


while True:
    try:
        for table in running_tables:
            if table.is_table_visible():

                if table.find_button_location():
                    if not table.get_is_acted():         # was in BB and all fold
                        print(table)
                    table.update_new_hand()
                    table.find_blinds_locations()
                    table.figure_table_structure()
                    table.read_cards()

                if table.is_my_turn():
                    table.read_previous_actions()
                    table.act()
                    print(table)

            while not Table.processing_idle:
                pass

            time.sleep(0.1)

    except Exception as e:
        print("="*50+"\n"+"="*10+"Caught Exception:")
        print(e)
        print(table)
        print(table.get_all_in_cor())
        cv2.imwrite("./pictures\problematic cases/" + table.get_short_name() + "_crush.png", table.get_screen_shot())
        exit()

