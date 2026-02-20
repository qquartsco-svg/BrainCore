"""
Cingulate Cortex Engine 테스트

갈등 모니터링, 오류 감지, 시스템 건강 점검 테스트
"""

import pytest
import sys
from pathlib import Path

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core.engines import (
    CingulateCortexEngine,
    ConflictType,
    ErrorSeverity,
)


class TestCingulateCortexEngine:
    """Cingulate Cortex Engine 테스트"""
    
    def test_basic_monitoring(self):
        """기본 모니터링 테스트"""
        engine = CingulateCortexEngine(mode="production")
        
        system_state = {
            "thalamus": {"value": 0.5},
            "amygdala": {"value": 0.6},
            "memory": {"value": 0.4},
        }
        
        result = engine.monitor(system_state)
        
        assert "has_error" in result
        assert "has_conflict" in result
        assert "health_score" in result
        assert "recommendations" in result
    
    def test_conflict_detection(self):
        """갈등 감지 테스트"""
        engine = CingulateCortexEngine(
            mode="research",
            conflict_threshold=0.1,  # 낮은 임계값
        )
        
        system_state = {
            "thalamus": {"value": 0.9},
            "amygdala": {"value": 0.1},  # 큰 차이
        }
        
        result = engine.monitor(system_state)
        
        assert result["has_conflict"] is True
        assert len(result["conflicts"]) > 0
    
    def test_error_detection(self):
        """오류 감지 테스트"""
        engine = CingulateCortexEngine(mode="production")
        
        system_state = {
            "thalamus": {"error": True, "error_message": "테스트 오류"},
            "selected": None,  # 선택된 행동 없음
        }
        
        result = engine.monitor(system_state)
        
        assert result["has_error"] is True
        assert len(result["errors"]) > 0
    
    def test_health_check(self):
        """건강 점검 테스트"""
        engine = CingulateCortexEngine(mode="research")
        
        system_state = {
            "thalamus": {"value": 0.5},
            "amygdala": {"value": 0.6},
        }
        
        result = engine.monitor(system_state)
        
        assert "health" in result
        assert result["health"].overall_score >= 0.0
        assert result["health"].overall_score <= 1.0
        assert "thalamus" in result["health"].engine_health
        assert "amygdala" in result["health"].engine_health
    
    def test_recommendations(self):
        """권장사항 생성 테스트"""
        engine = CingulateCortexEngine(mode="production")
        
        system_state = {
            "thalamus": {"value": -1.0},  # 범위 위반
            "amygdala": {"error": True},
        }
        
        result = engine.monitor(system_state)
        
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
    
    def test_reset(self):
        """리셋 테스트"""
        engine = CingulateCortexEngine(mode="research")
        
        system_state = {"thalamus": {"value": 0.5}}
        engine.monitor(system_state)
        
        # 상태 확인
        state = engine.get_state()
        assert state["conflicts_count"] >= 0
        
        # 리셋
        engine.reset()
        
        # 리셋 후 상태 확인
        state_after = engine.get_state()
        assert state_after["conflicts_count"] == 0
        assert state_after["errors_count"] == 0
    
    def test_research_mode_stats(self):
        """연구 모드 통계 테스트"""
        engine = CingulateCortexEngine(mode="research")
        
        system_state = {
            "thalamus": {"value": 0.9},
            "amygdala": {"value": 0.1},
        }
        
        result = engine.monitor(system_state)
        
        assert "stats" in result
        assert "total_conflicts" in result["stats"]
        assert "conflict_types" in result["stats"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

