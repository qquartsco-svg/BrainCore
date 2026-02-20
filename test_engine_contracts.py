#!/usr/bin/env python3
"""
엔진 계약 검증 스크립트
실행: python3 test_engine_contracts.py
"""

import sys
sys.path.insert(0, 'src')

from brain_core.execution_modes import SelfOrganizingEngine
from brain_core.engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
    NeuralDynamicsCoreWrapper,
    HistoricalDataReconstructorWrapper,
    CingulateCortexEngineWrapper,
)
from brain_core.global_state import GlobalState
import numpy as np
import inspect

# Mock 엔진들
class MockWellFormationEngine:
    def generate_well(self, episodes):
        class Result:
            W = [[0.5, -0.3], [-0.3, 0.5]]
            b = [0.1, 0.1]
            analysis = {}
        return Result()

class MockStateManifoldEngine:
    def build_state_space(self, biases):
        class Manifold:
            dimensions = {"test": {"risk_map": {"c1": 0.5}}}
            organic_connections = {}
            collapse_zones = []
        return Manifold()

class MockNeuralDynamicsCore:
    def run(self, x0, W, b):
        return [x0, [x + 0.01 for x in x0]]
    def hopfield_energy(self, x):
        return 0.5

class MockHistoricalReconstructor:
    def collect_fragment(self, content, source, timestamp):
        class Fragment:
            pass
        return Fragment()

class MockCingulateCortex:
    def monitor(self, data):
        return {"health_score": 0.9, "conflicts": [], "errors": []}

def check_protocol_compliance(wrapper, protocol):
    """프로토콜 준수 여부 확인"""
    return isinstance(wrapper, protocol)

def check_method_signature(wrapper, method_name, expected_params, expected_return):
    """메서드 시그니처 확인"""
    if not hasattr(wrapper, method_name):
        return False, f"{method_name} 메서드 없음"
    
    sig = inspect.signature(getattr(wrapper, method_name))
    params = list(sig.parameters.keys())
    return_annotation = str(sig.return_annotation)
    
    # 파라미터 확인
    if params != expected_params:
        return False, f"파라미터 불일치: {params} != {expected_params}"
    
    # 반환 타입 확인 (타입 힌트만 확인, 실제 타입 체크는 런타임)
    if expected_return and return_annotation != expected_return:
        return False, f"반환 타입 불일치: {return_annotation} != {expected_return}"
    
    return True, "OK"

def test_wrapper_execution(wrapper, state):
    """실제 실행 테스트"""
    try:
        result = wrapper.update(state)
        if not isinstance(result, GlobalState):
            return False, f"반환 타입 오류: {type(result).__name__}"
        return True, "OK"
    except Exception as e:
        return False, f"실행 오류: {e}"

def main():
    print("=" * 60)
    print("엔진 계약 상태 검증")
    print("=" * 60)
    print()
    
    # 엔진 래퍼 생성
    wrappers = [
        ("WellFormationEngineWrapper", WellFormationEngineWrapper(MockWellFormationEngine())),
        ("StateManifoldEngineWrapper", StateManifoldEngineWrapper(MockStateManifoldEngine())),
        ("NeuralDynamicsCoreWrapper", NeuralDynamicsCoreWrapper(MockNeuralDynamicsCore())),
        ("HistoricalDataReconstructorWrapper", HistoricalDataReconstructorWrapper(MockHistoricalReconstructor())),
        ("CingulateCortexEngineWrapper", CingulateCortexEngineWrapper(MockCingulateCortex())),
    ]
    
    results = []
    
    for name, wrapper in wrappers:
        print(f"📋 {name}")
        print("-" * 60)
        
        # 1. SelfOrganizingEngine 프로토콜 준수
        is_self_organizing = check_protocol_compliance(wrapper, SelfOrganizingEngine)
        print(f"  SelfOrganizingEngine 프로토콜: {'✅' if is_self_organizing else '❌'}")
        
        # 2. update() 메서드 시그니처
        has_update, update_msg = check_method_signature(
            wrapper, 
            "update", 
            ["self", "state"],
            "GlobalState"
        )
        print(f"  update() 메서드: {'✅' if has_update else f'❌ ({update_msg})'}")
        
        # 3. get_energy() 메서드 (SelfOrganizingEngine 프로토콜 요구사항)
        has_get_energy, energy_msg = check_method_signature(
            wrapper,
            "get_energy",
            ["self", "state"],
            "float"
        )
        if has_get_energy:
            print(f"  get_energy() 메서드: ✅")
        else:
            print(f"  get_energy() 메서드: ⚠️  (프로토콜에 정의되어 있지만 구현되지 않음)")
        
        # 4. 실제 실행 테스트
        test_state = GlobalState(state_vector=np.array([0.5, 0.3]))
        exec_ok, exec_msg = test_wrapper_execution(wrapper, test_state)
        print(f"  실행 테스트: {'✅' if exec_ok else f'❌ ({exec_msg})'}")
        
        # 5. GlobalState Extensions 접근 방식
        uses_get_extension = "get_extension" in inspect.getsource(wrapper.update)
        uses_set_extension = "set_extension" in inspect.getsource(wrapper.update)
        print(f"  Extensions 접근: {'✅' if (uses_get_extension or uses_set_extension) else '⚠️  (직접 접근)'}")
        
        # 종합 평가
        all_ok = is_self_organizing and has_update and exec_ok
        status = "✅ 계약 준수" if all_ok else "⚠️  부분적 준수"
        results.append((name, status, all_ok))
        
        print(f"  상태: {status}")
        print()
    
    # 종합 결과
    print("=" * 60)
    print("종합 결과")
    print("=" * 60)
    for name, status, ok in results:
        print(f"  {name}: {status}")
    
    all_compliant = all(ok for _, _, ok in results)
    print()
    print(f"전체 계약 준수: {'✅ 완료' if all_compliant else '⚠️  일부 개선 필요'}")

if __name__ == "__main__":
    main()

