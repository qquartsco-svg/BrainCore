"""
BrainCore 기본 통합 데모

Mock 엔진들을 사용한 기본 통합 데모
"""

import sys
from pathlib import Path

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core import BrainCore
from brain_core.engine_adapters import MockEngineAdapter


def main():
    """기본 통합 데모"""
    print("=" * 60)
    print("BrainCore 기본 통합 데모")
    print("=" * 60)
    print()
    
    # BrainCore 생성
    print("1. BrainCore 생성")
    print("-" * 60)
    core = BrainCore(mode="research")  # 연구 모드로 상세 로깅
    print(f"✅ BrainCore 생성 완료 (모드: {core.mode})")
    print()
    
    # Mock 엔진 생성 및 등록
    print("2. 엔진 등록")
    print("-" * 60)
    
    # Thalamus (입력 수집)
    thalamus = MockEngineAdapter(
        name="thalamus",
        process_func=lambda x: {
            "sensor_value": x.get("sensor", 0.5),
            "processed": True,
        },
    )
    core.register_engine("thalamus", thalamus, priority=1)
    print("✅ Thalamus 엔진 등록")
    
    # Amygdala (감정 가중)
    amygdala = MockEngineAdapter(
        name="amygdala",
        process_func=lambda x: {
            "value": x.get("sensor_value", 0.5),
            "emotion_weight": 0.8,
            "weighted_value": x.get("sensor_value", 0.5) * 0.8,
        },
    )
    core.register_engine("amygdala", amygdala, priority=2)
    print("✅ Amygdala 엔진 등록")
    
    # Hippo_Memory (기억 검색)
    hippo_memory = MockEngineAdapter(
        name="hippo_memory",
        process_func=lambda x: {
            "value": x.get("weighted_value", 0.5),
            "memory_match": 0.7,
            "recalled_value": x.get("weighted_value", 0.5) * 0.7,
        },
    )
    core.register_engine("hippo_memory", hippo_memory, priority=3)
    print("✅ Hippo_Memory 엔진 등록")
    
    # Basal_Ganglia (행동 후보 생성)
    basal_ganglia = MockEngineAdapter(
        name="basal_ganglia",
        process_func=lambda x: {
            "value": x.get("recalled_value", 0.5),
            "action_candidates": [
                {"action": "move_forward", "confidence": 0.8},
                {"action": "turn_left", "confidence": 0.6},
                {"action": "turn_right", "confidence": 0.4},
            ],
        },
    )
    core.register_engine("basal_ganglia", basal_ganglia, priority=4)
    print("✅ Basal_Ganglia 엔진 등록")
    print()
    
    # 실행
    print("3. 실행 사이클")
    print("-" * 60)
    input_data = {"sensor": 0.7}
    result = core.run_cycle(input_data, return_intermediate=True)
    
    print(f"✅ 실행 완료")
    print(f"✅ 성공: {result['success']}")
    print()
    
    # 중간 결과 확인 (연구 모드)
    if "intermediate" in result:
        print("4. 중간 결과 (연구 모드)")
        print("-" * 60)
        for engine_name, intermediate in result["intermediate"].items():
            print(f"   {engine_name}:")
            print(f"     입력: {intermediate.get('input', {})}")
            print(f"     출력: {intermediate.get('output', {})}")
        print()
    
    # 모니터링 결과 확인
    if "monitoring" in result:
        print("5. 모니터링 결과")
        print("-" * 60)
        monitoring = result["monitoring"]
        print(f"   건강 점수: {monitoring.get('health_score', 0):.2f}")
        print(f"   갈등: {len(monitoring.get('conflicts', []))}개")
        print(f"   오류: {len(monitoring.get('errors', []))}개")
        if monitoring.get("needs_stabilization"):
            print("   ⚠️ 안정화 필요")
        print()
    
    # 시스템 상태 확인
    print("6. 시스템 상태")
    print("-" * 60)
    state = core.get_system_state()
    print(f"   등록된 엔진: {state['registered_count']}개")
    print(f"   엔진 목록: {', '.join(state['engines'])}")
    print()
    
    # 데이터 흐름 통계 (연구 모드)
    if core.mode == "research":
        print("7. 데이터 흐름 통계 (연구 모드)")
        print("-" * 60)
        stats = core.data_flow.get_flow_statistics()
        print(f"   총 전달 횟수: {stats.get('total_transfers', 0)}")
        print(f"   평균 전달 시간: {stats.get('avg_time', 0)*1000:.2f}ms")
        print()
    
    print("=" * 60)
    print("✅ BrainCore 기본 통합 데모 완료")
    print("=" * 60)


if __name__ == "__main__":
    main()

