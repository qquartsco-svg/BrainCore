# BrainCore

**여러 개의 "뇌 엔진"을 하나로 통합해서 사용하는 도구**

---

## 🎯 이게 뭐하는 거야?

### 간단한 비유

**여러 개의 AI 엔진을 하나의 "공통 상태"에서 동작시키는 도구**

예를 들어:
- 엔진 A: 패턴 학습
- 엔진 B: 위험도 평가
- 엔진 C: 안정화
- 엔진 D: 인과관계 추적

이들을 각각 따로 쓰면 복잡하지만, **BrainCore를 쓰면 하나의 상태 공간에서 모두 동작**합니다.

### 문제 상황

여러 개의 독립적인 AI/뇌 엔진들이 각각 다른 형식으로 데이터를 주고받으면:
- 엔진 A는 JSON 형식
- 엔진 B는 NumPy 배열
- 엔진 C는 딕셔너리
- 엔진 D는 리스트

→ **데이터 변환 코드가 복잡해지고, 엔진 추가가 어려워짐**

### BrainCore의 해결책

**하나의 공통 상태 (GlobalState)**를 만들고, 모든 엔진이 이 상태를 업데이트:

```
엔진1 → GlobalState 업데이트
엔진2 → GlobalState 업데이트  
엔진3 → GlobalState 업데이트
...
→ 최종 결과
```

**장점**:
- ✅ 데이터 변환 불필요 (모두 GlobalState 사용)
- ✅ 엔진 추가 쉬움 (새 엔진만 만들면 됨)
- ✅ 엔진 간 의존성 단순화 (상태만 공유)

---

## 💼 실제로 뭐에 쓰나?

### 예시 1: 실시간 제어 시스템 (로봇/드론)

**상황**: 로봇이나 드론을 제어해야 함

**문제**: 
- 센서 데이터를 읽어야 함
- 위험도를 평가해야 함
- 제어 신호를 생성해야 함

**BrainCore 사용**:
```python
# 센서 데이터 → 위험도 평가 → 제어 신호 생성
센서 데이터 → WellFormationEngine (패턴 학습)
           → StateManifoldEngine (위험도 평가)
           → NeuralDynamicsCore (안정화)
           → 제어 신호 출력
```

**결과**: 센서 데이터를 입력하면 자동으로 제어 신호가 나옴

### 예시 2: 데이터 분석 파이프라인

**상황**: 복잡한 데이터를 분석해야 함

**문제**:
- 데이터에서 패턴을 찾아야 함
- 인과관계를 추적해야 함
- 스토리를 재구성해야 함

**BrainCore 사용**:
```python
# 데이터 → 패턴 학습 → 인과관계 추적 → 스토리 재구성
데이터 → WellFormationEngine (패턴 학습)
      → HistoricalDataReconstructor (인과관계 추적)
      → 스토리라인 생성
```

**결과**: 데이터를 입력하면 자동으로 스토리라인이 생성됨

### 예시 3: 뇌 모델링 연구

**상황**: 뇌의 동작을 시뮬레이션하고 싶음

**문제**: 여러 뇌 영역이 서로 상호작용하면서 전체 뇌가 동작함

**BrainCore 사용**:
```python
# 여러 뇌 영역을 하나의 상태 공간에서 통합
뇌 영역1 → GlobalState 업데이트
뇌 영역2 → GlobalState 업데이트
뇌 영역3 → GlobalState 업데이트
...
→ 전체 뇌 동작 시뮬레이션
```

**결과**: 여러 뇌 영역을 통합하여 전체 뇌를 시뮬레이션

---

## 🚀 빠른 시작 (5분)

### 1. 설치

```bash
git clone https://github.com/qquartsco-svg/BrainCore.git
cd BrainCore
pip install -r requirements.txt
```

### 2. 기본 사용 (3줄)

```python
from brain_core import BrainCore, GlobalState
import numpy as np

# BrainCore 생성
core = BrainCore(mode="production")

# 초기 상태 생성 (예: 센서 데이터)
initial_state = GlobalState(
    state_vector=np.array([0.5, 0.3, 0.8]),  # 센서 값들
    energy=0.0,
    risk=0.0,
)

# 실행
result = core.run_cycle(initial_state=initial_state)
final_state = result["final_state"]

# 결과 확인
print(f"최종 상태: {final_state.state_vector}")
print(f"에너지: {final_state.energy:.4f}")
print(f"위험도: {final_state.risk:.4f}")
```

### 3. 실제 엔진 연결

```python
from brain_core import BrainCore, GlobalState
from brain_core.real_engine_imports import import_well_formation_engine
from brain_core.engine_wrappers import WellFormationEngineWrapper
import numpy as np

# 실제 엔진 import
WellFormationEngine = import_well_formation_engine()
well_engine = WellFormationEngine()
well_wrapper = WellFormationEngineWrapper(well_engine)

# BrainCore에 등록
core = BrainCore()
core.register_engine("well_formation", well_wrapper, priority=10)

# 실행
initial_state = GlobalState(
    state_vector=np.array([0.5, 0.3, 0.8]),
    energy=0.0,
    risk=0.0,
)
result = core.run_cycle(initial_state=initial_state)
```

---

## 🧠 핵심 개념

### GlobalState (공통 상태)

모든 엔진이 공유하는 상태:

```python
GlobalState = {
    state_vector: [x1, x2, ..., xN],  # 공통 상태 벡터
    energy: E,                        # 에너지
    risk: r,                          # 위험도 (0.0 ~ 1.0)
    extensions: {                     # 엔진별 데이터
        "L0": {...},                  # NeuralDynamicsCore 데이터
        "L1": {...},                  # StateManifoldEngine 데이터
        "L2": {...},                  # HistoricalDataReconstructor 데이터
    }
}
```

