"""
BrainCore - 뇌 코어 오케스트레이터

상태 중심 동역학 통합 인프라

핵심 원칙:
- The system is state-centric.
- BrainCore orchestrates updates over a shared GlobalState.
- Engines do not control the system; they perturb the state.

산업용 중심:
- 실시간 처리 우선
- 최소 로깅 (성능 중시)
- 오류 복구 메커니즘

연구용 확장:
- 상세 로깅 옵션
- 중간 결과 수집
- 실험 모드 지원

Author: GNJz (Qquarts)
Version: 0.3.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional, List
import logging

from .engine_registry import EngineRegistry
from .state_centric_execution_loop import StateCentricExecutionLoop
from .data_flow import DataFlowManager
from .global_state import GlobalState
from .engines.cingulate_cortex import CingulateCortexEngine

__version__ = "0.3.0"


class BrainCore:
    """뇌 코어 오케스트레이터
    
    상태 중심 동역학 통합 인프라
    
    핵심 원칙:
    - 상태 중심 실행 (state_{t+1} = engine.update(state_t))
    - 엔진은 상태를 perturb하여 변화
    - 최종 상태는 에너지 최소화 수렴
    """
    
    def __init__(
        self,
        mode: str = "production",
        enable_logging: bool = True,
    ):
        """BrainCore 초기화
        
        Args:
            mode: "production" (산업용) 또는 "research" (연구용)
            enable_logging: 로깅 활성화 여부
        
        Note:
            현재는 SELF_ORGANIZING 모드만 사용 (상태 중심 실행)
            필요할 때 CONTROLLER 모드 추가 가능 (ControllerEngine Protocol 유지)
        """
        self.mode = mode
        self.enable_logging = enable_logging
        
        # 컴포넌트 초기화
        self.registry = EngineRegistry()
        self.data_flow = DataFlowManager(mode=mode, enable_logging=enable_logging)
        self.state_centric_loop = StateCentricExecutionLoop(
            enable_logging=enable_logging,
        )
        
        # 로깅 설정
        if enable_logging:
            self.logger = logging.getLogger("BrainCore")
            self.logger.info(f"BrainCore 초기화 완료 (모드: {mode}, 실행 모드: self_organizing)")
        else:
            self.logger = None
        
        # Cingulate Cortex 자동 등록
        self.cingulate = CingulateCortexEngine(mode=mode)
        self.register_engine("cingulate", self.cingulate, priority=100)
    
    def register_engine(
        self,
        name: str,
        engine: Any,
        priority: int = 50,
    ):
        """엔진 등록
        
        Args:
            name: 엔진 이름
            engine: 엔진 인스턴스 (SelfOrganizingEngine Protocol 준수)
            priority: 우선순위 (낮을수록 먼저 실행)
        
        Note:
            엔진은 update(state: GlobalState) -> GlobalState 메서드를 가져야 함
        """
        self.registry.register(name, engine, priority)
        if self.logger:
            self.logger.info(f"엔진 등록: {name} (우선순위: {priority})")
    
    def run_cycle(
        self,
        initial_state: GlobalState,
        return_intermediate: bool = False,
        max_steps: int = 100,
        convergence_threshold: float = 1e-4,
    ) -> Dict[str, Any]:
        """실행 사이클
        
        상태 중심 실행:
        - 엔진들이 순차적으로 상태를 업데이트
        - 수식: state_{t+1} = engine.update(state_t)
        - 수렴 조건: |E_{t+1} - E_t| < ε
        
        Args:
            initial_state: 초기 상태 (필수)
            return_intermediate: 중간 결과 반환 여부
            max_steps: 최대 스텝 수
            convergence_threshold: 수렴 임계값
        
        Returns:
            실행 결과:
            - success: 성공 여부
            - final_state: 최종 상태
            - trajectory: 상태 궤적 (return_intermediate=True일 때)
            - mode: 실행 모드 ("self_organizing")
        """
        if initial_state is None:
            raise ValueError("initial_state는 필수입니다.")
        
        # 자기조직화 엔진 수집
        self_organizing_engines = [
            engine for engine in self.registry.get_engines().values()
            if hasattr(engine, 'update')
        ]
        
        if not self_organizing_engines:
            if self.logger:
                self.logger.warning("등록된 엔진이 없습니다.")
            return {
                "success": False,
                "final_state": initial_state,
                "mode": "self_organizing",
            }
        
        # 상태계 중심 실행
        result = self.state_centric_loop.run_cycle(
            initial_state=initial_state,
            engines={name: engine for name, engine in zip(
                [name for name, _ in self.registry.get_engines().items() if hasattr(_, 'update')],
                self_organizing_engines
            )},
            max_steps=max_steps,
            convergence_threshold=convergence_threshold,
            return_trajectory=return_intermediate,
        )
        
        if return_intermediate:
            final_state, trajectory = result
            return {
                "success": True,
                "final_state": final_state,
                "trajectory": trajectory,
                "mode": "self_organizing",
            }
        else:
            final_state, _ = result
            return {
                "success": True,
                "final_state": final_state,
                "mode": "self_organizing",
            }
    
    def get_system_state(self) -> Dict[str, Any]:
        """시스템 상태 반환
        
        Returns:
            시스템 상태 정보
        """
        return {
            "mode": self.mode,
            "execution_mode": "self_organizing",
            "registered_count": len(self.registry.get_engines()),
            "engines": list(self.registry.get_engines().keys()),
        }
