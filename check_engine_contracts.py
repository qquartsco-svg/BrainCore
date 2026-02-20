#!/usr/bin/env python3
"""
엔진 계약 상태 확인 스크립트

각 엔진이 StateCentricEngine 프로토콜을 제대로 구현하고 있는지 확인
"""

import sys
from pathlib import Path
from typing import Protocol, runtime_checkable
import inspect

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core.execution_modes import SelfOrganizingEngine
from brain_core.global_state import GlobalState
from brain_core.engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
    NeuralDynamicsCoreWrapper,
    HistoricalDataReconstructorWrapper,
    CingulateCortexEngineWrapper,
)
import numpy as np

@runtime_checkable
class StateCentricEngineProtocol(Protocol):
    """StateCentricEngine 프로토콜 정의"""
    def update(self, state: GlobalState) -> GlobalState:
        """상태 업데이트"""
        ...
    
    def get_state(self) -> dict:
        """엔진 내부 상태 반환"""
        ...
    
    def reset(self):
        """상태 리셋"""
        ...

def check_protocol_compliance(engine_class, engine_name):
    """프로토콜 준수 여부 확인"""
    print(f"\n{'='*60}")
    print(f"🔍 {engine_name} 계약 확인")
    print(f"{'='*60}")
    
    issues = []
    
    # 1. StateCentricEngine 프로토콜 체크
    if not isinstance(engine_class, type):
        issues.append("❌ 클래스가 아님")
        return issues
    
    # 2. update 메서드 확인
    if not hasattr(engine_class, 'update'):
        issues.append("❌ update() 메서드 없음")
    else:
        update_method = getattr(engine_class, 'update')
        sig = inspect.signature(update_method)
        
        # 파라미터 확인
        params = list(sig.parameters.keys())
        if len(params) != 2 or params[0] != 'self' or params[1] != 'state':
            issues.append(f"❌ update() 시그니처 불일치: {params}")
        
        # 반환 타입 힌트 확인
        return_annotation = sig.return_annotation
        if return_annotation == inspect.Signature.empty:
            issues.append("⚠️  update() 반환 타입 힌트 없음")
        elif 'GlobalState' not in str(return_annotation):
            issues.append(f"⚠️  update() 반환 타입 힌트 불일치: {return_annotation}")
    
    # 3. get_state 메서드 확인
    if not hasattr(engine_class, 'get_state'):
        issues.append("❌ get_state() 메서드 없음")
    else:
        get_state_method = getattr(engine_class, 'get_state')
        sig = inspect.signature(get_state_method)
        return_annotation = sig.return_annotation
        if return_annotation == inspect.Signature.empty:
            issues.append("⚠️  get_state() 반환 타입 힌트 없음")
    
    # 4. reset 메서드 확인
    if not hasattr(engine_class, 'reset'):
        issues.append("⚠️  reset() 메서드 없음 (선택적)")
    
    # 5. get_energy 메서드 확인 (SelfOrganizingEngine 프로토콜)
    if not hasattr(engine_class, 'get_energy'):
        issues.append("⚠️  get_energy() 메서드 없음 (SelfOrganizingEngine 프로토콜)")
    else:
        get_energy_method = getattr(engine_class, 'get_energy')
        sig = inspect.signature(get_energy_method)
        params = list(sig.parameters.keys())
        if len(params) != 2 or params[0] != 'self' or params[1] != 'state':
            issues.append(f"⚠️  get_energy() 시그니처 불일치: {params}")
    
    # 6. SelfOrganizingEngine 상속 확인
    if not issubclass(engine_class, SelfOrganizingEngine):
        issues.append("❌ SelfOrganizingEngine 상속 안 됨")
    
    # 7. runtime_checkable 프로토콜 체크
    try:
        # Mock 인스턴스 생성하여 프로토콜 준수 확인
        class MockEngine:
            def __init__(self):
                pass
        
        # 실제 엔진 인스턴스 생성 테스트
        # (이 부분은 실제 엔진이 필요하므로 스킵)
        pass
    except Exception as e:
        issues.append(f"⚠️  인스턴스 생성 테스트 실패: {e}")
    
    # 결과 출력
    if not issues:
        print("✅ 모든 계약 준수")
    else:
        for issue in issues:
            print(issue)
    
    return issues

def check_implementation_details(engine_class, engine_name):
    """구현 세부사항 확인"""
    print(f"\n📋 {engine_name} 구현 세부사항:")
    
    # update 메서드 소스 확인
    if hasattr(engine_class, 'update'):
        source = inspect.getsource(engine_class.update)
        lines = source.split('\n')
        
        # GlobalState 사용 확인
        if 'GlobalState' in source:
            print("  ✅ GlobalState 사용")
        else:
            print("  ⚠️  GlobalState 사용 안 함")
        
        # state.extensions 사용 확인
        if 'extensions' in source or 'get_extension' in source or 'set_extension' in source:
            print("  ✅ extensions 사용")
        else:
            print("  ⚠️  extensions 사용 안 함")
        
        # 반환 확인
        if 'return state' in source:
            print("  ✅ state 반환")
        else:
            print("  ⚠️  state 반환 확인 필요")

def main():
    """메인 함수"""
    print("="*60)
    print("엔진 계약 상태 확인")
    print("="*60)
    
    engines = {
        "WellFormationEngineWrapper": WellFormationEngineWrapper,
        "StateManifoldEngineWrapper": StateManifoldEngineWrapper,
        "NeuralDynamicsCoreWrapper": NeuralDynamicsCoreWrapper,
        "HistoricalDataReconstructorWrapper": HistoricalDataReconstructorWrapper,
        "CingulateCortexEngineWrapper": CingulateCortexEngineWrapper,
    }
    
    all_issues = {}
    
    for engine_name, engine_class in engines.items():
        issues = check_protocol_compliance(engine_class, engine_name)
        check_implementation_details(engine_class, engine_name)
        all_issues[engine_name] = issues
    
    # 전체 요약
    print(f"\n{'='*60}")
    print("📊 전체 요약")
    print(f"{'='*60}")
    
    total_engines = len(engines)
    compliant_engines = sum(1 for issues in all_issues.values() if not issues)
    
    print(f"총 엔진 수: {total_engines}")
    print(f"계약 준수: {compliant_engines}/{total_engines}")
    
    if compliant_engines == total_engines:
        print("\n✅ 모든 엔진이 계약을 준수합니다!")
    else:
        print("\n⚠️  일부 엔진에 계약 위반이 있습니다:")
        for engine_name, issues in all_issues.items():
            if issues:
                print(f"  - {engine_name}: {len(issues)}개 이슈")

if __name__ == "__main__":
    main()

