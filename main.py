import socket

import cv2
import mediapipe as mp
from ultralytics import YOLO

model = YOLO("yolov8n.pt")


class football:
    def __init__(self): ...


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
            bodylandmark = poselandmark[11:33]
            for lm in bodylandmark:
                x, y, z = lm.x, lm.y, lm.z
            leftwrist = poselandmark[15]
            rightwrist = poselandmark[16]
            lefthip = poselandmark[23]
            righthip = poselandmark[24]
            return leftwrist, rightwrist, lefthip, righthip

    def trackball(self, frame):
        results = model(frame, classes=[32], verbose=False)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                radius = int((x2 - x1) / 2)
                return center_x, center_y, radius
        return None, None, None
