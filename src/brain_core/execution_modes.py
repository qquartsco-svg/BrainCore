"""
Execution Modes - 실행 모드 정의

Self-organizing 모드 지원 (상태 중심 실행)

확장 가능성:
- ControllerEngine Protocol은 유지 (필요할 때 CONTROLLER 모드 추가 가능)
- 현재는 SELF_ORGANIZING만 사용

Author: GNJz (Qquarts)
Version: 0.2.0
"""

from __future__ import annotations

from typing import Dict, Any, List, Protocol, runtime_checkable
from enum import Enum

from .global_state import GlobalState

__version__ = "0.2.0"


# 현재는 SELF_ORGANIZING만 사용
# 필요할 때 CONTROLLER, HYBRID 모드 추가 가능
class ExecutionMode(Enum):
    """실행 모드"""
    SELF_ORGANIZING = "self_organizing"  # 자기조직화 상태계 모드 (현재 사용)


@runtime_checkable
class ControllerEngine(Protocol):
    """컨트롤러 모드 엔진 인터페이스 (확장 가능성)
    
    현재는 사용하지 않지만, 필요할 때 CONTROLLER 모드 추가를 위해 Protocol 유지.
    
    입력→평가→선택→출력 구조
    """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """입력 처리 및 결정
        
        Args:
            input_data: 입력 데이터
        
        Returns:
            처리 결과 및 결정
        """
        ...
    
    def evaluate(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """후보 평가 및 선택
        
        Args:
            candidates: 후보 리스트
        
        Returns:
            선택된 후보
        """
        ...


@runtime_checkable
class SelfOrganizingEngine(Protocol):
    """자기조직화 상태계 모드 엔진 인터페이스
    
    상태 갱신/에너지 최소/어트랙터 수렴
    
    핵심 원칙:
    - 엔진은 상태를 perturb하여 변화시킴
    - 상태의 최종 형태는 엔진들의 상호작용 결과
    """
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태를 perturb하여 업데이트
        
        수식: state_{t+1} = engine.update(state_t)
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태
        """
        ...
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 계산
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        ...


# ExecutionModeManager 제거
# 현재는 SELF_ORGANIZING만 사용하므로 별도 관리자 불필요
# 필요할 때 다시 추가 가능
