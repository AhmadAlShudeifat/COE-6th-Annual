import socket

import cv2
import mediapipe as mp
import torch
from torch import nn, optim


class football:
    def __init__(self, modelpath="holistic_landmarker.task"): ...


class tracker:
    def __init__(self, modelpath="holistic_landmarker.task"):
        base_options = mp.tasks.BaseOptions(model_asset_path=modelpath)
        options = mp.tasks.vision.HolisticLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            min_face_presence_confidence=0.5,
            min_pose_detection_confidence=0.5,
            min_hand_landmarks_confidence=0.5,
        )
        self.landmarker = mp.tasks.vision.HolisticLandmarker.create_from_options(
            options
        )

    def convertBGR(self, frame):
        rgbimage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return rgbimage

    def procandtrack(self, image, timestamp):
        proccesedframe = self.landmarker.detect_for_video(image, timestamp)
        if proccesedframe.pose.landmarks:
            poselandmark = proccesedframe.pose_landmarks[0]
