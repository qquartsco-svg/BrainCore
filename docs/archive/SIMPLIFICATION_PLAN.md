# 단순화 계획

**작성일**: 2026-02-20  
**목적**: "큰 줄기" 관점에서 불필요한 복잡도 제거

---

## 🎯 핵심 원칙

### "큰 줄기로 길을 만들어가는 형태"

**의미**:
- 디테일 확장은 언제든지 가능하게
- 현재 필요한 것만 구현
- 나머지는 인터페이스만 정의

---

## 📋 단순화 항목

### 1. ExecutionMode 단순화

**현재 상태**:
- CONTROLLER, SELF_ORGANIZING, HYBRID 모드 정의
- ExecutionModeManager 구현
- BrainCore에 통합

**문제점**:
- 현재는 SELF_ORGANIZING만 사용
- Controller 모드는 아직 미사용
- 과도한 추상화

**제안**:
- SELF_ORGANIZING만 유지
- Controller는 필요할 때 추가
- ExecutionModeManager는 단순화

**작업**:
- [ ] ExecutionMode 단순화 (SELF_ORGANIZING만)
- [ ] ExecutionModeManager 단순화
- [ ] BrainCore 단순화

---

### 2. PhysicsPipeline 단순화

**현재 상태**:
- MockPhysicsAdapter 구현
- MockTurbulenceFeatureExtractor 구현
- MockFailureAtlasBuilder 구현

**문제점**:
- 실제 사용 전에 Mock 구현
- 불필요한 복잡도

**제안**:
- 인터페이스만 정의 (Protocol만)
- Mock 구현 제거
- 필요할 때 구현

**작업**:
- [ ] Mock 구현 제거
- [ ] Protocol만 유지
- [ ] 문서 업데이트

---

### 3. 문서 통합

**현재 상태**:
- WORK_LOG.md
- CONCEPT_DOCUMENTATION.md
- mathematical_background.md
- PHAM_SIGNATURE.md
- PHAM_SIGNED.md
- IMPLEMENTATION_SUMMARY.md
- FINAL_COMPLETION_REPORT.md
- DIRECTIONAL_REVIEW.md
- SIMPLIFICATION_PLAN.md

**문제점**:
- 문서가 너무 많아서 혼란스러움
- 핵심 정보가 분산됨

**제안**:
- 핵심 문서만 유지
- 나머지는 필요할 때 참고용

**핵심 문서**:
- `README.md`: 전체 개요
- `ARCHITECTURE.md`: 구조 설명
- `PHAM_SIGNATURE.md`: 블록체인 서명

**작업**:
- [ ] 핵심 문서만 유지
- [ ] 나머지 문서는 참고용으로 정리

---

## 🎯 최종 구조 (단순화 후)

### 큰 줄기 (필수)

1. **GlobalState**
   - Core: state_vector, energy, risk
   - Extensions: 엔진별 확장 데이터

2. **StateCentricExecutionLoop**
   - `state_{t+1} = engine.update(state_t)`
   - 명확한 실행 순서

3. **엔진 래퍼**
   - WellFormationEngineWrapper
   - StateManifoldEngineWrapper
   - NeuralDynamicsCoreWrapper
   - HistoricalDataReconstructorWrapper
   - CingulateCortexEngineWrapper

### 확장 가능한 구조 (필요할 때)

1. **ExecutionMode**
   - 현재는 SELF_ORGANIZING만
   - 필요할 때 CONTROLLER 추가

2. **PhysicsPipeline**
   - 인터페이스만 정의 (Protocol)
   - 필요할 때 구현

---

## ✅ 작업 순서

1. **ExecutionMode 단순화**
   - SELF_ORGANIZING만 유지
   - ExecutionModeManager 단순화

2. **PhysicsPipeline 단순화**
   - Mock 구현 제거
   - Protocol만 유지

3. **문서 통합**
   - 핵심 문서만 유지
   - 나머지 정리

---

**작성자**: GNJz (Qquarts)  
**상태**: 단순화 계획 수립 완료

