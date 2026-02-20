"""
상태계 중심 실행 데모

엔진 래퍼를 사용한 상태계 중심 실행 데모

Author: GNJz (Qquarts)
Version: 0.1.0
"""

import sys
from pathlib import Path
import numpy as np

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core import (
    BrainCore,
    GlobalState,
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


def main():
    """상태계 중심 실행 데모"""
    print("=" * 60)
    print("상태계 중심 실행 데모")
    print("=" * 60)
    print()
    
    # BrainCore 생성 (상태 중심 실행)
    print("1. BrainCore 생성 (상태 중심 실행)")
    print("-" * 60)
    core = BrainCore(mode="research")
    print(f"✅ BrainCore 생성 완료 (실행 모드: self_organizing)")
    print()
    
    # Mock 엔진 생성 및 래핑
    print("2. 엔진 생성 및 래핑")
    print("-" * 60)
    
    well_formation = WellFormationEngineWrapper(MockWellFormationEngine())
    state_manifold = StateManifoldEngineWrapper(MockStateManifoldEngine())
    neural_dynamics = NeuralDynamicsCoreWrapper(MockNeuralDynamicsCore())
    historical = HistoricalDataReconstructorWrapper(MockHistoricalReconstructor())
    cingulate = CingulateCortexEngineWrapper(MockCingulateCortex())
    
    # 엔진 등록 (cingulate는 이미 자동 등록되어 있으므로 제외)
    core.register_engine("well_formation", well_formation, priority=1)
    core.register_engine("state_manifold", state_manifold, priority=2)
    core.register_engine("neural_dynamics", neural_dynamics, priority=3)
    core.register_engine("historical", historical, priority=4)
    # cingulate는 BrainCore 초기화 시 자동 등록됨
    
    print("✅ 엔진 등록 완료")
    print(f"   - WellFormationEngine (L0 초기화기)")
    print(f"   - StateManifoldEngine (제약 조건 생성기)")
    print(f"   - NeuralDynamicsCore (동역학 실행)")
    print(f"   - HistoricalDataReconstructor (상태 기록기)")
    print(f"   - CingulateCortexEngine (안정성 모니터)")
    print()
    
    # 초기 상태 생성
    print("3. 초기 상태 생성")
    print("-" * 60)
    initial_state = GlobalState(
        state_vector=np.array([0.5, 0.3]),
        energy=1.0,
        risk=0.5,
    )
    initial_state.set_extension("well_formation", {"episodes": []})
    initial_state.set_extension("state_manifold", {"search_biases": {"test": {}}})
    
    print(f"✅ 초기 상태 생성 완료")
    print(f"   - state_vector: {initial_state.state_vector}")
    print(f"   - energy: {initial_state.energy}")
    print(f"   - risk: {initial_state.risk}")
    print()
    
    # 상태계 실행
    print("4. 상태계 실행")
    print("-" * 60)
    result = core.run_cycle(
        initial_state=initial_state,
        max_steps=10,
        convergence_threshold=0.01,
        return_intermediate=True,
    )
    
    final_state = result["final_state"]
    trajectory = result.get("trajectory", [])
    
    print(f"✅ 실행 완료")
    print(f"   - 최종 스텝: {final_state.step}")
    print(f"   - 최종 에너지: {final_state.energy:.4f}")
    print(f"   - 최종 위험도: {final_state.risk:.4f}")
    print(f"   - 궤적 길이: {len(trajectory)}")
    print()
    
    # Extensions 확인
    print("5. Extensions 확인")
    print("-" * 60)
    print(f"   - L0: {final_state.l0_weights is not None}")
    print(f"   - L1: {final_state.risk_map is not None}")
    print(f"   - L2: {final_state.causal_links is not None}")
    print(f"   - Monitoring: {'monitoring' in final_state.metadata}")
    print()
    
    # 궤적 확인
    print("6. 궤적 확인")
    print("-" * 60)
    print(f"   - 초기 에너지: {trajectory[0].energy:.4f}")
    print(f"   - 최종 에너지: {trajectory[-1].energy:.4f}")
    print(f"   - 에너지 변화: {trajectory[0].energy - trajectory[-1].energy:.4f}")
    print()
    
    print("=" * 60)
    print("✅ 상태계 중심 실행 데모 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

