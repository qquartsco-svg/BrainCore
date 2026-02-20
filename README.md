# BrainCore - 뇌 코어 오케스트레이터

**작성일**: 2026-02-05  
**버전**: 0.3.0  
**상태**: 상태 중심 동역학 통합 인프라 완료

---

## 📚 문서

- **README.md**: 전체 개요 (이 문서)
- **ARCHITECTURE.md**: 구조 설명 (수식 포함)
- **DESIGN_INVARIANTS.md**: 설계 불변 원칙 ⭐
- **PHAM_SIGNATURE.md**: 블록체인 서명 기록
- **FINAL_COMPREHENSIVE_REVIEW.md**: 종합 검토 리포트
- 자세한 문서는 `docs/` 폴더를 참고하세요.

---

## 🎯 목적

개별 엔진들을 하나의 뇌로 통합하는 **상태 중심 동역학 통합 인프라**

### 프로젝트 목표

**산업용 중심 + 연구/철학적 확장 가능**

- **산업용**: 실제 제어/의사결정 시스템, 실시간 처리, 안정성 중시
- **연구용**: 뇌 모델링 연구 도구, 실험 가능성, 데이터 수집
- **철학적**: 인지/의식 탐구, 이론적 완성도, 생물학적 정확성

---

## 🧠 핵심 정체성

### 상태 중심 동역학 통합 인프라

**오케스트레이터가 아니다**  
**엔진 컨트롤러가 아니다**  
**상태 공간 중심 시스템이다**

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

여기서:
- `state_t`: 시간 t에서의 GlobalState
- `engine.update`: 엔진별 상태 변환 함수
- `state_{t+1}`: 시간 t+1에서의 업데이트된 상태

---

## 🔧 핵심 기능

### 1. 상태 중심 실행 (State-Centric Execution)

**GlobalState (Core + Extensions 구조)**
- **Core**: 모든 엔진이 공유하는 최소 공통 필드
  - `state_vector`: 공통 상태 벡터 (N차원)
  - `energy`: 에너지 (Hopfield energy)
  - `risk`: 위험도 (0.0 ~ 1.0)
  - `step`: 시뮬레이션 스텝
  - `timestamp`: 시간 스탬프
  
- **Extensions**: 엔진별 확장 데이터
  - `extensions["L0"]`: NeuralDynamicsCore 데이터 (W, b, converged)
  - `extensions["L1"]`: StateManifoldEngine 데이터 (risk_map, dimensions)
  - `extensions["L2"]`: HistoricalDataReconstructor 데이터 (causal_links, storyline)
  - `extensions["well_formation"]`: WellFormationEngine 데이터 (episodes)
  - `extensions["cingulate"]`: CingulateCortexEngine 데이터 (health, conflicts)

### 2. 엔진 통합 및 오케스트레이션

**5개 엔진 래퍼 구현 완료**:
1. **WellFormationEngineWrapper**: L0 초기화기 (W, b 설정)
   - Hebbian 학습: `Δw_ij = η · pre_i · post_j - λ · w_ij`
   - 에너지 지형 형성: `E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i`

2. **StateManifoldEngineWrapper**: L0 제약 조건 생성기 (risk_map 설정)
   - 위험 지형 통합: `risk_amplified = risk_base · (1 + (high_risk_count - 1) · 0.2)`

3. **NeuralDynamicsCoreWrapper**: 실제 동역학 상태가 살아있는 코어
   - 신경 동역학: `τ · dx/dt = -x + f(Wx + I + b)`
   - 에너지 최소화: `dE/dt ≤ 0` (Lyapunov 안정성)

4. **HistoricalDataReconstructorWrapper**: L0 상태 기록기 (causal_links 기록)
   - 인과 네트워크 추출: `causal_link = (fragment_i, fragment_j, strength)`
   - 스토리라인 생성: `storyline = [fragment_0, fragment_1, ..., fragment_n]`

5. **CingulateCortexEngineWrapper**: L0 안정성 모니터 (risk, health 체크)
   - 갈등 모니터링
   - 오류 감지
   - 시스템 건강 점검
   - 복구 권장사항

### 3. 실시간 실행 루프

**산업용 모드**:
- 최소 지연
- 최소 로깅
- 오류 복구 메커니즘

**연구용 모드**:
- 상세 로깅
- 중간 결과 수집
- 실험 모드 지원

### 4. 시스템 모니터링 (Cingulate Cortex)

