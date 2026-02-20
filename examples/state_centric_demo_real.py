"""
상태계 중심 실행 데모 (실제 엔진 사용)

실제 엔진들을 사용한 상태계 중심 실행 데모

Author: GNJz (Qquarts)
Version: 0.2.0
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
from brain_core.real_engine_imports import (
    import_well_formation_engine,
    import_state_manifold_engine,
    import_historical_data_reconstructor,
    import_neural_dynamics_core,
)


def main():
    """메인 함수"""
    print("=" * 60)
    print("상태계 중심 실행 데모 (실제 엔진 사용)")
    print("=" * 60)
    print()
    
    # BrainCore 생성 (상태 중심 실행)
    print("1. BrainCore 생성 (상태 중심 실행)")
    print("-" * 60)
    core = BrainCore(mode="research")
    print(f"✅ BrainCore 생성 완료 (실행 모드: self_organizing)")
    print()
    
    # 실제 엔진 import 및 생성
    print("2. 실제 엔진 생성 및 래핑")
    print("-" * 60)
    
    # WellFormationEngine
    WellFormationEngine = import_well_formation_engine()
    if WellFormationEngine:
        well_formation_engine = WellFormationEngine()
        well_formation = WellFormationEngineWrapper(well_formation_engine)
        print("✅ WellFormationEngine 생성 완료")
    else:
        print("⚠️  WellFormationEngine import 실패 - Mock 사용")
        # Mock 엔진 사용
        class MockWellFormationEngine:
            def generate_well(self, episodes):
                class WellResult:
                    def __init__(self):
                        self.W = [[0.5, -0.3], [-0.3, 0.5]]
                        self.b = [0.1, 0.1]
                        self.analysis = {"test": True}
                return WellResult()
        well_formation = WellFormationEngineWrapper(MockWellFormationEngine())
    
    # StateManifoldEngine
    StateManifoldEngine = import_state_manifold_engine()
    if StateManifoldEngine:
        state_manifold_engine = StateManifoldEngine()
        state_manifold = StateManifoldEngineWrapper(state_manifold_engine)
        print("✅ StateManifoldEngine 생성 완료")
    else:
        print("⚠️  StateManifoldEngine import 실패 - Mock 사용")
        # Mock 엔진 사용
        class MockStateManifoldEngine:
            def build_state_space(self, search_biases):
                class StateManifold:
                    def __init__(self):
                        self.dimensions = {"test": {"risk_map": {"condition_1": 0.5}}}
                        self.organic_connections = {}
                        self.collapse_zones = []
                return StateManifold()
        state_manifold = StateManifoldEngineWrapper(MockStateManifoldEngine())
    
    # HistoricalDataReconstructor
    HistoricalDataReconstructor = import_historical_data_reconstructor()
    if HistoricalDataReconstructor:
        historical_reconstructor = HistoricalDataReconstructor()
        historical = HistoricalDataReconstructorWrapper(historical_reconstructor)
        print("✅ HistoricalDataReconstructor 생성 완료")
    else:
        print("⚠️  HistoricalDataReconstructor import 실패 - Mock 사용")
        # Mock 엔진 사용
        class MockHistoricalReconstructor:
            def collect_fragment(self, content, source, timestamp):
                class DataFragment:
                    def __init__(self):
                        self.content = content
                        self.source = source
                        self.timestamp = timestamp
                return DataFragment()
        historical = HistoricalDataReconstructorWrapper(MockHistoricalReconstructor())
    
    # NeuralDynamicsCore (아직 위치 확인 필요)
    NeuralDynamicsCore = import_neural_dynamics_core()
    if NeuralDynamicsCore:
        neural_dynamics_core = NeuralDynamicsCore()
        neural_dynamics = NeuralDynamicsCoreWrapper(neural_dynamics_core)
        print("✅ NeuralDynamicsCore 생성 완료")
    else:
        print("⚠️  NeuralDynamicsCore import 실패 - Mock 사용")
        # Mock 엔진 사용
        class MockNeuralDynamicsCore:
            def run(self, x0, W, b):
                # 간단한 시뮬레이션
                x = np.array(x0)
                for _ in range(10):
                    x = np.tanh(np.dot(W, x) + b)
                return [x.tolist()]
        neural_dynamics = NeuralDynamicsCoreWrapper(MockNeuralDynamicsCore())
    
    # CingulateCortexEngine (이미 BrainCore에 포함)
    from brain_core.engines.cingulate_cortex import CingulateCortexEngine
    cingulate_engine = CingulateCortexEngine(mode="research")
    cingulate = CingulateCortexEngineWrapper(cingulate_engine)
    print("✅ CingulateCortexEngine 생성 완료")
    print()
    
    # 엔진 등록 (cingulate는 이미 자동 등록되어 있으므로 제외)
    print("3. 엔진 등록")
    print("-" * 60)
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
    print("4. 초기 상태 생성")
    print("-" * 60)
    initial_state = GlobalState(
        state_vector=np.array([0.5, 0.3]),
        energy=1.0,
        risk=0.5,
    )
    print("✅ 초기 상태 생성 완료")
    print(f"   - state_vector: {initial_state.state_vector}")
    print(f"   - energy: {initial_state.energy}")
    print(f"   - risk: {initial_state.risk}")
    print()
    
    # 상태계 실행
    print("5. 상태계 실행")
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
    print("6. Extensions 확인")
    print("-" * 60)
    for key in ["L0", "L1", "L2", "Monitoring"]:
        extension = final_state.get_extension(key)
        print(f"   - {key}: {extension is not None}")
    print()
    
    # 궤적 확인
    if trajectory:
        print("7. 궤적 확인")
        print("-" * 60)
        initial_energy = trajectory[0].energy
        final_energy = trajectory[-1].energy
        energy_change = final_energy - initial_energy
        print(f"   - 초기 에너지: {initial_energy:.4f}")
        print(f"   - 최종 에너지: {final_energy:.4f}")
        print(f"   - 에너지 변화: {energy_change:.4f}")
        print()
    
    print("=" * 60)
    print("✅ 상태계 중심 실행 데모 완료 (실제 엔진 사용)")
    print("=" * 60)


if __name__ == "__main__":
    main()

