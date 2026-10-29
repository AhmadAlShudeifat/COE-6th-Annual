import socket

import cv2
import mediapipe as mp
from ultralytics import YOLO
import numpy as np
import struct


class football:
    def __init__(self):
        self.tracker = tracker()
        self.sock = camsocket()

    def getimage(self):
        self.sock.recv_all()


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
        self.model = YOLO("yolov8n.pt")

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
        results = self.model(frame, classes=[32], verbose=False)
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)
                radius = int((x2 - x1) / 2)
                return center_x, center_y, radius
        return None, None, None


class camsocket:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("127.0.0.1", 65512))
        self.server_socket.listen(1)
        self.conn = None

    def accept(self):
        self.conn, _ = self.server_socket.accept()

    def recv_all(self, count):
        buf = b""
        while count > 0:
            newbuf = self.conn.recv(count)
            if not newbuf:
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def get_frame(self):
        packed_size = self.recv_all(4)
        if not packed_size:
            return None
        message_size = struct.unpack("!I", packed_size)[0]
        frame_data = self.recv_all(message_size)
        if not frame_data:
            return None
        np_arr = np.frombuffer(frame_data, dtype=np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    def close(self):
        if self.conn:
            self.conn.close()
        self.server_socket.close()
