
# Import cv2 to control image and numpy to control pixels in image
import cv2 as cv
import subprocess
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import time

# Tkinter GUI 숨기기
tk.Tk().withdraw()

# 실시간 스트리밍 URL (예: RTSP 또는 HTTP)
stream_url = "http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8"  # 기본 웹캠 사용 (0), 다른 카메라는 정수 또는 RTSP URL
                                                                            # 레이크타운 3차 사거리 from https://www.data.go.kr/data/15063717/fileData.do/충청남도 천안시_교통정보 CCTV.csv
main_cctv = cv.VideoCapture(stream_url)
start_time = time.time()

while not main_cctv.isOpened():
    if time.time() - start_time > 5:  # 5초 초과 시 종료
        print("Error: Unable to open video stream")
        exit()
    print("Retrying video stream connection...")
    time.sleep(1)
    main_cctv = cv.VideoCapture(stream_url)

print("Video stream connected!")

if not main_cctv.isOpened():
    print("Error: Unable to open video stream")
    exit()

# 해상도 및 FPS 가져오기
frame_width = int(main_cctv.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(main_cctv.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(main_cctv.get(cv.CAP_PROP_FPS)) or 10  # FPS가 감지되지 않으면 기본 10

# 녹화 유무
recording = False
recorded_cctv = None

# 좌우 반전 상태 변수
flip_mode = False

#https://topis.seoul.go.kr/6cc831b1-97fb-49b8-9d94-15bc68c0553e
#http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8
#http://210.99.70.120:1935/live/cctv090.stream/playlist.m3u8          레이크타운 3차 사거리 from https://www.data.go.kr/data/15063717/fileData.do/충청남도 천안시_교통정보 CCTV.csv

while True:
    valid, hometown = main_cctv.read()
    if not valid or hometown is not None:
        print("Error: Failed to fetch frame. Retrying...")
        time.sleep(1)  # 1초 대기 후 재시도
        continue

    if flip_mode:
        hometown = cv.flip(hometown, 1)

    if recording and recorded_cctv is not None:
        recorded_cctv.write(hometown)
        cv.circle(hometown, (50, 50), 10, (0, 0, 255), -1)  # 빨간 원 표시

    cv.imshow('Realtime_Hometown_Weather', hometown)

    key = cv.waitKey(1) & 0xFF

    if key == 32:  # Space 키 -> 녹화 시작/정지
        if not recording:
            # 저장할 위치 선택
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi")],
                title="Choose Save Location"
            )
            if save_path:  # 사용자가 경로를 선택했을 때만 녹화 시작
                # 확장자에 따라 코덱 변경
                if save_path.endswith('.mp4'):
                    fourcc = cv.VideoWriter_fourcc(*'avc1')  # H.264
                else:
                    fourcc = cv.VideoWriter_fourcc(*'XVID')  # AVI용 XVID

                recorded_cctv = cv.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))
                if not recorded_cctv.isOpened():
                    print("Error: Failed to initialize VideoWriter")
                    recorded_cctv = None
                else:
                    recording = True
                    print(f"Recording started: {save_path}")
        else:
            recording = False
            if recorded_cctv:
                recorded_cctv.release()
                recorded_cctv = None
            print("Recording stopped")

    elif key == ord('c') or key == ord('C'):  # 'C' 키 -> 좌우 반전 토글
        flip_mode = not flip_mode
        print(f"Flip mode: {'ON' if flip_mode else 'OFF'}")

    elif key == 27:  # ESC 키로 종료
            break

main_cctv.release()
if recorded_cctv:
    recorded_cctv.release()
cv.destroyAllWindows()
