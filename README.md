# Realtime_Outside_Weather Tool

실시간 CCTV 스트림을 통해 외부 날씨를 모니터링하고 녹화할 수 있도록 OpenCV를 통해 구현한 간단한 Python 애플리케이션입니다.

## 기능 소개

- 실시간 CCTV 스트림 모니터링
- 비디오 녹화 및 저장 기능
- 좌우 반전 모드 지원
- 사용자 친화적인 키보드 단축키
- 녹화 상태 시각적 표시
- 다양한 비디오 형식(MP4, AVI) 지원

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install opencv-python numpy
```

2. 저장소 클론 또는 소스 코드 다운로드:

```bash
git clone https://github.com/jbjihwan/realtime_outside_weather.git
cd cctv-monitoring-tool
```

3. 프로그램 실행:

```bash
python cctv_monitor.py
```

## 사용 방법

### CCTV 스트림 설정

기본적으로 다음 CCTV 스트림을 사용합니다:
```python
stream_url = "http://210.99.70.120:1935/live/cctv090.stream/playlist.m3u8"  # 레이크타운 3차 사거리 from https://www.data.go.kr/data/15063717/fileData.do/충청남도 천안시_교통정보 CCTV.csv
```

다른 CCTV 소스를 사용하려면 소스 코드에서 `stream_url` 변수를 수정하세요.

### 키보드 단축키

| 키 | 기능 |
|-----|-----|
| **스페이스바** | 녹화 시작/중지 토글 |
| **C** | 좌우 반전 모드 토글 |
| **ESC** | 프로그램 종료 |

### 녹화 기능

- 스페이스바를 누르면 녹화가 시작되고 파일 저장 대화상자가 나타납니다.
- 파일 형식으로 MP4 또는 AVI를 선택할 수 있습니다.
- 녹화 중에는 화면 좌측 상단에 빨간색 원과 "REC" 텍스트가 표시됩니다.
- 다시 스페이스바를 누르면 녹화가 중지됩니다.

## 문제 해결

### 코덱 오류

OpenH264 라이브러리 관련 오류가 발생할 경우:

```
Failed to load OpenH264 library: openh264-1.8.0-win64.dll
```

다음 해결책을 시도해 보세요:

1. 코드에서 MP4 대신 AVI 형식으로 저장
2. [OpenH264 릴리스 페이지](https://github.com/cisco/openh264/releases)에서 해당 라이브러리 다운로드 후 설치

### 스트림 연결 오류

CCTV 스트림에 연결할 수 없는 경우:

1. 인터넷 연결 확인
2. CCTV 스트림 URL이 유효한지 확인
3. 방화벽 설정 확인

## 환경

- Python 3.6 이상
- OpenCV 4.x
- tkinter (파일 저장 대화상자용)
- NumPy
