# 개념 문서

**작성일**: 2026-02-20  
**버전**: 0.2.0

---

## 1. 상태계 중심 구조

### 핵심 개념

**"수액이 흐르는 생명체"**:
- GlobalState: 공통 상태 표현 (혈액)
- 엔진: 상태를 perturb하는 모듈 (장기)
- L0: 실제 동역학 상태가 살아있는 코어 (심장)

### 수학적 표현

**상태 업데이트**:
```
state_{t+1} = engine.update(state_t)
```

**의미**:
- 각 엔진이 상태를 조금씩 변화시킴
- 최종적으로 안정 어트랙터로 수렴

---

## 2. L0 중심 재정렬

### 구조

```
L0 (NeuralDynamicsCore) - 중심 (심장)
  │
  ├── WellFormationEngine (초기화기)
  │   └── W, b 설정
  │
  ├── StateManifoldEngine (제약 조건 생성기)
  │   └── risk_map 설정
  │
  ├── HistoricalDataReconstructor (상태 기록기)
  │   └── causal_links 기록
  │
  └── CingulateCortexEngine (안정성 모니터)
      └── risk, health 체크
```

### 실행 순서

1. **WellFormationEngine**: L0 초기화 (W, b 설정)
2. **StateManifoldEngine**: 제약 조건 생성 (risk_map 설정)
3. **NeuralDynamicsCore**: 동역학 실행 (state_vector, energy 업데이트)
4. **HistoricalDataReconstructor**: 상태 기록 (causal_links 기록)
5. **CingulateCortexEngine**: 안정성 모니터링 (risk, health 체크)

---

## 3. GlobalState (Core + Extensions)

### Core (최소 공통)

```python
Core = {
    state_vector: np.ndarray,  # 공통 상태 벡터
    energy: float,              # 에너지
    risk: float,                # 위험도
    step: int,                  # 시뮬레이션 스텝
    timestamp: float,           # 시간 스탬프
    metadata: dict,             # 추가 정보
}
```

### Extensions (엔진별 결과)

```python
Extensions = {
    "L0": {
        "weights": W,
        "bias": b,
        "converged": bool,
    },
    "L1": {
        "risk_map": {...},
        "dimensions": {...},
    },
    "L2": {
        "causal_links": [...],
        "storyline": [...],
    },
    ...
}
```

**의미**: 엔진이 늘어나도 GlobalState의 필드가 폭발하지 않음

---

## 4. 실행 모드

### Controller 모드

**특징**:
- 입력→평가→선택→출력 구조
- 정책/우선순위로 선택
- 디버깅/안전/재현성 좋음

**수식**:
```
output = evaluate(candidates)
selected = select(output, policy)
```

### Self-organizing 모드

**특징**:
- 상태 갱신/에너지 최소/어트랙터 수렴
- 상태가 수렴/어트랙터로 들어감
- 난류/대류 같은 비선형 문제에 적합

**수식**:
```
state_{t+1} = engine.update(state_t)
E_{t+1} ≤ E_t (에너지 감소)
```

### Hybrid 모드

**특징**:
- Controller와 Self-organizing 둘 다 실행
- 모드/엔진 조합으로 정의

---

## 5. 난류/대류 접근

### 현재 가능한 것

**"난류 데이터를 학습 대상으로 사용"**:
- StateManifold: 난류 지형 매핑
- WellFormation: 난류 패턴 학습
- Historical: 난류 인과 추적
- Cingulate: 난류 영향 모니터링

### 필요한 것 (3종)

1. **Physics/PDE Adapter**: 물리 시뮬레이터 (또는 외부 CFD 결과)
2. **Turbulence Feature Extractor**: 난류 특징 추출
3. **FailureAtlas/RiskMap Builder**: 특징 → FailureAtlas 변환

**의미**: 이 3종만 추가되면 난류/대류 연구 루프 가능

---

## 6. 확장 가능한 큰 줄기

### 철학

**"어느 한 방향으로 정하고 가는게 아니야"**:
- 특정 목적에 고정하지 않음
- 확장 가능한 기반 구조 구축
- 여러 방향으로 확장 가능

**"확장 가능한 큰 줄기를 만들어가는거야"**:
- BrainCore: 강력한 줄기 (통합 인프라)
- 인터페이스: 표준화된 연결점
- 엔진들: 독립적이면서 통합 가능한 가지들
- 미래: 어떤 방향으로든 확장 가능

---

**작성자**: GNJz (Qquarts)  
**상태**: 개념 문서 작성 완료

