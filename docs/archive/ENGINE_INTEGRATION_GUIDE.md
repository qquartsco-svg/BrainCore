# 엔진 통합 가이드

**작성일**: 2026-02-05  
**목적**: 기존 엔진들을 BrainCore에 통합하는 방법

---

## 1. 엔진 위치

### Cognitive_Kernel 엔진

- `/Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel/Thalamus/`
- `/Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel/Amygdala/`
- `/Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel/BasalGanglia/`

### Independent Engines

- `/Users/jazzin/Desktop/00_BRAIN/Engines/Independent/6.Thalamus_Engine/`
- `/Users/jazzin/Desktop/00_BRAIN/Engines/Independent/7.Amygdala_Engine/`

---

## 2. 통합 방법

### 방법 1: EngineAdapter 사용 (권장)

기존 엔진을 `EngineAdapter`로 감싸서 통합:

```python
from brain_core import BrainCore
from brain_core.engine_adapters import EngineAdapter

# 기존 엔진 import
from thalamus import ThalamusEngine
from amygdala import AmygdalaEngine

# BrainCore 생성
core = BrainCore(mode="production")

# 엔진 어댑터로 감싸서 등록
thalamus_engine = ThalamusEngine(...)
thalamus_adapter = EngineAdapter(
    engine=thalamus_engine,
    name="thalamus",
    mode="production",
)
core.register_engine("thalamus", thalamus_adapter, priority=1)

amygdala_engine = AmygdalaEngine(...)
amygdala_adapter = EngineAdapter(
    engine=amygdala_engine,
    name="amygdala",
    mode="production",
)
core.register_engine("amygdala", amygdala_adapter, priority=2)

# 실행
result = core.run_cycle({"input": 0.5})
```

### 방법 2: 직접 인터페이스 구현

기존 엔진이 `BrainEngine` 인터페이스를 직접 구현:

```python
from brain_core.interfaces import BrainEngineBase

class MyEngine(BrainEngineBase):
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # 엔진 로직
        return {"output": input_data["input"] * 2}
```

---

## 3. 인터페이스 확인

### 필수 메서드

모든 엔진은 다음 메서드를 구현해야 함:

1. **`process(input_data: Dict[str, Any]) -> Dict[str, Any]`**
   - 입력 처리 메서드

2. **`get_state() -> Dict[str, Any]`** (선택적)
   - 현재 상태 반환

3. **`reset()`** (선택적)
   - 상태 리셋

### 확인 방법

```python
from brain_core.interfaces import BrainEngine

# 인터페이스 준수 확인
if isinstance(engine, BrainEngine):
    print("인터페이스 준수")
else:
    print("어댑터 필요")
```

---

## 4. 통합 체크리스트

### 각 엔진별 확인

- [ ] 엔진 위치 확인
- [ ] 인터페이스 확인 (`process`, `get_state`, `reset`)
- [ ] EngineAdapter로 감싸기 또는 직접 구현
- [ ] BrainCore에 등록
- [ ] 우선순위 설정
- [ ] 통합 테스트

---

## 5. 우선순위 가이드

### 권장 우선순위

| 엔진 | 우선순위 | 이유 |
|------|----------|------|
| Thalamus | 1 | 입력 수집 (가장 먼저) |
| Amygdala | 2 | 감정 가중 |
| Hippo_Memory | 3 | 기억 검색 |
| Basal_Ganglia | 4 | 행동 후보 생성 |
| PFC | 5 | 실행 선택 (미구현) |
| Cingulate Cortex | 100 | 모니터링 (가장 나중) |

---

## 6. 예시

### Thalamus 통합

```python
# Thalamus 엔진 import
import sys
sys.path.insert(0, "/Users/jazzin/Desktop/00_BRAIN/Cognitive_Kernel/Thalamus/src")
from thalamus import ThalamusEngine

# BrainCore 생성
core = BrainCore(mode="production")

# Thalamus 엔진 생성 및 등록
thalamus = ThalamusEngine(...)
thalamus_adapter = EngineAdapter(
    engine=thalamus,
    name="thalamus",
    mode="production",
)
core.register_engine("thalamus", thalamus_adapter, priority=1)
```

---

**작성자**: GNJz (Qquarts)  
**상태**: 통합 가이드 작성 완료