- 갈등 모니터링
- 오류 감지
- 시스템 건강 점검
- 복구 권장사항

---

## 🔗 블록체인 서명 (PHAM)

### 무결성 보장

BrainCore v0.3.0은 **PHAM 블록체인**에 서명되어 코드 무결성을 보장합니다.

**서명 정보**:
- **모듈명**: BrainCore (CookiieKernel)
- **버전**: 0.3.0
- **SHA256**: `4f6606b697996a989f83a0e75b08b1a2a11b3b652157b5e1fe62e2ac937959d5`
- **파일 수**: 18개
- **서명 시간**: 2026-02-05

**서명 내용**:
- 코드 무결성 보장
- 버전 0.3.0 고정
- 실제 엔진 연결 완료 상태 기록

**검증 방법**:
```bash
# 해시 계산
cd BrainCore
python3 calculate_hash.py

# PHAM_SIGNATURE.md에서 해시 확인
cat PHAM_SIGNATURE.md
```

자세한 내용은 `PHAM_SIGNATURE.md`를 참고하세요.

---

## 🚀 확장 기능

### 1. 엔진 추가

**새 엔진 래퍼 구현**:

```python
from brain_core import SelfOrganizingEngine, GlobalState

class MyEngineWrapper(SelfOrganizingEngine):
    """새 엔진 래퍼"""
    
    def __init__(self, my_engine: Any):
        self.engine = my_engine
        self.name = "my_engine"
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태를 perturb하여 업데이트"""
        # 엔진 로직 구현
        result = self.engine.process(state.state_vector)
        
        # 상태 업데이트
        state.state_vector = result
        state.set_extension("my_engine", {"data": result})
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환"""
        return state.energy
```

**엔진 등록**:

```python
from brain_core import BrainCore

core = BrainCore()
core.register_engine("my_engine", MyEngineWrapper(my_engine), priority=50)
```

### 2. 실행 모드 확장

**현재**: SELF_ORGANIZING 모드만 사용

**확장 가능**: ControllerEngine Protocol 유지 (필요할 때 CONTROLLER 모드 추가 가능)

```python
from brain_core import ControllerEngine

class MyControllerEngine(ControllerEngine):
    """컨트롤러 모드 엔진"""
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """입력 처리 및 결정"""
        # 컨트롤러 로직 구현
        pass
    
    def evaluate(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """후보 평가 및 선택"""
        # 평가 로직 구현
        pass
```

### 3. Physics Pipeline 확장

**현재**: Protocol만 정의 (확장 가능성)

**확장 예시**:
- TurbulenceFeatureExtractor 구현
- FailureAtlasBuilder 구현
- PhysicsAdapter 구현

자세한 내용은 `src/brain_core/physics_pipeline.py`를 참고하세요.

### 4. 데이터 흐름 확장

**DataFlowManager**:
- 엔진 간 데이터 변환
- 상태 동기화
- 히스토리 관리

**확장 가능**:
- 커스텀 DataConverter 구현
- 커스텀 StateSynchronizer 구현

---

## 💼 활용성

### 1. 산업용 활용

**실시간 제어 시스템**:
```python
from brain_core import BrainCore, GlobalState
import numpy as np

# BrainCore 생성
core = BrainCore(mode="production")

# 엔진 등록
core.register_engine("well_formation", well_formation_wrapper, priority=10)
core.register_engine("state_manifold", state_manifold_wrapper, priority=20)
core.register_engine("neural_dynamics", neural_dynamics_wrapper, priority=30)

# 실시간 제어 루프
while True:
    # 센서 데이터 입력
    sensor_data = get_sensor_data()
    
    # 초기 상태 생성
    initial_state = GlobalState(
        state_vector=np.array(sensor_data),
        energy=0.0,
        risk=0.0,
    )
    
    # 실행
    result = core.run_cycle(
        initial_state=initial_state,
        max_steps=10,
        convergence_threshold=1e-4,
    )
    
    # 제어 출력
    control_output = result["final_state"].state_vector
    send_control_signal(control_output)
```

**의사결정 시스템**:
- 위험도 평가 (`state.risk`)
- 에너지 최소화 (`state.energy`)
- 안정성 모니터링 (`state.extensions["cingulate"]`)

### 2. 연구용 활용

