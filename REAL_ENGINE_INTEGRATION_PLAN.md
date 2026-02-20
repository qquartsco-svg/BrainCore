# 실제 엔진 연결 계획

**작성일**: 2026-02-20  
**목적**: Mock 엔진 대신 실제 엔진 사용

---

## 🎯 목표

1. 실제 엔진 위치 확인
2. 실제 엔진 import 경로 설정
3. Mock 엔진 대신 실제 엔진 사용
4. 통합 테스트
5. 데모 실행

---

## 📋 작업 순서

### 1단계: 실제 엔진 위치 확인

**확인할 엔진**:
- WellFormationEngine
- StateManifoldEngine
- NeuralDynamicsCore
- HistoricalDataReconstructor
- CingulateCortexEngine (이미 구현됨)

**예상 위치**:
- `/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines/`
- 각 엔진별 폴더

---

### 2단계: 실제 엔진 import 경로 설정

**작업 내용**:
- 각 엔진의 메인 클래스 확인
- import 경로 설정
- 의존성 확인

---

### 3단계: Mock 엔진 대신 실제 엔진 사용

**작업 내용**:
- engine_wrappers.py에서 Mock 엔진 제거
- 실제 엔진 import 추가
- 예제에서 실제 엔진 사용

---

### 4단계: 통합 테스트

**작업 내용**:
- 실제 엔진 연결 테스트
- 통합 테스트 실행
- 오류 수정

---

### 5단계: 데모 실행

**작업 내용**:
- state_centric_demo.py에서 실제 엔진 사용
- 데모 실행 및 검증

---

## 🔧 구현 세부사항

### 엔진 래퍼 구조

현재 구조:
```python
class WellFormationEngineWrapper:
    def __init__(self, engine):
        self.engine = engine
    def update(self, state: GlobalState) -> GlobalState:
        # 상태 변환 및 엔진 실행
        ...
```

변경 후:
```python
# 실제 엔진 import
from well_formation_engine import WellFormationEngine

# 래퍼는 그대로 사용
wrapper = WellFormationEngineWrapper(WellFormationEngine(...))
```

---

## ✅ 검증 체크리스트

- [ ] 실제 엔진 위치 확인
- [ ] import 경로 설정
- [ ] Mock 엔진 제거
- [ ] 실제 엔진 연결 테스트
- [ ] 통합 테스트 통과
- [ ] 데모 실행 성공

---

**작성자**: GNJz (Qquarts)  
**상태**: 계획 수립 완료

