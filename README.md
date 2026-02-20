# BrainCore - 뇌 코어 오케스트레이터

**작성일**: 2026-02-05  
**버전**: 0.2.0  
**상태**: 엔진 통합 완료 (Mock 엔진용 래퍼 구현 완료)

---

## 📚 문서

- **README.md**: 전체 개요 (이 문서)
- **ARCHITECTURE.md**: 구조 설명 (수식 포함)
- **DESIGN_INVARIANTS.md**: 설계 불변 원칙 ⭐
- **PHAM_SIGNATURE.md**: 블록체인 서명

자세한 문서는 `docs/` 폴더를 참고하세요.

---

## 목적

개별 엔진들을 하나의 뇌로 통합하는 중앙 오케스트레이터

---

## 프로젝트 목표

**산업용 중심** + **연구/철학적 확장 가능**

- **산업용**: 실제 제어/의사결정 시스템, 실시간 처리, 안정성 중시
- **연구용**: 뇌 모델링 연구 도구, 실험 가능성, 데이터 수집
- **철학적**: 인지/의식 탐구, 이론적 완성도, 생물학적 정확성

---

## 핵심 기능

### 1. 엔진 통합 및 오케스트레이션

- 모든 뇌 엔진을 하나로 통합
- 우선순위 기반 실행
- 데이터 흐름 관리

### 2. 실시간 실행 루프

- 산업용: 최소 지연, 최소 로깅
- 연구용: 상세 로깅, 중간 결과 수집

### 3. 시스템 모니터링 (Cingulate Cortex)

- 갈등 모니터링
- 오류 감지
- 시스템 건강 점검
- 복구 권장사항

---

## 핵심 정체성

**상태 중심 동역학 통합 인프라**

- 오케스트레이터가 아니다
- 엔진 컨트롤러가 아니다
- **상태 공간 중심 시스템**이다

**핵심 원칙**:
- The system is state-centric.
- BrainCore orchestrates updates over a shared GlobalState.
- Engines do not control the system; they perturb the state.

---

## 아키텍처

```
입력
  ↓
Thalamus (입력 수집)
  ↓
Amygdala (감정 가중)
  ↓
Hippo_Memory (기억 검색)
  ↓
Basal_Ganglia (행동 후보 생성)
  ↓
PFC (실행 선택) [미구현]
  ↓
출력
  ↓
Cingulate Cortex (모니터링) ✅
  ↓
Dynamics_Engine (안정화)
```

---

## 사용 예시

### 기본 사용

```python
from brain_core import BrainCore

# BrainCore 생성
core = BrainCore(mode="production")

# 엔진 등록
core.register_engine("thalamus", thalamus_engine, priority=1)
core.register_engine("amygdala", amygdala_engine, priority=2)
core.register_engine("hippo_memory", hippo_memory_engine, priority=3)

# 실행
result = core.run_cycle(input_data={"sensor": 0.5})

# 시스템 상태 확인
state = core.get_system_state()
```

### 연구 모드

```python
# 연구 모드로 생성
core = BrainCore(mode="research")

# 중간 결과 포함 실행
result = core.run_cycle(
    input_data={"sensor": 0.5},
    return_intermediate=True
)

# 중간 결과 확인
print(result["intermediate"])
print(result["monitoring"])
```

---

## 구현 상태

### ✅ 완료

- BrainCore 기본 구조
- EngineRegistry (엔진 등록 시스템)
- ExecutionLoop (실행 루프)
- Cingulate Cortex Engine (모니터링)

### ⚠️ 진행 중

- 엔진 통합 테스트
- 성능 최적화

### 📋 미구현

- PFC (실행 선택 엔진)
- 실제 엔진 연결 (Thalamus, Amygdala 등)

---

## 테스트

```bash
cd BrainCore
python -m pytest tests/ -v
```

**테스트 결과**: 7개 테스트 통과 ✅

---

## 버전

- **v0.1.0**: 초기 구현
  - BrainCore 기본 구조
  - Cingulate Cortex Engine
  - 엔진 등록 시스템
  - 실행 루프

---

**작성자**: GNJz (Qquarts)  
**상태**: 기본 구조 완료, 엔진 통합 진행 중

