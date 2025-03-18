
# Import cv2 to control image and numpy to control pixels in image
import cv2 as cv
import numpy as np

main_cctv = cv.VideoCapture("http://210.99.70.120:1935/live/cctv090.stream/playlist.m3u8")  # 기본 웹캠 사용 (0), 다른 카메라는 정수 또는 RTSP URL
format = 'avi'
fourcc = 'XVID'  # 코덱 설정 (예: 'XVID', 'MP4V', 'MJPG')
recorded_cctv = cv.VideoWriter()  # 파일명, FPS, 해상도

recording = False # 녹화 유무

#https://topis.seoul.go.kr/6cc831b1-97fb-49b8-9d94-15bc68c0553e
#http://210.99.70.120:1935/live/cctv001.stream/playlist.m3u8
#http://210.99.70.120:1935/live/cctv090.stream/playlist.m3u8          레이크타운 3차 사거리 from https://www.data.go.kr/data/15063717/fileData.do/충청남도 천안시_교통정보 CCTV.csv

while main_cctv.isOpened():
    valid, hometown = main_cctv.read()
    if not valid:
        break

    if recording:
        recorded_cctv_file = hometown[:hometown.rfind('.')] + '.' + format
        fps = hometown.get(cv.CAP_PROP_FPS)
        h, w, *_ = hometown.shape
        is_color = (hometown.ndim > 2) and (hometown.shape[2] > 1)
        recorded_cctv.open(recorded_cctv_file, cv.VideoWriter_fourcc(*fourcc))
        assert recorded_cctv.isOpened(), 'Cannot open the given video, ' + recorded_cctv_file + '.'

    recorded_cctv.write(hometown) # 프레임 저장

    if recording:
        cv.circle(hometown, (50, 50), 10, (0, 0, 255), -1)  # 녹화 중 표시 (빨간 원)

    cv.imshow('Realtime_Hometown_Weather', hometown)

    key = cv.waitKey(1) & 0xFF

    if key == 32 : # Space 키로 모드 전환
        recording = not recording
    #elif key == 46 : # . forward

    #elif key == 44:  # , backward
    elif key == 67:  # C : change right and left
        cv.flip(hometown, 1)
    elif key == 27:  # ESC 키로 종료
        break

main_cctv.release()
recorded_cctv.release()
cv.destroyAllWindows()
