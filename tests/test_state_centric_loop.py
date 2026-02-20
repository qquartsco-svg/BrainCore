"""
상태계 중심 실행 루프 테스트

Author: GNJz (Qquarts)
Version: 0.2.0
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core.global_state import GlobalState
from brain_core.state_centric_execution_loop import StateCentricExecutionLoop
from brain_core.execution_modes import SelfOrganizingEngine


class MockSelfOrganizingEngine:
    """Mock 자기조직화 엔진"""
    
    def __init__(self, name: str, energy_reduction: float = 0.1):
        self.name = name
        self.energy_reduction = energy_reduction
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태를 perturb하여 업데이트"""
        # 에너지 감소 시뮬레이션
        state.energy = max(0.0, state.energy - self.energy_reduction)
        
        # 상태 벡터 약간 변화
        state.state_vector = state.state_vector + np.random.randn(*state.state_vector.shape) * 0.01
        
        # Extension에 엔진 이름 기록
        state.set_extension(self.name, {"updated": True, "step": state.step})
        
        return state


class TestStateCentricExecutionLoop:
    """상태계 중심 실행 루프 테스트"""
    
    def test_basic_execution(self):
        """기본 실행 테스트"""
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3, 0.7]),
            energy=1.0,
            risk=0.5,
        )
        
        # Mock 엔진 생성
        engine1 = MockSelfOrganizingEngine("engine1", energy_reduction=0.1)
        engine2 = MockSelfOrganizingEngine("engine2", energy_reduction=0.05)
        
        # 실행 루프 생성
        loop = StateCentricExecutionLoop()
        
        # 실행 (engines 딕셔너리로 전달)
        final_state, _ = loop.run_cycle(
            initial_state=initial_state,
            engines={"engine1": engine1, "engine2": engine2},
            max_steps=10,
            convergence_threshold=0.01,
        )
        
        # 검증
        assert final_state.energy < initial_state.energy  # 에너지 감소
        assert final_state.step >= 0
        assert "engine1" in final_state.extensions
        assert "engine2" in final_state.extensions
    
    def test_convergence(self):
        """수렴 테스트"""
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # 에너지를 빠르게 감소시키는 엔진
        engine = MockSelfOrganizingEngine("engine", energy_reduction=0.2)
        
        # 실행 루프 생성
        loop = StateCentricExecutionLoop()
        
        # 실행
        final_state, _ = loop.run_cycle(
            initial_state=initial_state,
            engines={"engine": engine},
            max_steps=100,
            convergence_threshold=0.01,
        )
        
        # 검증: 수렴했거나 최대 스텝에 도달
        assert final_state.step < 100 or final_state.energy < 0.01
    
    def test_trajectory(self):
        """궤적 반환 테스트"""
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # Mock 엔진 생성
        engine = MockSelfOrganizingEngine("engine", energy_reduction=0.1)
        
        # 실행 루프 생성
        loop = StateCentricExecutionLoop()
        
        # 실행 (궤적 반환)
        final_state, trajectory = loop.run_cycle(
            initial_state=initial_state,
            engines={"engine": engine},
            max_steps=5,
            return_trajectory=True,
        )
        
        # 검증
        assert len(trajectory) > 0
        assert trajectory[0].energy == initial_state.energy
        assert trajectory[-1].energy == final_state.energy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
