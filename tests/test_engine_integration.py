"""
엔진 통합 테스트

기존 엔진들을 BrainCore에 통합하는 테스트

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

from brain_core import BrainCore, GlobalState
from brain_core.execution_modes import SelfOrganizingEngine


class MockSelfOrganizingEngine:
    """Mock 자기조직화 엔진"""
    
    def __init__(self, name: str, energy_reduction: float = 0.1):
        self.name = name
        self.energy_reduction = energy_reduction
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태를 perturb하여 업데이트"""
        state.energy = max(0.0, state.energy - self.energy_reduction)
        state.state_vector = state.state_vector + np.random.randn(*state.state_vector.shape) * 0.01
        state.set_extension(self.name, {"updated": True})
        return state


class TestEngineIntegration:
    """엔진 통합 테스트"""
    
    def test_basic_integration(self):
        """기본 통합 테스트"""
        core = BrainCore(mode="production")
        
        # Mock 엔진 생성 및 등록
        engine1 = MockSelfOrganizingEngine("engine1", energy_reduction=0.1)
        engine2 = MockSelfOrganizingEngine("engine2", energy_reduction=0.05)
        
        core.register_engine("engine1", engine1, priority=1)
        core.register_engine("engine2", engine2, priority=2)
        
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3, 0.7]),
            energy=1.0,
            risk=0.5,
        )
        
        # 실행
        result = core.run_cycle(
            initial_state=initial_state,
            max_steps=10,
            convergence_threshold=0.01,
        )
        
        assert result["success"] is True
        assert "final_state" in result
        assert result["final_state"].energy < initial_state.energy
    
    def test_engine_chain(self):
        """엔진 체인 테스트"""
        core = BrainCore(mode="research")
        
        # 여러 엔진 등록
        engines = [
            ("engine1", 1, 0.1),
            ("engine2", 2, 0.05),
            ("engine3", 3, 0.03),
        ]
        
        for name, priority, energy_reduction in engines:
            engine = MockSelfOrganizingEngine(name, energy_reduction=energy_reduction)
            core.register_engine(name, engine, priority=priority)
        
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # 실행
        result = core.run_cycle(
            initial_state=initial_state,
            max_steps=10,
            convergence_threshold=0.01,
            return_intermediate=True,
        )
        
        assert result["success"] is True
        assert "trajectory" in result
        assert len(result["trajectory"]) > 0
    
    def test_error_handling(self):
        """오류 처리 테스트"""
        core = BrainCore(mode="production")
        
        # 오류 발생 엔진
        class ErrorEngine:
            def update(self, state: GlobalState) -> GlobalState:
                raise ValueError("테스트 오류")
        
        error_engine = ErrorEngine()
        core.register_engine("error_engine", error_engine, priority=1)
        
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # 실행 (오류가 있어도 결과 반환)
        result = core.run_cycle(
            initial_state=initial_state,
            max_steps=10,
            convergence_threshold=0.01,
        )
        
        # 산업용: 오류가 있어도 결과 반환
        assert "final_state" in result
    
    def test_monitoring_integration(self):
        """모니터링 통합 테스트"""
        core = BrainCore(mode="research")
        
        # 엔진 등록
        engine = MockSelfOrganizingEngine("engine", energy_reduction=0.1)
        core.register_engine("engine", engine, priority=1)
        
        # 초기 상태 생성
        initial_state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # 실행
        result = core.run_cycle(
            initial_state=initial_state,
            max_steps=10,
            convergence_threshold=0.01,
            return_intermediate=True,
        )
        
        # 모니터링 결과 확인
        assert "trajectory" in result or "final_state" in result
    
    def test_system_state(self):
        """시스템 상태 테스트"""
        core = BrainCore(mode="production")
        
        # 엔진 등록
        engine = MockSelfOrganizingEngine("engine", energy_reduction=0.1)
        core.register_engine("engine", engine, priority=1)
        
        # 시스템 상태 확인
        state = core.get_system_state()
        
        assert "engines" in state
        assert "engine" in state["engines"]
        assert "cingulate" in state["engines"]  # 자동 등록된 cingulate
        assert state["registered_count"] >= 2  # engine + cingulate


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
