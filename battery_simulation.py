# 폐배터리 재사용 판별 시뮬레이션 설계 (Python 예제 포함)

## 1. 목표
- 재사용 가능한 폐배터리 vs 재사용 불가능한 폐배터리 판별
- 열폭주 위험은 가상 시뮬레이션으로만 확인
- 초기 열화(팽창, 내부 저항 증가, 전류 이상) 감지 기준

---

## 2. 실험/시뮬레이션 조건
| 항목 | 값 | 설명 |
|------|----|------|
| 온도 범위 | 50–80°C | 50–70°C: 초기 열화 관찰, 70–80°C: 재사용 판정 |
| 유지 시간 | 10분 | 팽창/전류 이상 여부 판별 기준 |
| 가상 전류 범위 | 0–5A | 정상 배터리: ±5% 변동, 열화 배터리: 급상승/급감 |
| 팽창 신호 | 0–1 | 0: 정상, 1: 팽창 발생 (서보 동작 시그널) |

---

## 3. Python 시뮬레이션 예제

```python
import numpy as np
import matplotlib.pyplot as plt

# 시뮬레이션 파라미터
time_min = 10         # 관찰 시간 (분)
dt = 0.1              # 시간 간격 (분)
time = np.arange(0, time_min, dt)

# 정상 배터리: 가상 전류 (A)
normal_current = 2.0 + 0.05*np.random.randn(len(time))  # ±5% 노이즈
# 열화 배터리: 가상 전류 급상승
degraded_current = 2.0 + np.where(time>5, 0.5*np.exp((time-5)/2), 0)  # 5분 이후 급상승

# 팽창 신호 (가상)
normal_swelling = np.zeros(len(time))
degraded_swelling = np.where(time>5, 1, 0)  # 5분 이후 팽창 발생

# 그래프 출력
plt.figure(figsize=(10,6))
plt.subplot(2,1,1)
plt.plot(time, normal_current, label="Normal Battery Current (A)")
plt.plot(time, degraded_current, label="Degraded Battery Current (A)")
plt.ylabel("Current [A]")
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(time, normal_swelling, label="Normal Swelling")
plt.plot(time, degraded_swelling, label="Degraded Swelling")
plt.xlabel("Time [min]")
plt.ylabel("Swelling Signal")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# 판정 로직 예제
def battery_judgement(current, swelling, threshold_current=3.0, swelling_flag=0.5):
    if np.any(current > threshold_current) or np.any(swelling > swelling_flag):
        return "Re-use Not Recommended"
    else:
        return "Re-use Possible"

# 테스트
print("Normal Battery:", battery_judgement(normal_current, normal_swelling))
print("Degraded Battery:", battery_judgement(degraded_current, degraded_swelling))
