#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import copy
import argparse
import itertools

import cv2 as cv
import numpy as np
import mediapipe as mp

from model import KeyPointClassifier
from Operation import Finger2Mouse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--width", help='cap width', type=int, default=960)
    parser.add_argument("--height", help='cap height', type=int, default=540)

    args = parser.parse_args()

    return args

def main():
    f2m = Finger2Mouse()

    args = get_args()
    cap_device = args.device
    cap_width = args.width
    cap_height = args.height

    # カメラ準備 ----------------------------------------------------------------
    cap = cv.VideoCapture(cap_device)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, cap_width)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, cap_height)

    # モデルロード ---------------------------------------------------------------
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    )

    keypoint_classifier = KeyPointClassifier()

    # ラベル読み込み ------------------------------------------------------------
    with open('model/keypoint_classifier/keypoint_classifier_label.csv',encoding='utf-8-sig') as f:
        keypoint_classifier_labels = csv.reader(f)
        keypoint_classifier_labels = [
            row[0] for row in keypoint_classifier_labels
        ]

    while True:
        # カメラキャプチャ --------------------------------------------------------
        ret, image = cap.read()
        if not ret:
            break
        image = cv.flip(image, 1)  # ミラー表示
        debug_image = copy.deepcopy(image)

        # 検出実施 ------------------------------------------------------------
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = hands.process(image)

        #  finger2mouseのための準備 --------------------------------------------
        if results.multi_hand_landmarks is not None:  # 手が映っているか
            hand_landmarks = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0]
            hand_info = handedness.classification[0].label[0:]  # 右手か左手か
            # 外接矩形の計算
            brect = calc_bounding_rect(debug_image, hand_landmarks)
            # ランドマークの計算
            landmark_list = calc_landmark_list(debug_image, hand_landmarks)

            # 相対座標・正規化座標への変換
            pre_processed_landmark_list = pre_process_landmark(landmark_list)

            # ハンドサイン分類 ----------------------------------------------------
            hand_sign_id = keypoint_classifier(pre_processed_landmark_list)

            # finger2mouseの処理 ----------------------------------------------------
            if hand_sign_id == 0:  # パー
                f2m.move_mouse(landmark_list[8])  # カーソル移動
                f2m.stop(brect)  # プログラム停止判定
            elif (hand_sign_id==2) & (hand_info=="Right"):  # 右1本指
                f2m.leftclick(landmark_list[8])  # クリック
            elif (hand_sign_id==3) & (hand_info=="Right"):  # 右2本指
                f2m.rightclick(landmark_list[8])  # 右クリック
            elif (hand_sign_id==4) & (hand_info=="Right"):  # 右3本指
                f2m.drag(landmark_list[8])  # ドラッグ
            elif (hand_sign_id==2) & (hand_info=="Left"):  # 左１本指
                f2m.upper_right_scroll(landmark_list,brect)  # 上/右にスクロール
            elif (hand_sign_id==3) & (hand_info=="Left"):  # 左2本指
                f2m.under_left_scroll(landmark_list,brect)  # 下/左にスクロール
            elif (hand_sign_id==4) & (hand_info=="Left"):  # 左3本指
                f2m.choose_app()  # アプリ選択
            elif hand_sign_id==5:  # 親指
                f2m.voice_recognition()  # 音声認識
            else:  #グー
                pass  #何もしない

    cap.release()
    cv.destroyAllWindows()


def calc_bounding_rect(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_array = np.empty((0, 2), int)

    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)

        landmark_point = [np.array((landmark_x, landmark_y))]

        landmark_array = np.append(landmark_array, landmark_point, axis=0)

    x, y, w, h = cv.boundingRect(landmark_array)

    return [x, y, x + w, y + h]


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # キーポイント
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point

def pre_process_landmark(landmark_list):
    temp_landmark_list = copy.deepcopy(landmark_list)

    # 相対座標に変換
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temp_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
        temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y

    # 1次元リストに変換
    temp_landmark_list = list(
        itertools.chain.from_iterable(temp_landmark_list))

    # 正規化
    max_value = max(list(map(abs, temp_landmark_list)))

    def normalize_(n):
        return n / max_value

    temp_landmark_list = list(map(normalize_, temp_landmark_list))

    return temp_landmark_list

if __name__ == '__main__':
    main()