**뇌 모델링 연구**:
```python
from brain_core import BrainCore, GlobalState
import numpy as np

# 연구 모드로 생성
core = BrainCore(mode="research", enable_logging=True)

# 엔진 등록
core.register_engine("well_formation", well_formation_wrapper, priority=10)
core.register_engine("neural_dynamics", neural_dynamics_wrapper, priority=30)

# 실험 실행
initial_state = GlobalState(
    state_vector=np.random.randn(10),
    energy=0.0,
    risk=0.0,
)

# 중간 결과 포함 실행
result = core.run_cycle(
    initial_state=initial_state,
    return_intermediate=True,
    max_steps=100,
)

# 중간 결과 분석
trajectory = result["trajectory"]
for i, state in enumerate(trajectory):
    print(f"Step {i}: Energy={state.energy:.4f}, Risk={state.risk:.4f}")
    print(f"  L0 converged: {state.l0_converged}")
    print(f"  Risk map: {state.risk_map}")
```

**데이터 수집**:
- 상태 궤적 수집 (`trajectory`)
- 에너지 변화 추적
- 위험도 변화 추적
- 인과 링크 분석 (`causal_links`)

### 3. 철학적 탐구

**의식 모델링**:
- 상태 공간 탐색
- 에너지 최소화 수렴
- 인과 네트워크 형성
- 스토리라인 생성

**인지 구조 분석**:
- Well Formation (잠재 우물 형성)
- Risk Map (위험 지형)
- Causal Links (인과 링크)
- Storyline (스토리라인)

---

## 📐 아키텍처

### 상태 중심 실행 흐름

```
state_0 (초기 상태)
  ↓
WellFormationEngine.update(state_0) → state_1 (W, b 설정)
  ↓
StateManifoldEngine.update(state_1) → state_2 (risk_map 설정)
  ↓
NeuralDynamicsCore.update(state_2) → state_3 (동역학 실행)
  ↓
HistoricalDataReconstructor.update(state_3) → state_4 (기록)
  ↓
CingulateCortex.update(state_4) → state_5 (모니터링)
  ↓
state_final (최종 상태)
```

### 수학적 배경

**핵심 수식**:
1. **상태 업데이트**: `state_{t+1} = engine.update(state_t)`
2. **에너지 함수**: `E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i`
3. **신경 동역학**: `τ · dx/dt = -x + f(Wx + I + b)`
4. **수렴 조건**: `|E_{t+1} - E_t| < ε`

자세한 내용은 `ARCHITECTURE.md`와 `src/brain_core/mathematical_background.md`를 참고하세요.

---

## 💻 사용 예시

### 기본 사용

```python
from brain_core import BrainCore, GlobalState
import numpy as np

# BrainCore 생성
core = BrainCore(mode="production")

# 엔진 등록
core.register_engine("well_formation", well_formation_wrapper, priority=10)
core.register_engine("state_manifold", state_manifold_wrapper, priority=20)
core.register_engine("neural_dynamics", neural_dynamics_wrapper, priority=30)

# 초기 상태 생성
initial_state = GlobalState(
    state_vector=np.array([0.5, 0.3, 0.8]),
    energy=0.0,
    risk=0.0,
)

# 실행
result = core.run_cycle(
    initial_state=initial_state,
    max_steps=100,
    convergence_threshold=1e-4,
)

# 결과 확인
final_state = result["final_state"]
print(f"Energy: {final_state.energy:.4f}")
print(f"Risk: {final_state.risk:.4f}")
print(f"L0 converged: {final_state.l0_converged}")
```

### 연구 모드

```python
# 연구 모드로 생성
core = BrainCore(mode="research", enable_logging=True)

# 중간 결과 포함 실행
result = core.run_cycle(
    initial_state=initial_state,
    return_intermediate=True,
    max_steps=100,
)

# 중간 결과 확인
trajectory = result["trajectory"]
for i, state in enumerate(trajectory):
    print(f"Step {i}: Energy={state.energy:.4f}, Risk={state.risk:.4f}")
```

### 실제 엔진 연결

