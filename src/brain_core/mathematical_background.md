# 수학적 배경

**작성일**: 2026-02-20  
**버전**: 0.2.0

---

## 1. GlobalState

### 상태 표현

**수식**:
```
GlobalState = {
    state_vector: x ∈ ℝ^N,      # 공통 상태 벡터
    energy: E ∈ ℝ,              # 에너지
    risk: r ∈ [0, 1],           # 위험도
    extensions: {engine: data}   # 엔진별 확장 데이터
}
```

**의미**:
- `state_vector`: 모든 엔진이 공유하는 상태 벡터
- `energy`: Hopfield 에너지
- `risk`: 시스템 위험도
- `extensions`: 엔진별 확장 데이터 (확장 가능)

---

## 2. WellFormationEngine

### Hebbian 학습

**수식**:
```
Δw_ij = η · pre_i · post_j - λ · w_ij
```

**여기서**:
- `η`: 학습률 (hebbian_config.eta)
- `λ`: 가중치 감쇠 계수 (hebbian_config.weight_decay)
- `pre_i`: pre-synaptic 뉴런 i의 활동
- `post_j`: post-synaptic 뉴런 j의 활동

### 에너지 함수

**수식**:
```
E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
```

**의미**:
- `W`: 연결 가중치 행렬
- `b`: 바이어스 벡터
- `x`: 뉴런 상태 벡터

---

## 3. StateManifoldEngine

### 위험도 통합

**수식**:
```
risk(condition) = f(risk_1(condition), risk_2(condition), ...)
```

**유기적 결합**:
```
risk_base = (1/n) · Σ_i risk_i(condition)
```

**유기적 증폭**:
```
risk_amplified = risk_base · (1 + (high_risk_count - 1) · 0.2)
```

**여기서**:
- `high_risk_count`: 위험도 > 0.7인 차원 수
- `0.2`: 증폭 계수

---

## 4. NeuralDynamicsCore (L0)

### 연속시간 동역학

**수식**:
```
τ · dx/dt = -x + f(Wx + I + b)
```

**여기서**:
- `τ`: 시간 상수
- `x`: 뉴런 상태 벡터
- `W`: 연결 가중치 행렬
- `I`: 외부 입력 벡터
- `b`: 바이어스 벡터
- `f`: 활성화 함수

### 에너지 함수

**수식**:
```
E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
```

### Lyapunov 안정성

**수식**:
```
dE/dt ≤ 0
```

**의미**: 동역학은 항상 에너지를 감소시키는 방향으로 진행

---

## 5. HistoricalDataReconstructor

### 인과 링크

**수식**:
```
causal_link = (fragment_i, fragment_j, strength)
```

**여기서**:
- `fragment_i`: 이전 데이터 단편
- `fragment_j`: 이후 데이터 단편
- `strength`: 인과 강도 (0.0 ~ 1.0)

### 스토리라인

**수식**:
```
storyline = [fragment_0, fragment_1, ..., fragment_n]
```

**의미**: 인과 링크를 따라 역추적하여 원인을 찾음

---

## 6. CingulateCortexEngine

### 건강 점수

**수식**:
```
health_score = 1.0 - (conflict_weight + error_weight)
```

**여기서**:
- `conflict_weight`: 갈등 가중치
- `error_weight`: 오류 가중치

### 위험도

**수식**:
```
risk = 1.0 - health_score
```

**의미**: 건강 점수가 낮을수록 위험도가 높음

---

## 7. 상태계 중심 실행

### 상태 업데이트

**수식**:
```
state_{t+1} = engine.update(state_t)
```

**의미**: 엔진이 상태를 perturb하여 변화

### 수렴 조건

**수식**:
```
|E_{t+1} - E_t| < ε
```

**여기서**:
- `E_t`: 시간 t에서의 에너지
- `ε`: 수렴 임계값 (convergence_threshold)

---

**작성자**: GNJz (Qquarts)  
**상태**: 수학적 배경 문서 작성 완료

