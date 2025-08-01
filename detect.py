import cv2
import os

def detect_lanes(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        edges = cv2.Canny(frame, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, cv2.cv2.PI/180, threshold=100, minLineLength=50, maxLineGap=50)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        frame = cv2.resize(frame, (640, 480))
        out.write(frame)

    cap.release()
    out.release()
