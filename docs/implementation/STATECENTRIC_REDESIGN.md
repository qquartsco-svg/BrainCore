# 상태계 중심 구조 재배치 설계안

**작성일**: 2026-02-05  
**목적**: "수액이 흐르는 생명체"로 진화하기 위한 재설계

---

## 1. 핵심 문제 정의

### 현재 문제

1. **공통 표현 공간 부재**
   - 엔진들이 서로 다른 언어 사용
   - 공통 상태 벡터 없음

2. **실행 루프가 컨트롤러 모델**
   - 순차 실행 파이프라인
   - 상태계가 아님

3. **L0가 중심이 아님**
   - BrainCore가 중심처럼 보임
   - L0가 위성 모듈처럼 취급됨

---

## 2. 설계 목표

### 목표 1: GlobalState 통일

모든 엔진이 공통 상태 표현을 사용

### 목표 2: 상태계 중심 실행

엔진이 상태를 perturb하는 모듈

### 목표 3: L0 중심 재정렬

L0가 중심, 나머지가 위성 모듈

---

## 3. GlobalState 정의

### 구조

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
import numpy as np

@dataclass
class GlobalState:
    """공통 상태 표현
    
    모든 엔진이 공유하는 상태 벡터
    """
    # 핵심 상태
    state_vector: np.ndarray  # 공통 상태 벡터 (N차원)
    energy: float             # 에너지 (Hopfield energy)
    risk: float               # 위험도 (0.0 ~ 1.0)
    
    # 메타데이터
    metadata: Dict[str, Any]  # 추가 정보
    
    # 시간 정보
    timestamp: float          # 시간 스탬프
    step: int                 # 시뮬레이션 스텝
    
    # L0 관련
    l0_weights: Optional[np.ndarray] = None  # W 행렬
    l0_bias: Optional[np.ndarray] = None     # b 벡터
    l0_converged: bool = False               # 수렴 여부
    
    # L1 관련
    risk_map: Optional[Dict[str, float]] = None  # 위험 지형
    manifold_dimensions: Optional[Dict[str, Any]] = None
    
    # L2 관련
    causal_links: Optional[list] = None  # 인과 링크
    storyline: Optional[list] = None     # 스토리라인
    
    def copy(self) -> 'GlobalState':
        """상태 복사"""
        return GlobalState(
            state_vector=self.state_vector.copy(),
            energy=self.energy,
            risk=self.risk,
            metadata=self.metadata.copy(),
            timestamp=self.timestamp,
            step=self.step,
            l0_weights=self.l0_weights.copy() if self.l0_weights is not None else None,
            l0_bias=self.l0_bias.copy() if self.l0_bias is not None else None,
            l0_converged=self.l0_converged,
            risk_map=self.risk_map.copy() if self.risk_map else None,
            manifold_dimensions=self.manifold_dimensions.copy() if self.manifold_dimensions else None,
            causal_links=self.causal_links.copy() if self.causal_links else None,
            storyline=self.storyline.copy() if self.storyline else None,
        )
```

---

## 4. 엔진 인터페이스 재정의

### 새로운 인터페이스

```python
class StateCentricEngine(Protocol):
    """상태계 중심 엔진 인터페이스"""
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태를 perturb하여 업데이트
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        ...
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        ...
    
    def reset(self):
        """상태 리셋"""
        ...
```

---

## 5. L0 중심 재정렬

### 구조

```
L0 (NeuralDynamicsCore) - 중심
  │
  ├── WellFormationEngine (초기화기)
  │   └── state.l0_weights, state.l0_bias 설정
  │
  ├── StateManifoldEngine (제약 조건 생성기)
  │   └── state.risk_map, state.manifold_dimensions 설정
  │
  ├── HistoricalDataReconstructor (상태 기록기)
  │   └── state.causal_links, state.storyline 기록
  │
  └── CingulateCortexEngine (안정성 모니터)
      └── state.risk, state.energy 모니터링
```

### 실행 순서

```python
# 1. WellFormation: L0 초기화
state = well_formation.update(state)  # W, b 설정

# 2. StateManifold: 제약 조건 생성
state = state_manifold.update(state)  # risk_map 설정

# 3. L0: 동역학 실행
state = l0_core.update(state)  # state_vector, energy 업데이트

# 4. Historical: 상태 기록
state = historical.update(state)  # causal_links 기록

# 5. Cingulate: 안정성 모니터링
state = cingulate.update(state)  # risk, health 체크
```

---

## 6. 상태계 중심 실행 루프

### 새로운 ExecutionLoop

```python
class StateCentricExecutionLoop:
    """상태계 중심 실행 루프"""
    
    def __init__(self, engines: List[StateCentricEngine]):
        self.engines = engines
    
    def run_cycle(
        self,
        initial_state: GlobalState,
        max_steps: int = 100,
        convergence_threshold: float = 1e-4,
    ) -> GlobalState:
        """상태계 실행 사이클
        
        Args:
            initial_state: 초기 상태
            max_steps: 최대 스텝 수
            convergence_threshold: 수렴 임계값
        
        Returns:
            최종 상태
        """
        state = initial_state.copy()
        
        for step in range(max_steps):
            # 각 엔진이 상태를 perturb
            for engine in self.engines:
                state = engine.update(state)
                state.step = step
                state.timestamp = time.time()
            
            # 수렴 체크
            if state.l0_converged:
                if abs(state.energy - previous_energy) < convergence_threshold:
                    break
            
            previous_energy = state.energy
        
        return state
