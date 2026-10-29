import socket

import cv2
import mediapipe as mp
import torch
from torch import nn, optim


class football:
    def __init__(self, model_path="holistic_landmarker.task"):
        hollistic = mp.tasks.BaseOptions
        self.HolisticLandmarker = mp.tasks.vision.HolisticLandmarker
        self.HolisticLandmarkerOptions = mp.tasks.vision.HolisticLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