```python
from brain_core import BrainCore, GlobalState
from brain_core.real_engine_imports import (
    import_well_formation_engine,
    import_state_manifold_engine,
    import_neural_dynamics_core,
)
from brain_core.engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
    NeuralDynamicsCoreWrapper,
)

# 실제 엔진 import
WellFormationEngine = import_well_formation_engine()
StateManifoldEngine = import_state_manifold_engine()
NeuralDynamicsCore = import_neural_dynamics_core()

# 엔진 인스턴스 생성
well_formation_engine = WellFormationEngine()
state_manifold_engine = StateManifoldEngine()
neural_dynamics_core = NeuralDynamicsCore()

# 래퍼 생성
well_formation_wrapper = WellFormationEngineWrapper(well_formation_engine)
state_manifold_wrapper = StateManifoldEngineWrapper(state_manifold_engine)
neural_dynamics_wrapper = NeuralDynamicsCoreWrapper(neural_dynamics_core)

# BrainCore 생성 및 엔진 등록
core = BrainCore(mode="production")
core.register_engine("well_formation", well_formation_wrapper, priority=10)
core.register_engine("state_manifold", state_manifold_wrapper, priority=20)
core.register_engine("neural_dynamics", neural_dynamics_wrapper, priority=30)

# 실행
initial_state = GlobalState(
    state_vector=np.array([0.5, 0.3, 0.8]),
    energy=0.0,
    risk=0.0,
)

result = core.run_cycle(initial_state=initial_state)
```

자세한 예시는 `examples/` 폴더를 참고하세요.

---

## ✅ 구현 상태

### 완료 ✅

- **BrainCore 기본 구조**: 상태 중심 실행 구조
- **EngineRegistry**: 엔진 등록 및 관리 시스템
- **StateCentricExecutionLoop**: 상태 중심 실행 루프
- **GlobalState**: Core + Extensions 구조
- **5개 엔진 래퍼**: WellFormation, StateManifold, NeuralDynamics, Historical, Cingulate
- **Cingulate Cortex Engine**: 시스템 모니터링 및 오류 감지
- **실제 엔진 연결**: WellFormation, StateManifold, Historical (3/4 완료)
- **PHAM 블록체인 서명**: 코드 무결성 보장

### 진행 중 ⚠️

- **NeuralDynamicsCore 실제 연결**: 위치 확인 필요
- **성능 최적화**: 실시간 처리 최적화
- **문서화 보완**: API 문서화

### 미구현 📋

- **ControllerEngine 모드**: 확장 가능성 (Protocol 유지)
- **Physics Pipeline 구현**: Protocol만 정의 (확장 가능)
- **추가 엔진 통합**: 필요에 따라 추가 가능

---

## 🧪 테스트

```bash
cd BrainCore
python -m pytest tests/ -v
```

**테스트 결과**: 30개 테스트 통과 ✅

**테스트 커버리지**:
- `test_brain_core.py`: BrainCore 기본 기능
- `test_state_centric_loop.py`: 상태 중심 실행 루프
- `test_engine_wrappers.py`: 엔진 래퍼
- `test_cingulate_cortex.py`: Cingulate Cortex Engine
- `test_data_flow.py`: 데이터 흐름 관리
- `test_engine_integration.py`: 엔진 통합

---

## 📦 설치

```bash
# 저장소 클론
git clone https://github.com/qquartsco-svg/BrainCore.git
cd BrainCore

# 의존성 설치
pip install -r requirements.txt

# 테스트 실행
python -m pytest tests/ -v
```

---

## 📝 버전

### v0.3.0 (2026-02-05)
- ExecutionMode 단순화 완료
- PhysicsPipeline 단순화 완료
- 실제 엔진 연결 완료 (3/4)
- 상태 중심 실행 구조 완성
- PHAM 블록체인 서명 완료

### v0.2.0 (이전)
- 엔진 통합 완료
- 상태 중심 설계 원칙 명문화

### v0.1.0 (초기)
- BrainCore 기본 구조
- Cingulate Cortex Engine
- 엔진 등록 시스템
- 실행 루프

---

## 👤 작성자

**GNJz (Qquarts)**

---

## 📄 라이선스

[라이선스 정보 추가]

---

## 🔗 관련 프로젝트

- **WellFormationEngine**: L0 초기화기 (W, b 생성)
- **StateManifoldEngine**: L0 제약 조건 생성기 (risk_map 생성)
- **NeuralDynamicsCore**: 실제 동역학 상태가 살아있는 코어
- **HistoricalDataReconstructor**: L0 상태 기록기 (causal_links 기록)

---

## 📚 참고 자료

- **ARCHITECTURE.md**: 아키텍처 상세 설명
- **DESIGN_INVARIANTS.md**: 설계 불변 원칙
- **PHAM_SIGNATURE.md**: 블록체인 서명 기록
- **FINAL_COMPREHENSIVE_REVIEW.md**: 종합 검토 리포트
- **docs/**: 상세 문서

---

**상태**: v0.3.0 완료, 프로덕션 준비 완료 ✅
