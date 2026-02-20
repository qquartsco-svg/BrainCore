"""
엔진 래퍼 테스트

Author: GNJz (Qquarts)
Version: 0.1.0
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core.global_state import GlobalState
from brain_core.engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
    NeuralDynamicsCoreWrapper,
    HistoricalDataReconstructorWrapper,
    CingulateCortexEngineWrapper,
)


class MockWellFormationEngine:
    """Mock WellFormationEngine"""
    
    def generate_well(self, episodes):
        class WellResult:
            def __init__(self):
                self.W = [[0.5, -0.3], [-0.3, 0.5]]
                self.b = [0.1, 0.1]
                self.analysis = {"test": True}
        return WellResult()


class MockStateManifoldEngine:
    """Mock StateManifoldEngine"""
    
    def build_state_space(self, search_biases):
        class StateManifold:
            def __init__(self):
                self.dimensions = {"test": {"risk_map": {"condition_1": 0.5}}}
                self.organic_connections = {}
                self.collapse_zones = []
        return StateManifold()


class MockNeuralDynamicsCore:
    """Mock NeuralDynamicsCore"""
    
    def run(self, x0, W, b):
        # 간단한 Mock: x0를 약간 변화시킴
        return [x0, [x + 0.01 for x in x0]]
    
    def hopfield_energy(self, x):
        return 0.5


class MockHistoricalReconstructor:
    """Mock HistoricalDataReconstructor"""
    
    def collect_fragment(self, content, source, timestamp):
        class Fragment:
            def __init__(self):
                self.content = content
                self.source = source
                self.timestamp = timestamp
        return Fragment()


class MockCingulateCortex:
    """Mock CingulateCortexEngine"""
    
    def monitor(self, data):
        return {
            "health_score": 0.9,
            "conflicts": [],
            "errors": [],
        }


class TestEngineWrappers:
    """엔진 래퍼 테스트"""
    
    def test_well_formation_wrapper(self):
        """WellFormationEngineWrapper 테스트"""
        mock_engine = MockWellFormationEngine()
        wrapper = WellFormationEngineWrapper(mock_engine)
        
        # 초기 상태 생성
        state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # Mock Episode 생성 (간단한 리스트로 시뮬레이션)
        class MockEpisode:
            def __init__(self):
                self.pre_activity = [0.5, 0.3]
                self.post_activity = [0.6, 0.4]
                self.timestamp = 0.0
        
        episodes = [MockEpisode()]
        state.set_extension("well_formation", {"episodes": episodes})
        
        # update 실행
        updated_state = wrapper.update(state)
        
        # 검증
        l0_data = updated_state.get_extension("L0")
        assert l0_data is not None
        assert l0_data.get("weights") is not None
        assert l0_data.get("bias") is not None
    
    def test_state_manifold_wrapper(self):
        """StateManifoldEngineWrapper 테스트"""
        mock_engine = MockStateManifoldEngine()
        wrapper = StateManifoldEngineWrapper(mock_engine)
        
        # 초기 상태 생성
        state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        state.set_extension("state_manifold", {"search_biases": {"test": {}}})
        
        # update 실행
        updated_state = wrapper.update(state)
        
        # 검증
        assert updated_state.risk_map is not None
    
    def test_neural_dynamics_wrapper(self):
        """NeuralDynamicsCoreWrapper 테스트"""
        mock_core = MockNeuralDynamicsCore()
        wrapper = NeuralDynamicsCoreWrapper(mock_core)
        
        # 초기 상태 생성 (L0 extension 포함)
        state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        state.set_extension("L0", {
            "weights": np.array([[0.5, -0.3], [-0.3, 0.5]]),
            "bias": np.array([0.1, 0.1]),
            "converged": False,
        })
        
        # update 실행
        updated_state = wrapper.update(state)
        
        # 검증
        assert updated_state.state_vector is not None
        assert updated_state.energy is not None
    
    def test_historical_wrapper(self):
        """HistoricalDataReconstructorWrapper 테스트"""
        mock_reconstructor = MockHistoricalReconstructor()
        wrapper = HistoricalDataReconstructorWrapper(mock_reconstructor)
        
        # 초기 상태 생성
        state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
            step=1,
        )
        
        # update 실행
        updated_state = wrapper.update(state)
        
        # 검증
        l2_data = updated_state.get_extension("L2")
        assert l2_data is not None
        assert "causal_links" in l2_data
    
    def test_cingulate_wrapper(self):
        """CingulateCortexEngineWrapper 테스트"""
        mock_cingulate = MockCingulateCortex()
        wrapper = CingulateCortexEngineWrapper(mock_cingulate)
        
        # 초기 상태 생성
        state = GlobalState(
            state_vector=np.array([0.5, 0.3]),
            energy=1.0,
        )
        
        # update 실행
        updated_state = wrapper.update(state)
        
        # 검증
        assert "monitoring" in updated_state.metadata
        assert updated_state.risk >= 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

