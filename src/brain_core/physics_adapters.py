"""
Physics Adapters - 물리 시뮬레이터 어댑터 인터페이스

난류/대류 접근을 위한 Protocol 정의

확장 가능성:
- Protocol만 정의 (Mock 구현 제거)
- 필요할 때 구현 가능
- 인터페이스는 명확히 정의

Author: GNJz (Qquarts)
Version: 0.2.0
"""

from __future__ import annotations

from typing import Dict, Any, Protocol, runtime_checkable
import numpy as np

from .physics_pipeline import (
    PhysicsAdapter,
    TurbulenceFeatureExtractor,
    FailureAtlasBuilder,
)

__version__ = "0.2.0"

# Mock 구현 제거
# Protocol만 유지하여 확장 가능성 보장
# 필요할 때 실제 구현 추가 가능

# 사용 예시:
# class MyPhysicsAdapter(PhysicsAdapter):
#     def generate_field(self, parameters: Dict[str, Any], time: float = 0.0) -> Dict[str, np.ndarray]:
#         # 실제 구현
#         pass
#     
#     def load_from_file(self, filepath: str) -> Dict[str, np.ndarray]:
#         # 실제 구현
#         pass
