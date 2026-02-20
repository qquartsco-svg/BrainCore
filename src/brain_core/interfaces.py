"""
BrainCore 인터페이스 표준

모든 뇌 엔진이 준수해야 하는 표준 인터페이스 정의

산업용 중심:
- 효율적인 데이터 전달
- 타입 안전성
- 버전 호환성

연구용 확장:
- 데이터 추적
- 변환 과정 기록

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional, Protocol, runtime_checkable
from abc import ABC, abstractmethod

__version__ = "0.1.0"


@runtime_checkable
class BrainEngine(Protocol):
    """뇌 엔진 기본 인터페이스 (Protocol)
    
    모든 뇌 엔진이 구현해야 하는 최소 인터페이스
    """
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """입력 처리
        
        Args:
            input_data: 입력 데이터
        
        Returns:
            처리 결과
        """
        ...
    
    def get_state(self) -> Dict[str, Any]:
        """현재 상태 반환
        
        Returns:
            상태 정보
        """
        ...
    
    def reset(self):
        """상태 리셋"""
        ...


class BrainEngineBase(ABC):
    """뇌 엔진 기본 클래스
    
    모든 뇌 엔진의 추상 기본 클래스
    """
    
    def __init__(self, name: str, mode: str = "production"):
        """BrainEngineBase 초기화
        
        Args:
            name: 엔진 이름
            mode: "production" (산업용) 또는 "research" (연구용)
        """
        self.name = name
        self.mode = mode
        self._state: Dict[str, Any] = {}
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """입력 처리
        
        Args:
            input_data: 입력 데이터
        
        Returns:
            처리 결과
        """
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """현재 상태 반환
        
        Returns:
            상태 정보
        """
        return {
            "name": self.name,
            "mode": self.mode,
            "state": self._state.copy(),
        }
    
    def reset(self):
        """상태 리셋"""
        self._state.clear()
    
    def get_config(self) -> Dict[str, Any]:
        """설정 반환"""
        return {
            "name": self.name,
            "mode": self.mode,
        }


class DataConverter:
    """데이터 변환 레이어
    
    엔진 간 데이터 전달 시 변환 처리
    """
    
    @staticmethod
    def convert(
        source_data: Dict[str, Any],
        target_format: Optional[str] = None,
        source_engine: Optional[str] = None,
        target_engine: Optional[str] = None,
    ) -> Dict[str, Any]:
        """데이터 변환
        
        Args:
            source_data: 원본 데이터
            target_format: 목표 형식 (None이면 자동 감지)
            source_engine: 소스 엔진 이름
            target_engine: 목표 엔진 이름
        
        Returns:
            변환된 데이터
        """
        # 기본 변환: 딕셔너리 복사
        converted = source_data.copy()
        
        # 엔진별 특수 변환 (필요시)
        if source_engine and target_engine:
            # 특정 엔진 쌍에 대한 변환 로직
            pass
        
        return converted
    
    @staticmethod
    def validate(
        data: Dict[str, Any],
        expected_keys: Optional[list] = None,
        value_ranges: Optional[Dict[str, tuple]] = None,
    ) -> tuple[bool, Optional[str]]:
        """데이터 유효성 검사
        
        Args:
            data: 검사할 데이터
            expected_keys: 예상 키 리스트
            value_ranges: 값 범위 딕셔너리 {key: (min, max)}
        
        Returns:
            (유효성, 오류 메시지)
        """
        # 키 검사
        if expected_keys:
            missing_keys = set(expected_keys) - set(data.keys())
            if missing_keys:
                return False, f"누락된 키: {missing_keys}"
        
        # 값 범위 검사
        if value_ranges:
            for key, (min_val, max_val) in value_ranges.items():
                if key in data:
                    value = data[key]
                    if isinstance(value, (int, float)):
                        if value < min_val or value > max_val:
                            return False, f"키 '{key}' 값이 범위를 벗어남: {value} (범위: {min_val}~{max_val})"
        
        return True, None


class StateSynchronizer:
    """상태 동기화 관리자
    
    여러 엔진의 상태를 동기화
    """
    
    def __init__(self):
        """StateSynchronizer 초기화"""
        self.engine_states: Dict[str, Dict[str, Any]] = {}
        self.sync_history: list = []
    
    def update_state(self, engine_name: str, state: Dict[str, Any]):
        """엔진 상태 업데이트
        
        Args:
            engine_name: 엔진 이름
            state: 상태 정보
        """
        self.engine_states[engine_name] = state.copy()
        self.sync_history.append({
            "engine": engine_name,
            "timestamp": time.time(),
            "state": state.copy(),
        })
        # 최근 100개만 유지
        if len(self.sync_history) > 100:
            self.sync_history = self.sync_history[-100:]
    
    def get_synchronized_state(self) -> Dict[str, Any]:
        """동기화된 전체 상태 반환
        
        Returns:
            전체 상태 정보
        """
        return {
            "engines": self.engine_states.copy(),
            "sync_count": len(self.sync_history),
        }
    
    def reset(self):
        """상태 리셋"""
        self.engine_states.clear()
        self.sync_history.clear()


import time

