# 단순화 작업 상세 계획

**작성일**: 2026-02-05  
**목적**: 엔지니어링 관점과 확장 가능성을 고려한 단순화

---

## 🎯 단순화 원칙

### 1. 확장 가능성 유지
- 현재 사용하지 않는 기능도 **인터페이스는 유지**
- 필요할 때 구현할 수 있도록 **Protocol만 정의**
- Mock 구현은 제거하되 **확장 포인트는 보존**

### 2. 엔지니어링 관점
- **단순함**: 현재 필요한 것만 구현
- **명확함**: 코드 의도가 명확
- **유지보수성**: 나중에 이해하기 쉬움

### 3. 큰 줄기 유지
- **상태 중심 설계 원칙** 유지
- **확장 가능한 구조** 유지
- **불필요한 복잡도만 제거**

---

## 📋 작업 1: ExecutionMode 단순화

### 현재 상태

**문제점**:
- CONTROLLER, SELF_ORGANIZING, HYBRID 모드 정의
- 현재는 SELF_ORGANIZING만 사용
- 과도한 추상화

**엔지니어링 관점**:
- YAGNI (You Aren't Gonna Need It) 원칙
- 현재 사용하지 않는 기능은 제거
- 필요할 때 확장 가능하도록 인터페이스만 유지

### 단순화 계획

**변경 사항**:
1. ExecutionMode를 SELF_ORGANIZING만 유지
2. ControllerEngine Protocol은 유지 (확장 가능성)
3. ExecutionModeManager 단순화
4. BrainCore에서 ExecutionMode 관련 코드 단순화

**확장 가능성**:
- ControllerEngine Protocol은 유지
- 필요할 때 CONTROLLER 모드 추가 가능
- 인터페이스는 그대로 유지

---

## 📋 작업 2: PhysicsPipeline 단순화

### 현재 상태

**문제점**:
- MockPhysicsAdapter 구현
- MockTurbulenceFeatureExtractor 구현
- MockFailureAtlasBuilder 구현
- 실제 사용 전에 Mock 구현

**엔지니어링 관점**:
- Mock 구현은 테스트용
- 실제 사용 전에는 Protocol만 정의
- 필요할 때 구현

### 단순화 계획

**변경 사항**:
1. Mock 구현 제거
2. Protocol만 유지 (확장 가능성)
3. 문서에 확장 방법 명시

**확장 가능성**:
- Protocol은 그대로 유지
- 필요할 때 구현 가능
- 인터페이스는 명확히 정의

---

## 🔧 구현 세부사항

### ExecutionMode 단순화

**변경 파일**:
- `src/brain_core/execution_modes.py`: 단순화
- `src/brain_core/brain_core.py`: ExecutionMode 관련 코드 단순화

**변경 내용**:
1. ExecutionMode를 SELF_ORGANIZING만 유지
2. ControllerEngine Protocol은 유지 (주석으로 확장 가능성 명시)
3. ExecutionModeManager 제거 또는 단순화
4. BrainCore에서 execution_mode 파라미터 제거

### PhysicsPipeline 단순화

**변경 파일**:
- `src/brain_core/physics_adapters.py`: Mock 구현 제거
- `src/brain_core/physics_pipeline.py`: Protocol만 유지

**변경 내용**:
1. Mock 구현 클래스 제거
2. Protocol만 유지
3. 확장 방법 문서화

---

## ✅ 검증 체크리스트

단순화 후 확인:

- [ ] 모든 테스트 통과
- [ ] 확장 가능성 유지 (Protocol 존재)
- [ ] 코드 복잡도 감소
- [ ] 문서 업데이트 완료

---

**작성자**: GNJz (Qquarts)  
**상태**: 단순화 계획 수립 완료

