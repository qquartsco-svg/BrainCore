# BrainCore - 상태 중심 동역학 통합 인프라

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/qquartsco-svg/BrainCore)
[![PHAM Signed](https://img.shields.io/badge/PHAM-Signed-green.svg)](PHAM_SIGNATURE.md)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

**BrainCore는 무엇인가?**

여러 개의 독립적인 "뇌 엔진"들을 하나의 **상태 공간**에서 통합하여 동작시키는 인프라입니다.

---

## 🎯 핵심 정체성 (30초 이해)

### BrainCore는 **오케스트레이터가 아닙니다**

```
❌ 오케스트레이터 (엔진을 제어)
❌ 엔진 컨트롤러 (명령을 내림)
✅ 상태 공간 중심 시스템 (엔진들이 상태를 변화시킴)
```

### 핵심 원칙

```
The system is state-centric.
BrainCore orchestrates updates over a shared GlobalState.
Engines do not control the system; they perturb the state.
```

**수학적 표현**:
```
state_{t+1} = engine.update(state_t)
```

**의미**: 엔진들은 상태를 "perturb(교란)"하여 변화시킵니다. 최종 상태는 모든 엔진의 상호작용 결과입니다.

---

## 🧠 무엇을 하는가?

### 1. 상태 중심 실행

모든 엔진이 공유하는 **GlobalState**를 중심으로 동작:

```python
GlobalState = {
    state_vector: [x1, x2, ..., xN],  # 공통 상태 벡터
    energy: E,                        # 에너지 (Hopfield)
    risk: r,                          # 위험도
    extensions: {                     # 엔진별 확장 데이터
        "L0": {...},                  # NeuralDynamicsCore 데이터
        "L1": {...},                  # StateManifoldEngine 데이터
        "L2": {...},                  # HistoricalDataReconstructor 데이터
    }
}
```

### 2. 엔진 통합

**5개 엔진 래퍼**가 상태를 순차적으로 업데이트:

```
state_0
  ↓ WellFormationEngine → state_1 (W, b 설정)
  ↓ StateManifoldEngine → state_2 (risk_map 설정)
  ↓ NeuralDynamicsCore → state_3 (동역학 실행)
  ↓ HistoricalDataReconstructor → state_4 (기록)
  ↓ CingulateCortex → state_5 (모니터링)
  ↓
state_final
```

### 3. 에너지 최소화 수렴

엔진들이 상태를 변화시키면서 에너지를 최소화하는 방향으로 수렴:
```
|E_{t+1} - E_t| < ε  →  수렴 완료
```

---

## 💡 왜 필요한가?

### 문제 상황

여러 개의 독립적인 "뇌 엔진"들이 각각 다른 형식으로 데이터를 주고받으면:
- 데이터 변환 코드가 복잡해짐
- 엔진 간 의존성이 복잡해짐
- 새로운 엔진 추가가 어려움

### BrainCore의 해결책

**하나의 공통 상태 공간 (GlobalState)**을 만들고, 모든 엔진이 이 상태를 업데이트:

- ✅ 데이터 변환 불필요 (모두 GlobalState 사용)
- ✅ 엔진 간 의존성 단순화 (상태만 공유)
- ✅ 새 엔진 추가 쉬움 (SelfOrganizingEngine Protocol만 구현)

---

## 🚀 빠른 시작

### 설치

```bash
git clone https://github.com/qquartsco-svg/BrainCore.git
cd BrainCore
pip install -r requirements.txt
```

### 기본 사용 (3줄)

```python
from brain_core import BrainCore, GlobalState
import numpy as np

# 1. BrainCore 생성
core = BrainCore(mode="production")

# 2. 초기 상태 생성
initial_state = GlobalState(
    state_vector=np.array([0.5, 0.3, 0.8]),
    energy=0.0,
    risk=0.0,
)

# 3. 실행
result = core.run_cycle(initial_state=initial_state)
final_state = result["final_state"]

print(f"Energy: {final_state.energy:.4f}")
print(f"Risk: {final_state.risk:.4f}")
```

### 실제 엔진 연결

```python
from brain_core import BrainCore, GlobalState
from brain_core.real_engine_imports import (
    import_well_formation_engine,
    import_state_manifold_engine,
)
from brain_core.engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
)

# 실제 엔진 import 및 래핑
WellFormationEngine = import_well_formation_engine()
well_engine = WellFormationEngine()
well_wrapper = WellFormationEngineWrapper(well_engine)

StateManifoldEngine = import_state_manifold_engine()
manifold_engine = StateManifoldEngine()
manifold_wrapper = StateManifoldEngineWrapper(manifold_engine)

# BrainCore에 등록
core = BrainCore()
core.register_engine("well_formation", well_wrapper, priority=10)
core.register_engine("state_manifold", manifold_wrapper, priority=20)

# 실행
result = core.run_cycle(initial_state=initial_state)
```

---

## 📐 아키텍처

### 상태 중심 실행 흐름

```
┌─────────────────────────────────────────┐
│         GlobalState (공유 상태)          │
│  ┌───────────────────────────────────┐  │
│  │ Core: state_vector, energy, risk  │  │
│  │ Extensions: {L0, L1, L2, ...}     │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ↓        ↓        ↓
         [엔진1]   [엔진2]   [엔진3]
              ↓        ↓        ↓
         state 업데이트 (perturb)
              ↓        ↓        ↓
         ┌─────────────────────┐
         │  최종 GlobalState    │
         └─────────────────────┘
```

### 엔진 구조

**5개 엔진 래퍼**:

1. **WellFormationEngineWrapper**
   - 역할: L0 초기화 (W, b 생성)
   - 수식: `E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i`

2. **StateManifoldEngineWrapper**
   - 역할: L0 제약 조건 생성 (risk_map 설정)
   - 수식: `risk_amplified = risk_base · (1 + (high_risk_count - 1) · 0.2)`

3. **NeuralDynamicsCoreWrapper**
   - 역할: 실제 동역학 실행 (상태 진화)
   - 수식: `τ · dx/dt = -x + f(Wx + I + b)`

4. **HistoricalDataReconstructorWrapper**
   - 역할: 상태 기록 (인과 링크 추출)
   - 수식: `causal_link = (fragment_i, fragment_j, strength)`

5. **CingulateCortexEngineWrapper**
   - 역할: 안정성 모니터링 (건강 체크)
   - 기능: 갈등 모니터링, 오류 감지, 복구 권장

---

## 🎯 사용 사례

### 1. 산업용: 실시간 제어 시스템

```python
# 센서 데이터 → BrainCore → 제어 신호
while True:
    sensor_data = get_sensor_data()
    state = GlobalState(state_vector=np.array(sensor_data))
    result = core.run_cycle(initial_state=state)
    control_signal = result["final_state"].state_vector
    send_control_signal(control_signal)
```

### 2. 연구용: 뇌 모델링 연구

```python
# 상태 궤적 수집 및 분석
core = BrainCore(mode="research")
result = core.run_cycle(
    initial_state=initial_state,
    return_intermediate=True,
)
trajectory = result["trajectory"]
# 에너지 변화, 위험도 변화, 인과 링크 분석
```

### 3. 철학적: 의식 모델링

```python
# 상태 공간 탐색, 에너지 최소화 수렴, 인과 네트워크 형성
# Well Formation, Risk Map, Causal Links, Storyline 생성
```

---

## 📊 현재 상태

### ✅ 완료 (v0.3.0)

- ✅ 상태 중심 실행 구조
- ✅ GlobalState (Core + Extensions)
- ✅ 5개 엔진 래퍼 구현
- ✅ 실제 엔진 연결 (3/4 완료)
- ✅ Cingulate Cortex Engine (모니터링)
- ✅ PHAM 블록체인 서명

### ⚠️ 진행 중

- ⚠️ NeuralDynamicsCore 실제 연결 (위치 확인 필요)
- ⚠️ 성능 최적화

### 📋 확장 가능

- 📋 ControllerEngine 모드 (Protocol 유지)
- 📋 Physics Pipeline 구현 (Protocol만 정의)
- 📋 다층 스케일 구조 (MultiScaleGlobalState)

---

## 🔗 블록체인 서명 (PHAM)

BrainCore v0.3.0은 **PHAM 블록체인**에 서명되어 코드 무결성을 보장합니다.

- **SHA256**: `4f6606b697996a989f83a0e75b08b1a2a11b3b652157b5e1fe62e2ac937959d5`
- **파일 수**: 18개
- **서명 시간**: 2026-02-05

자세한 내용은 [`PHAM_SIGNATURE.md`](PHAM_SIGNATURE.md)를 참고하세요.

---

## 📚 문서 구조

```
BrainCore/
├── README.md                    # 이 문서 (시작점)
├── ARCHITECTURE.md              # 아키텍처 상세 설명
├── DESIGN_INVARIANTS.md         # 설계 불변 원칙 ⭐
├── PHAM_SIGNATURE.md            # 블록체인 서명 기록
├── MULTISCALE_POTENTIAL_ANALYSIS.md  # 다층 잠재함수 분석
├── src/brain_core/              # 핵심 코드
│   ├── brain_core.py            # BrainCore 메인
│   ├── global_state.py          # GlobalState 정의
│   ├── engine_wrappers.py       # 5개 엔진 래퍼
│   └── ...
├── examples/                    # 사용 예시
└── tests/                       # 테스트
```

---

## 🧪 테스트

```bash
python -m pytest tests/ -v
```

**테스트 결과**: 30개 테스트 통과 ✅

---

## 📝 버전

- **v0.3.0** (2026-02-05): 상태 중심 동역학 통합 인프라 완료
- **v0.2.0**: 엔진 통합 완료
- **v0.1.0**: 초기 구현

---

## 👤 작성자

**GNJz (Qquarts)**

---

## 📄 라이선스

[라이선스 정보 추가 예정]

---

## 🔗 관련 프로젝트

- [WellFormationEngine](https://github.com/qquartsco-svg/WellFormation_Engine): L0 초기화기
- [StateManifoldEngine](https://github.com/qquartsco-svg/StateManifoldEngine): L0 제약 조건 생성기
- [NeuralDynamicsCore](https://github.com/...): 동역학 코어
- [HistoricalDataReconstructor](https://github.com/qquartsco-svg/HistoricalDataReconstructor): 상태 기록기

---

## 💬 핵심 요약

**BrainCore는**:
- ✅ 여러 뇌 엔진을 하나의 상태 공간에서 통합
- ✅ 상태 중심 실행 (엔진들이 상태를 perturb)
- ✅ 에너지 최소화 수렴
- ✅ 확장 가능한 구조 (새 엔진 추가 쉬움)

**BrainCore는 아니다**:
- ❌ 오케스트레이터 (엔진 제어)
- ❌ 엔진 컨트롤러 (명령 내림)
- ❌ 단순 데이터 파이프라인

---

**상태**: v0.3.0 완료, 프로덕션 준비 완료 ✅
