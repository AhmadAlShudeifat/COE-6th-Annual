import socket
import cv2
import mediapipe as mp
from ultralytics import YOLO
import numpy as np
import struct
import time
from collections import defaultdict
import math


class football:
    def __init__(self):
        self.tracker = tracker()
        self.sock = camsocket()
        self.team_scores = {"Team 1": 0, "Team 2": 0}
        self.team_possession = {"Team 1": 0.0, "Team 2": 0.0}
        self.player_possession = defaultdict(float)
        self.goal_line_left = 100
        self.goal_line_right = 1180
        self.last_time = time.time()
        self.sock.accept()

    def getimage(self):
        return self.sock.get_frame()

    def spot_goals_and_score(self, ball_x):
        if ball_x < self.goal_line_left:
            self.team_scores["Team 2"] += 1
        elif ball_x > self.goal_line_right:
            self.team_scores["Team 1"] += 1

    def update_possession(self, ball_x, ball_y, pose_landmarks, player_id, team_id):
        current_time = time.time()
        delta_time = current_time - self.last_time
        self.last_time = current_time
        if not pose_landmarks or ball_x is None:
            return
        leftwrist, rightwrist, lefthip, righthip = pose_landmarks
        hip_x = lefthip.x * 1280
        hip_y = lefthip.y * 720
        distance_to_ball = math.hypot(ball_x - hip_x, ball_y - hip_y)
        possession_threshold = 100
        if distance_to_ball < possession_threshold:
            self.team_possession[team_id] += delta_time
            self.player_possession[player_id] += delta_time

    def get_mvp(self):
        if not self.player_possession:
            return "None"
        return max(self.player_possession, key=self.player_possession.get)

    def run_match(self):
        while True:
            frame = self.getimage()
            if frame is None:
                continue
            rgb_frame = self.tracker.convertBGR(frame)
            timestamp = int(time.time() * 1000)
            pose_landmarks = self.tracker.procandtrack(rgb_frame, timestamp)
            ball_x, ball_y, ball_radius = self.tracker.trackball(frame)
            if ball_x is not None:
                self.spot_goals_and_score(ball_x)
                self.update_possession(
                    ball_x, ball_y, pose_landmarks, "Player_1", "Team 1"
                )
            print(
                f"Score:{self.team_scores}|Possession:{self.team_possession}|MVP:{self.get_mvp()}"
            )


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
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def procandtrack(self, image, timestamp):
        proccesedframe = self.landmarker.detect_for_video(image, timestamp)
        if proccesedframe.pose_landmarks:
            poselandmark = proccesedframe.pose_landmarks[0]
            leftwrist = poselandmark[15]
            rightwrist = poselandmark[16]
            lefthip = poselandmark[23]
            righthip = poselandmark[24]
            return leftwrist, rightwrist, lefthip, righthip
        return None

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


if __name__ == "__main__":
    game = football()
    game.run_match()