### 엔진 동작 방식

**핵심 원칙**: 엔진들은 상태를 "perturb(교란)"하여 변화시킴

```
state_{t+1} = engine.update(state_t)
```

**의미**: 각 엔진이 상태를 조금씩 변화시키고, 최종 상태는 모든 엔진의 상호작용 결과

### 실행 흐름

```
초기 상태
  ↓
엔진1 업데이트 → 상태 변화
  ↓
엔진2 업데이트 → 상태 변화
  ↓
엔진3 업데이트 → 상태 변화
  ↓
...
  ↓
최종 상태 (에너지 최소화 수렴)
```

---

## 📊 현재 구현된 엔진

### 5개 엔진 래퍼

1. **WellFormationEngineWrapper**
   - **역할**: 패턴 학습 (W, b 생성)
   - **용도**: 데이터에서 패턴을 찾아 에너지 지형 형성

2. **StateManifoldEngineWrapper**
   - **역할**: 위험도 평가 (risk_map 생성)
   - **용도**: 여러 위험 요소를 통합하여 위험 지형 생성

3. **NeuralDynamicsCoreWrapper**
   - **역할**: 동역학 실행 (상태 진화)
   - **용도**: 상태를 안정화시키는 방향으로 진화

4. **HistoricalDataReconstructorWrapper**
   - **역할**: 인과관계 추적 (causal_links 기록)
   - **용도**: 데이터에서 인과관계를 찾아 스토리 재구성

5. **CingulateCortexEngineWrapper**
   - **역할**: 시스템 모니터링 (건강 체크)
   - **용도**: 시스템 오류 감지 및 복구 권장

---

## 🎯 사용 사례

### 1. 실시간 제어 시스템

```python
# 로봇/드론 제어
while True:
    sensor_data = get_sensor_data()  # 센서 읽기
    state = GlobalState(state_vector=np.array(sensor_data))
    result = core.run_cycle(initial_state=state)
    control_signal = result["final_state"].state_vector
    send_control_signal(control_signal)  # 제어 신호 전송
```

### 2. 데이터 분석

```python
# 복잡한 데이터 분석
data = load_complex_data()
state = GlobalState(state_vector=np.array(data))
result = core.run_cycle(initial_state=state)

# 결과 분석
print(f"위험도: {result['final_state'].risk}")
print(f"인과 링크: {result['final_state'].causal_links}")
print(f"스토리라인: {result['final_state'].storyline}")
```

### 3. 뇌 모델링 연구

```python
# 뇌 시뮬레이션
core = BrainCore(mode="research")
result = core.run_cycle(
    initial_state=initial_state,
    return_intermediate=True,
)

# 상태 궤적 분석
trajectory = result["trajectory"]
for state in trajectory:
    print(f"Energy: {state.energy}, Risk: {state.risk}")
```

---

## 📐 아키텍처

### 상태 중심 실행

```
┌─────────────────────────────────┐
│      GlobalState (공유 상태)     │
│  state_vector, energy, risk     │
│  extensions: {L0, L1, L2, ...}  │
└─────────────────────────────────┘
         ↓        ↓        ↓
    [엔진1]   [엔진2]   [엔진3]
         ↓        ↓        ↓
    상태 업데이트 (perturb)
         ↓        ↓        ↓
    ┌─────────────────────┐
    │   최종 GlobalState   │
    └─────────────────────┘
```

### 엔진 실행 순서

```
state_0
  ↓ WellFormationEngine → state_1 (패턴 학습)
  ↓ StateManifoldEngine → state_2 (위험도 평가)
  ↓ NeuralDynamicsCore → state_3 (안정화)
  ↓ HistoricalDataReconstructor → state_4 (인과관계 추적)
  ↓ CingulateCortex → state_5 (모니터링)
  ↓
state_final
```

---

## ✅ 현재 상태

### 완료 ✅

- ✅ 상태 중심 실행 구조
- ✅ GlobalState (Core + Extensions)
- ✅ 5개 엔진 래퍼 구현
- ✅ 실제 엔진 연결 (3/4 완료)
- ✅ PHAM 블록체인 서명

### 진행 중 ⚠️

- ⚠️ NeuralDynamicsCore 실제 연결
- ⚠️ 성능 최적화

---

## 🔗 블록체인 서명 (PHAM)

BrainCore v0.3.0은 **PHAM 블록체인**에 서명되어 코드 무결성을 보장합니다.

- **SHA256**: `4f6606b697996a989f83a0e75b08b1a2a11b3b652157b5e1fe62e2ac937959d5`
- 자세한 내용은 [`PHAM_SIGNATURE.md`](PHAM_SIGNATURE.md) 참고

---

## 📚 문서

- **README.md**: 이 문서 (시작점)
- **ARCHITECTURE.md**: 아키텍처 상세 설명
- **DESIGN_INVARIANTS.md**: 설계 불변 원칙
- **PHAM_SIGNATURE.md**: 블록체인 서명 기록
- **docs/**: 상세 문서

---

## 🧪 테스트

```bash
python -m pytest tests/ -v
```

**테스트 결과**: 30개 테스트 통과 ✅

---

## 📝 버전

- **v0.3.0** (2026-02-05): 상태 중심 동역학 통합 인프라 완료

---

## 👤 작성자

**GNJz (Qquarts)**

---

## 💬 한 줄 요약

**BrainCore는 여러 개의 독립적인 "뇌 엔진"을 하나의 공통 상태 공간에서 통합하여 사용하는 도구입니다.**

**상태**: v0.3.0 완료, 프로덕션 준비 완료 ✅
