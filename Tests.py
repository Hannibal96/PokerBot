import cv2
from enum import Enum
import numpy as np
import os
from Card import *


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


method = cv2.TM_SQDIFF_NORMED
PHOTO_DISCOVERY_THRESHOLD = 0.1


def compare_photos_cards(im_a, im_b):
    im_a = (im_a > 150)
    im_b = (im_b > 150)
    res = (abs(im_a ^ im_b))
    res_sum = (sum(sum(res)))
    len_x = int(im_a.shape[1])
    len_y = int(im_a.shape[0])
    return res_sum/(len_x*len_y*255)


test_im = cv2.imread('./pictures\Running\AoF_Red_24_1_Turn.png', 0)
cv2.imshow('image', test_im)
cv2.waitKey(0)

cv2.imshow('image', my_turn_image)
cv2.waitKey(0)
cv2.imshow('image', not_my_turn_image)
cv2.waitKey(0)
cv2.imshow('image', empty_my_turn_image)
cv2.waitKey(0)


my_turn_score = compare_photos_cards(test_im, my_turn_image)
not_my_turn_score = compare_photos_cards(test_im, not_my_turn_image)
empty_my_turn_score = compare_photos_cards(test_im, empty_my_turn_image)


print(my_turn_score)
print(not_my_turn_score)
print(empty_my_turn_score)



exit()


for filename in os.listdir("./pictures\Running"):
    print("="*25)
    print(filename)

    im_all = cv2.imread("./pictures\Running/"+filename, 0)

    cv2.imshow('image', im_all)
    cv2.waitKey(0)
    if not (im_all.shape[0] == 105 and im_all.shape[1] == 152):
        continue

    my_turn_score = compare_photos_cards(im_all, my_turn_image)
    not_my_turn_score = compare_photos_cards(im_all, not_my_turn_image)
    empty_my_turn_score = compare_photos_cards(im_all, not_my_turn_image)

    print(my_turn_score)
    print(not_my_turn_score)
    print(empty_my_turn_score)


######################

[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2]  # 5
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3]  # 5

[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 5]  # 10
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 4]  # 10

[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 4]  # 15
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 6]  # 15

[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 3, 5]  # 20
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 2, 8]  # 20

[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 3, 7]  # 25
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 3, 7]  # 25

[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 7]  # 30
[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 5]  # 30


[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 4, 5]  # 35
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 7, 1]  # 35



[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 5, 3]  # 40
[1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 5, 1]  # 40

[1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 6, 1, 1]  # 60
[1, 0, 0, 1, 1, 0, 1, 1, 2, 3, 1, 1, 1]  # 60



[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 3]  # 15 PER 2 PLAYERS
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 5]  # 15

[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 3]  # 10 PER 2 PLAYERS
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 4]  # 10



















