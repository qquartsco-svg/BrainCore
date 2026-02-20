"""
State Centric Execution Loop - 상태계 중심 실행 루프

상태 중심 실행:
- 엔진들이 순차적으로 상태를 업데이트
- 수식: state_{t+1} = engine.update(state_t)
- 수렴 조건: |E_{t+1} - E_t| < ε

Author: GNJz (Qquarts)
Version: 0.2.0
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional, Tuple
import logging
import numpy as np

from .global_state import GlobalState
from .execution_modes import SelfOrganizingEngine

__version__ = "0.2.0"


class StateCentricExecutionLoop:
    """상태계 중심 실행 루프
    
    GlobalState를 입력받아 엔진들이 상태를 'perturb'하며 업데이트하는 루프.
    L0 중심의 자기조직화 시스템을 구현합니다.
    
    핵심 원칙:
    - 상태 중심 실행 (state_{t+1} = engine.update(state_t))
    - 에너지 최소화 수렴
    - 엔진은 상태를 perturb하여 변화
    """
    
    def __init__(
        self,
        enable_logging: bool = True,
    ):
        """StateCentricExecutionLoop 초기화
        
        Args:
            enable_logging: 로깅 활성화 여부
        """
        self.enable_logging = enable_logging
        if enable_logging:
            self.logger = logging.getLogger("StateCentricExecutionLoop")
        else:
            self.logger = None

    def run_cycle(
        self,
        initial_state: GlobalState,
        engines: Dict[str, SelfOrganizingEngine],
        max_steps: int = 100,
        convergence_threshold: float = 1e-4,
        return_trajectory: bool = False,
    ) -> Tuple[GlobalState, Optional[List[GlobalState]]]:
        """상태계 중심 실행 루프 실행
        
        수식:
        - 상태 업데이트: state_{t+1} = engine.update(state_t)
        - 수렴 조건: |E_{t+1} - E_t| < ε
        
        Args:
            initial_state: 초기 GlobalState
            engines: SelfOrganizingEngine 프로토콜을 따르는 엔진 딕셔너리 (순서 중요)
            max_steps: 최대 실행 스텝 수
            convergence_threshold: 수렴 임계값 (state_vector 변화량)
            return_trajectory: 전체 상태 궤적 반환 여부
        
        Returns:
            Tuple[GlobalState, Optional[List[GlobalState]]]: 최종 GlobalState와 (옵션) 상태 궤적
        """
        current_state = initial_state.copy(deep=True)  # 초기 상태 복사
        trajectory: List[GlobalState] = [current_state.copy()] if return_trajectory else []

        if self.logger:
            self.logger.info(f"StateCentricExecutionLoop 시작 (max_steps: {max_steps}, threshold: {convergence_threshold})")

        for step in range(max_steps):
            prev_state_vector = current_state.state_vector.copy()
            prev_energy = current_state.energy
            
            # 엔진 순서대로 상태 업데이트
            # 수식: state_{t+1} = engine.update(state_t)
            for name, engine in engines.items():
                if self.logger:
                    self.logger.debug(f"Step {step}, 엔진 {name} 업데이트 시작")
                try:
                    current_state = engine.update(current_state)
                    if self.logger:
                        self.logger.debug(f"Step {step}, 엔진 {name} 업데이트 완료. Risk: {current_state.risk:.3f}, Energy: {current_state.energy:.3f}")
                except Exception as e:
                    if self.logger:
                        self.logger.error(f"Step {step}, 엔진 {name} 업데이트 중 오류: {e}")
                    # 오류 발생 시 현재 상태 반환
                    return current_state, trajectory if return_trajectory else None
            
            current_state.update_step(step + 1)  # 스텝 및 타임스탬프 업데이트

            if return_trajectory:
                trajectory.append(current_state.copy())

            # 수렴 여부 확인 (에너지 기준)
            # 수식: |E_{t+1} - E_t| < ε
            energy_delta = abs(current_state.energy - prev_energy)
            state_vector_delta = np.linalg.norm(current_state.state_vector - prev_state_vector)
            
            if self.logger:
                self.logger.debug(f"Step {step}: Energy Delta = {energy_delta:.6f}, State Vector Delta = {state_vector_delta:.6f}, Risk = {current_state.risk:.3f}, Energy = {current_state.energy:.3f}")
            
            # 에너지 수렴 또는 상태 벡터 수렴
            if energy_delta < convergence_threshold or state_vector_delta < convergence_threshold:
                if self.logger:
                    self.logger.info(f"StateCentricExecutionLoop 수렴 완료 (스텝: {step+1})")
                return current_state, trajectory if return_trajectory else None

        if self.logger:
            self.logger.warning(f"StateCentricExecutionLoop 최대 스텝 도달 (수렴 실패)")
        return current_state, trajectory if return_trajectory else None
