"""
Data Flow 테스트

데이터 흐름 관리 및 변환 테스트
"""

import pytest
import sys
from pathlib import Path

# BrainCore 경로 추가
brain_core_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(brain_core_path))

from brain_core.data_flow import DataFlowManager
from brain_core.interfaces import DataConverter, StateSynchronizer


class TestDataFlowManager:
    """DataFlowManager 테스트"""
    
    def test_basic_transfer(self):
        """기본 데이터 전달 테스트"""
        manager = DataFlowManager(mode="production")
        
        source_data = {"value": 0.5, "status": "ok"}
        result = manager.transfer(
            source_data=source_data,
            source_engine="thalamus",
            target_engine="amygdala",
        )
        
        assert result == source_data  # 기본 변환은 복사
    
    def test_data_validation(self):
        """데이터 유효성 검사 테스트"""
        manager = DataFlowManager(mode="production")
        
        # 유효한 데이터
        valid_data = {"value": 0.5}
        result = manager.transfer(
            source_data=valid_data,
            source_engine="thalamus",
            target_engine="amygdala",
            validate=True,
        )
        assert result == valid_data
        
        # 범위 위반 데이터 (산업용: 원본 반환)
        invalid_data = {"value": 1.5}  # 범위 초과
        result = manager.transfer(
            source_data=invalid_data,
            source_engine="thalamus",
            target_engine="amygdala",
            validate=True,
        )
        assert result == invalid_data  # 산업용: 원본 반환
    
    def test_state_synchronization(self):
        """상태 동기화 테스트"""
        manager = DataFlowManager(mode="research")
        
        manager.synchronize_state("thalamus", {"value": 0.5})
        manager.synchronize_state("amygdala", {"value": 0.6})
        
        state = manager.get_state()
        assert "thalamus" in manager.synchronizer.engine_states
        assert "amygdala" in manager.synchronizer.engine_states
    
    def test_research_mode_statistics(self):
        """연구 모드 통계 테스트"""
        manager = DataFlowManager(mode="research")
        
        # 여러 전달 수행
        for i in range(5):
            manager.transfer(
                source_data={"value": i * 0.1},
                source_engine="thalamus",
                target_engine="amygdala",
            )
        
        stats = manager.get_flow_statistics()
        assert stats["total_transfers"] == 5
        assert "engine_stats" in stats
    
    def test_reset(self):
        """리셋 테스트"""
        manager = DataFlowManager(mode="research")
        
        manager.transfer(
            source_data={"value": 0.5},
            source_engine="thalamus",
            target_engine="amygdala",
        )
        manager.synchronize_state("thalamus", {"value": 0.5})
        
        # 리셋
        manager.reset()
        
        state = manager.get_state()
        assert state["flow_history_count"] == 0
        assert len(manager.synchronizer.engine_states) == 0


class TestDataConverter:
    """DataConverter 테스트"""
    
    def test_basic_conversion(self):
        """기본 변환 테스트"""
        source_data = {"value": 0.5}
        result = DataConverter.convert(source_data)
        
        assert result == source_data
    
    def test_validation(self):
        """유효성 검사 테스트"""
        # 유효한 데이터
        valid_data = {"value": 0.5}
        is_valid, error = DataConverter.validate(
            valid_data,
            expected_keys=["value"],
            value_ranges={"value": (0.0, 1.0)},
        )
        assert is_valid is True
        assert error is None
        
        # 범위 위반
        invalid_data = {"value": 1.5}
        is_valid, error = DataConverter.validate(
            invalid_data,
            value_ranges={"value": (0.0, 1.0)},
        )
        assert is_valid is False
        assert error is not None


class TestStateSynchronizer:
    """StateSynchronizer 테스트"""
    
    def test_state_update(self):
        """상태 업데이트 테스트"""
        synchronizer = StateSynchronizer()
        
        synchronizer.update_state("thalamus", {"value": 0.5})
        synchronizer.update_state("amygdala", {"value": 0.6})
        
        assert "thalamus" in synchronizer.engine_states
        assert "amygdala" in synchronizer.engine_states
    
    def test_synchronized_state(self):
        """동기화된 상태 반환 테스트"""
        synchronizer = StateSynchronizer()
        
        synchronizer.update_state("thalamus", {"value": 0.5})
        state = synchronizer.get_synchronized_state()
        
        assert "engines" in state
        assert "thalamus" in state["engines"]
    
    def test_reset(self):
        """리셋 테스트"""
        synchronizer = StateSynchronizer()
        
        synchronizer.update_state("thalamus", {"value": 0.5})
        synchronizer.reset()
        
        assert len(synchronizer.engine_states) == 0
        assert len(synchronizer.sync_history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

