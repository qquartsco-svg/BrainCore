# BrainCore 아키텍처

**작성일**: 2026-02-05  
**버전**: 0.2.0

---

## 🎯 핵심 정체성

### 이 시스템은 무엇인가?

**상태 중심 동역학 통합 인프라**

- 오케스트레이터가 아니다
- 엔진 컨트롤러가 아니다
- **상태 공간 중심 시스템**이다

**핵심 원칙**:
- The system is state-centric.
- BrainCore orchestrates updates over a shared GlobalState.
- Engines do not control the system; they perturb the state.

---

## 🎯 핵심 철학

### "확장 가능한 큰 줄기 만들기"

**의미**:
- 디테일 확장은 언제든지 가능하게
- 큰 줄기로 길을 만들어가는 형태
- 현재 필요한 것만 구현

---

## 📐 수학적 핵심

### 1. 상태 표현

```
GlobalState = {
    state_vector: x ∈ ℝ^N,      # 공통 상태 벡터
    energy: E ∈ ℝ,              # 에너지
    risk: r ∈ [0, 1],           # 위험도
    extensions: {engine: data}   # 엔진별 확장 데이터
}
```

**의미**: 모든 엔진이 공유하는 상태

---

### 2. 상태 업데이트

```
state_{t+1} = engine.update(state_t)
```

**의미**: 엔진이 상태를 perturb하여 변화

---

### 3. 수렴 조건

```
|E_{t+1} - E_t| < ε
```

**의미**: 에너지가 수렴하면 종료

---

## 🏗️ 구조적 핵심

### 1. GlobalState (Core + Extensions)

**Core** (최소 공통):
- `state_vector`: 공통 상태 벡터
- `energy`: 에너지
- `risk`: 위험도

**Extensions** (엔진별 확장):
- `L0`: W, b, converged
- `L1`: risk_map, dimensions
- `L2`: causal_links, storyline
- ...

**의미**: 필드 폭발 방지, 확장 가능

---

### 2. 상태계 중심 실행

**실행 순서**:
```
1. WellFormationEngine → L0 초기화 (W, b)
2. StateManifoldEngine → L1 제약 조건 (risk_map)
3. NeuralDynamicsCore → 동역학 실행 (state_vector, energy)
4. HistoricalDataReconstructor → L2 기록 (causal_links)
5. CingulateCortexEngine → 안정성 모니터 (risk, health)
```

**의미**: L0 중심 재정렬

---

### 3. 엔진 래퍼 패턴

**패턴**:
```python
class EngineWrapper(SelfOrganizingEngine):
    def update(self, state: GlobalState) -> GlobalState:
        # 상태 업데이트
        return state
```

**의미**: 기존 엔진을 쉽게 통합

---

## 🚀 확장 가능한 구조

### 필요할 때 추가 가능

1. **ExecutionMode**
   - 현재: SELF_ORGANIZING만
   - 필요할 때: CONTROLLER 추가

2. **PhysicsPipeline**
   - 현재: 인터페이스만 정의
   - 필요할 때: 구현

3. **기타 기능**
   - 필요할 때 확장

---

## 📁 파일 구조

```
BrainCore/
├── README.md              # 전체 개요
├── ARCHITECTURE.md        # 구조 설명 (이 문서)
├── DESIGN_INVARIANTS.md   # 설계 불변 원칙 ⭐
├── PHAM_SIGNATURE.md      # 블록체인 서명
├── src/                   # 소스 코드
│   └── brain_core/
├── tests/                 # 테스트
├── examples/              # 예제
└── docs/                  # 문서
    ├── phases/            # 단계별 완료 보고서
    ├── implementation/   # 구현 관련
    ├── concepts/         # 개념 문서
    ├── pham/             # PHAM 서명
    └── archive/          # 과거 문서
```

---

## 🔴 설계 불변 원칙

자세한 내용은 **DESIGN_INVARIANTS.md**를 참고하세요.

**핵심 불변 원칙**:
1. GlobalState는 최소 코어만 가진다
2. BrainCore는 상태를 소유하지 않는다
3. 엔진은 상태를 mutate하지만 지배하지 않는다
4. 실행 모델: 상태 업데이트 중심 (`state_{t+1} = engine.update(state_t)`)

---

## ✅ 핵심 원칙

1. **단순함**: 현재 필요한 것만 구현
2. **확장성**: 필요할 때 확장 가능
3. **명확함**: 수식과 구조가 명확

---

**작성자**: GNJz (Qquarts)  
**상태**: 아키텍처 문서 작성 완료

