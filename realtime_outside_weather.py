import cv2 as cv
import tkinter as tk
from tkinter import filedialog
import numpy as np

# Tkinter GUI 숨기기
tk.Tk().withdraw()

# 실시간 스트리밍 URL (예: RTSP 또는 HTTP)
stream_url = "http://210.99.70.120:1935/live/cctv090.stream/playlist.m3u8"  # 레이크타운 3차 사거리
main_cctv = cv.VideoCapture(stream_url)

if not main_cctv.isOpened():
    print("Error: Unable to open video stream")
    exit()

# 해상도 및 FPS 가져오기
frame_width = int(main_cctv.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(main_cctv.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(main_cctv.get(cv.CAP_PROP_FPS)) or 30  # FPS가 감지되지 않으면 기본 30

# 녹화 유무
recording = False
recorded_cctv = None

# save_path 초기화
save_path = None

# 좌우 반전 상태 변수
flip_mode = False

print(f"Video properties: {frame_width}x{frame_height} at {fps} FPS")

# 첫 프레임을 읽어서 해상도 확인
ret, test_frame = main_cctv.read()
if ret:
    actual_width = test_frame.shape[1]
    actual_height = test_frame.shape[0]
    # 해상도가 다르면 업데이트
    if actual_width != frame_width or actual_height != frame_height:
        frame_width, frame_height = actual_width, actual_height
        print(f"Updated resolution: {frame_width}x{frame_height}")

while True:
    valid, hometown = main_cctv.read()
    if not valid:
        print("Error: Failed to fetch frame")
        # 스트림 재연결 시도
        main_cctv.release()
        main_cctv = cv.VideoCapture(stream_url)
        if not main_cctv.isOpened():
            break
        continue

    if flip_mode:
        hometown = cv.flip(hometown, 1)

    if recording:
        if recorded_cctv is None:  # 녹화가 시작되면 VideoWriter 한 번만 열기
            save_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi")],
                title="Choose Save Location"
            )
            if save_path:  # 사용자가 경로를 선택했을 때만 녹화 시작
                try:
                    # 해상도 확인 및 FPS 조정
                    if fps > 60:
                        fps = 30  # FPS 제한
                        print(f"FPS limited to {fps}")

                    # 확장자에 따라 코덱 변경
                    if save_path.endswith('.mp4'):
                        # H.264 코덱 사용 (더 호환성이 좋음)
                        fourcc = cv.VideoWriter_fourcc(*'avc1')  # 또는 'H264'
                    else:
                        fourcc = cv.VideoWriter_fourcc(*'XVID')  # AVI용 XVID

                    recorded_cctv = cv.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

                    if not recorded_cctv.isOpened():
                        # 첫 번째 방법이 실패하면 다른 코덱 시도
                        print("Trying alternative codec...")
                        if save_path.endswith('.mp4'):
                            fourcc = cv.VideoWriter_fourcc(*'XVID')
                            temp_path = save_path.replace('.mp4', '.avi')
                            recorded_cctv = cv.VideoWriter(temp_path, fourcc, fps, (frame_width, frame_height))
                            print(f"Saving as AVI instead: {temp_path}")
                        else:
                            fourcc = cv.VideoWriter_fourcc(*'MJPG')
                            recorded_cctv = cv.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

                    print(f"Recording started: {save_path}")
                except Exception as e:
                    print(f"Error initializing VideoWriter: {e}")
                    recording = False
                    recorded_cctv = None
            else:
                print("No save path selected.")
                recording = False
                continue  # 사용자가 경로를 선택하지 않았을 때 녹화 중지

        try:
            recorded_cctv.write(hometown)
            # 녹화 중 표시
            cv.circle(hometown, (50, 50), 10, (0, 0, 255), -1)  # 빨간 원 표시
            cv.putText(hometown, "REC", (65, 55), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        except Exception as e:
            print(f"Error writing frame: {e}")

    cv.imshow('Realtime_Hometown_Weather', hometown)

    key = cv.waitKey(1) & 0xFF

    if key == 32:  # Space 키 -> 녹화 시작/정지
        if not recording:
            recording = True
            print(f"Recording started")
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
    recorded_cctv.release()  # 녹화 종료 시 파일 닫기
cv.destroyAllWindows()