```

---

## 7. 엔진별 update() 구현 예시

### WellFormationEngine

```python
class WellFormationEngine:
    def update(self, state: GlobalState) -> GlobalState:
        """L0 초기화 (W, b 설정)"""
        if state.l0_weights is None:
            # WellFormation으로 W, b 생성
            well_result = self.generate_well(episodes)
            state.l0_weights = np.array(well_result.W)
            state.l0_bias = np.array(well_result.b)
        return state
```

### StateManifoldEngine

```python
class StateManifoldEngine:
    def update(self, state: GlobalState) -> GlobalState:
        """제약 조건 생성 (risk_map 설정)"""
        if state.risk_map is None:
            # StateManifold로 risk_map 생성
            manifold = self.build_state_space(search_biases)
            state.risk_map = self._extract_risk_map(manifold)
            state.manifold_dimensions = manifold.dimensions
        return state
```

### NeuralDynamicsCore (L0)

```python
class NeuralDynamicsCore:
    def update(self, state: GlobalState) -> GlobalState:
        """동역학 실행 (state_vector, energy 업데이트)"""
        # L0 실행
        x_trajectory = self.run(
            x0=state.state_vector,
            W=state.l0_weights,
            b=state.l0_bias,
        )
        
        # 상태 업데이트
        state.state_vector = x_trajectory[-1]
        state.energy = self.hopfield_energy(state.state_vector)
        state.l0_converged = self._check_convergence(x_trajectory)
        
        return state
```

### HistoricalDataReconstructor

```python
class HistoricalDataReconstructor:
    def update(self, state: GlobalState) -> GlobalState:
        """상태 기록 (causal_links 기록)"""
        # 현재 상태를 DataFragment로 변환
        fragment = self.collect_fragment(
            content=f"State at step {state.step}",
            state_vector=state.state_vector,
            energy=state.energy,
        )
        
        # 인과 링크 분석
        if state.causal_links is None:
            state.causal_links = []
        state.causal_links.append(self._analyze_context([fragment]))
        
        return state
```

### CingulateCortexEngine

```python
class CingulateCortexEngine:
    def update(self, state: GlobalState) -> GlobalState:
        """안정성 모니터링 (risk, health 체크)"""
        # 모니터링
        monitoring = self.monitor({
            "state_vector": state.state_vector,
            "energy": state.energy,
            "risk_map": state.risk_map,
        })
        
        # 위험도 업데이트
        state.risk = monitoring.get("health_score", 0.0)
        
        # 메타데이터에 모니터링 결과 저장
        state.metadata["monitoring"] = monitoring
        
        return state
```

---

## 8. 마이그레이션 계획

### Phase 1: GlobalState 정의

1. `GlobalState` 클래스 구현
2. 모든 엔진이 `GlobalState` 사용하도록 수정

### Phase 2: 엔진 인터페이스 변경

1. `StateCentricEngine` Protocol 정의
2. 각 엔진에 `update(state: GlobalState) -> GlobalState` 구현

### Phase 3: 실행 루프 재구성

1. `StateCentricExecutionLoop` 구현
2. 기존 `ExecutionLoop`와 병행 운영

### Phase 4: L0 중심 재정렬

1. L0를 중심으로 엔진 순서 재정렬
2. WellFormation → StateManifold → L0 → Historical → Cingulate

### Phase 5: 통합 테스트

1. 전체 파이프라인 테스트
2. 성능 검증

---

## 9. 예상 효과

### Before (현재)

```
엔진별 다른 데이터 구조
  ↓
DataFlowManager가 변환
  ↓
복잡한 변환 로직
  ↓
엔진 간 상호작용 어려움
```

### After (재설계 후)

```
GlobalState (공통 상태)
  ↓
엔진이 상태를 perturb
  ↓
단순한 상태 업데이트
  ↓
엔진 간 자연스러운 상호작용
```

---

## 10. 구현 우선순위

### 우선순위 1: GlobalState 정의 ✅

- 가장 중요
- 모든 엔진 통합의 기반

### 우선순위 2: L0 중심 재정렬 ✅

- L0가 중심이 되도록 구조 변경
- WellFormation, StateManifold를 L0 초기화/제약 생성기로 재정의

### 우선순위 3: 상태계 중심 실행 루프 ✅

- `StateCentricExecutionLoop` 구현
- 엔진이 상태를 perturb하도록 변경

### 우선순위 4: 엔진별 update() 구현 ⚠️

- 각 엔진에 `update()` 메서드 구현
- 기존 인터페이스와 병행 운영

---

## 11. 결론

### 현재 상태

- 아키텍처 설계: 9/10 ✅
- 상태계 완성도: 4/10 ❌

### 목표 상태

- 아키텍처 설계: 9/10 (유지)
- 상태계 완성도: 9/10 (목표)

### 핵심 변화

**Before**: "줄기 설계 성공 단계"  
**After**: "에너지 흐름이 도는 생명체 단계"

---

**작성자**: GNJz (Qquarts)  
**상태**: 상태계 중심 구조 재배치 설계안 완료

