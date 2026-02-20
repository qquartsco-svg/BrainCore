"""
GlobalState - 공통 상태 표현 (Core + Extensions 구조)

모든 엔진이 공유하는 상태 벡터 정의
확장 가능한 구조: Core(최소 공통) + Extensions(엔진별 결과)

Author: GNJz (Qquarts)
Version: 0.2.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import numpy as np
import time

__version__ = "0.2.0"


@dataclass
class GlobalState:
    """공통 상태 표현 (Core + Extensions 구조)
    
    Core: 항상 있는 최소 공통 필드
    Extensions: 엔진별 결과를 담는 딕셔너리 (확장 가능)
    
    Attributes:
        # Core (최소 공통)
        state_vector: 공통 상태 벡터 (N차원)
        energy: 에너지 (Hopfield energy)
        risk: 위험도 (0.0 ~ 1.0)
        step: 시뮬레이션 스텝
        timestamp: 시간 스탬프
        metadata: 추가 정보
        
        # Extensions (엔진별 결과)
        extensions: 엔진별 확장 데이터 {engine_name: data}
    """
    # Core (최소 공통) - 항상 존재
    state_vector: np.ndarray  # 공통 상태 벡터 (N차원)
    energy: float = 0.0       # 에너지 (Hopfield energy)
    risk: float = 0.0         # 위험도 (0.0 ~ 1.0)
    step: int = 0             # 시뮬레이션 스텝
    timestamp: float = field(default_factory=time.time)  # 시간 스탬프
    metadata: Dict[str, Any] = field(default_factory=dict)  # 추가 정보
    
    # Extensions (엔진별 결과) - 확장 가능
    extensions: Dict[str, Any] = field(default_factory=dict)  # {engine_name: data}
    
    def get_extension(self, engine_name: str, default: Any = None) -> Any:
        """엔진별 확장 데이터 조회
        
        Args:
            engine_name: 엔진 이름
            default: 기본값
        
        Returns:
            확장 데이터
        """
        return self.extensions.get(engine_name, default)
    
    def set_extension(self, engine_name: str, data: Any):
        """엔진별 확장 데이터 설정
        
        Args:
            engine_name: 엔진 이름
            data: 확장 데이터
        """
        self.extensions[engine_name] = data
    
    def update_extension(self, engine_name: str, **kwargs):
        """엔진별 확장 데이터 부분 업데이트
        
        Args:
            engine_name: 엔진 이름
            **kwargs: 업데이트할 키-값 쌍
        """
        if engine_name not in self.extensions:
            self.extensions[engine_name] = {}
        self.extensions[engine_name].update(kwargs)
    
    def copy(self, deep: bool = False) -> 'GlobalState':
        """상태 복사
        
        Args:
            deep: True면 deep copy, False면 shallow copy (기본값)
        
        Returns:
            복사된 상태
        """
        if deep:
            # Deep copy (immutable snapshot 필요할 때만)
            return GlobalState(
                state_vector=self.state_vector.copy(),
                energy=self.energy,
                risk=self.risk,
                step=self.step,
                timestamp=self.timestamp,
                metadata=self.metadata.copy(),
                extensions={k: (v.copy() if hasattr(v, 'copy') else v) 
                           for k, v in self.extensions.items()},
            )
        else:
            # Shallow copy (참조 공유, 변경분 기록)
            return GlobalState(
                state_vector=self.state_vector,  # 참조 공유
                energy=self.energy,
                risk=self.risk,
                step=self.step,
                timestamp=self.timestamp,
                metadata=self.metadata.copy(),  # dict는 복사
                extensions=self.extensions.copy(),  # dict는 복사 (내부 참조는 공유)
            )
    
    def update_step(self, step: int):
        """스텝 업데이트"""
        self.step = step
        self.timestamp = time.time()
    
    def get_dimension(self) -> int:
        """상태 벡터 차원 반환"""
        return len(self.state_vector)
    
    def is_valid(self) -> bool:
        """상태 유효성 검사 (최소만)
        
        Core 필드만 검사. Extensions 검사는 Cingulate가 담당.
        
        Returns:
            유효성 여부
        """
        if self.state_vector is None or len(self.state_vector) == 0:
            return False
        if not (0.0 <= self.risk <= 1.0):
            return False
        return True
    
    # 편의 메서드: L0 관련 (extensions["L0"] 사용)
    @property
    def l0_weights(self) -> Optional[np.ndarray]:
        """L0 가중치 행렬"""
        l0_data = self.get_extension("L0")
        return l0_data.get("weights") if l0_data and isinstance(l0_data, dict) else None
    
    @property
    def l0_bias(self) -> Optional[np.ndarray]:
        """L0 바이어스 벡터"""
        l0_data = self.get_extension("L0")
        return l0_data.get("bias") if l0_data and isinstance(l0_data, dict) else None
    
    @property
    def l0_converged(self) -> bool:
        """L0 수렴 여부"""
        l0_data = self.get_extension("L0")
        return l0_data.get("converged", False) if l0_data and isinstance(l0_data, dict) else False
    
    # 편의 메서드: L1 관련 (extensions["L1"] 사용)
    @property
    def risk_map(self) -> Optional[Dict[str, float]]:
        """위험 지형"""
        l1_data = self.get_extension("L1")
        return l1_data.get("risk_map") if l1_data and isinstance(l1_data, dict) else None
    
    @property
    def manifold_dimensions(self) -> Optional[Dict[str, Any]]:
        """상태 공간 차원"""
        l1_data = self.get_extension("L1")
        return l1_data.get("dimensions") if l1_data and isinstance(l1_data, dict) else None
    
    # 편의 메서드: L2 관련 (extensions["L2"] 사용)
    @property
    def causal_links(self) -> Optional[List[Any]]:
        """인과 링크"""
        l2_data = self.get_extension("L2")
        return l2_data.get("causal_links") if l2_data and isinstance(l2_data, dict) else None
    
    @property
    def storyline(self) -> Optional[List[Any]]:
        """스토리라인"""
        l2_data = self.get_extension("L2")
        return l2_data.get("storyline") if l2_data and isinstance(l2_data, dict) else None
