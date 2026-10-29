import cv2
import socket
import struct
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 65512)) #localhost

cap = cv2.VideoCapture(0)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        data = buffer.tobytes()

        message_size = struct.pack('!I', len(data))

        client_socket.sendall(message_size + data)
finally:
    cap.release()
    client_socket.close()
