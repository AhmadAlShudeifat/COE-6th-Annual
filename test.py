import socket
import struct
import cv2
import numpy as np

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 65512))
server.listen(1)
print("waiting for cam ..")

conn, addr = server.accept()
print("Connected:", addr)

try:
    while True:
        header = b""
        while len(header) < 4:
            part = conn.recv(4 - len(header))
            if not part:
                raise ConnectionError("Client disconnected")
            header += part

        data_size = struct.unpack("!I", header)[0]

        data = b""
        while len(data) < data_size:
            part = conn.recv(data_size - len(data))
            if not part:
                raise ConnectionError("Client disconnected")
            data += part

        frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    conn.close()
    server.close()
    cv2.destroyAllWindows()

