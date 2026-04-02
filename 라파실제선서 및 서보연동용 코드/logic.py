# 라즈베리파이 + INA219 + 서보 모터 연동 예제

## 1. 필요한 부품
- Raspberry Pi (3/4 이상 권장)
- INA219 전류 센서 모듈
- 서보 모터 (SG90 등)
- I2C 연결용 점퍼선
- 전원 공급 (Raspberry Pi + 서보 모터)
- 선택: 온도 센서 (DS18B20 / TMP36)

---

## 2. 회로 연결
### INA219
| INA219 핀 | Raspberry Pi 핀 |
|------------|----------------|
| VCC        | 3.3V           |
| GND        | GND            |
| SDA        | GPIO2 (SDA)    |
| SCL        | GPIO3 (SCL)    |

### 서보 모터
| 서보 핀 | Raspberry Pi 핀 |
|----------|----------------|
| VCC      | 5V             |
| GND      | GND            |
| Signal   | GPIO18 (PWM)   |

> **주의:** 서보 전류가 클 경우 Pi 5V 직접 연결하지 말고 별도 외부 전원 사용 권장

---

## 3. Python 코드 예제

```python
import time
import board
import busio
from adafruit_ina219 import INA219
import RPi.GPIO as GPIO

# -----------------------------
# 1. GPIO 및 서보 초기화
# -----------------------------
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm_servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz
pwm_servo.start(0)

# 서보 각도 설정 함수
def set_servo_angle(angle):
    duty = 2 + (angle / 18)  # SG90 기준
    pwm_servo.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm_servo.ChangeDutyCycle(0)

# -----------------------------
# 2. INA219 초기화
# -----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
ina219 = INA219(i2c)

# -----------------------------
# 3. 임계치 설정
# -----------------------------
CURRENT_THRESHOLD = 3.0  # Amp
SWELLING_SIGNAL = 1       # 가상 신호 (온도 조건으로 생성 가능)

# -----------------------------
# 4. 측정 및 서보 제어 루프
# -----------------------------
try:
    while True:
        current = ina219.current / 1000  # mA → A 변환
        voltage = ina219.bus_voltage
        power = ina219.power

        print(f"Current: {current:.2f} A, Voltage: {voltage:.2f} V, Power: {power:.2f} W")

        # 팽창 판정 예제 (가상: 온도 기반 또는 임계 전류 기반)
        if current > CURRENT_THRESHOLD or SWELLING_SIGNAL:
            print("팽창 감지! 서보 모터 작동")
            set_servo_angle(90)  # 90도 회전
        else:
            set_servo_angle(0)   # 정상 상태

        time.sleep(0.5)

except KeyboardInterrupt:
    print("종료 중...")
finally:
    pwm_servo.stop()
    GPIO.cleanup()
