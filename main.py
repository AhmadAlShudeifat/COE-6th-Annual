import socket

import cv2
import mediapipe as mp
import torch
from torch import nn, optim


class football:
    def __init__(self, modelpath="holistic_landmarker.task"): ...


class tracker:
    def __init__(self, modelpath="holistic_landmarker.task"):
        self.hollistic = mp.tasks.BaseOptions
        self.holisticlandmarker = mp.tasks.vision.HolisticLandmarker
        self.holisticlandmarkeroptions = mp.tasks.vision.HolisticLandmarkerOptions
        self.visionrunningmode = mp.tasks.vision.RunningMode
        self.settings = self.holisticlandmarkeroptions(
            basesettings=self.hollistic(model_asset_path=modelpath),
            running_mode=self.visionrunningmode.VIDEO,
            min_face_presence_confidence=0.5,
            min_pose_detection_confidence=0.5,
            min_hand_landmarks_confidence=0.5,
        )
