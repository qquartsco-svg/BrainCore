"""
Engine Registry - 엔진 등록 시스템

엔진을 등록하고 우선순위에 따라 관리

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, List, Tuple
from collections import OrderedDict

__version__ = "0.1.0"


class EngineRegistry:
    """엔진 등록 시스템
    
    엔진을 등록하고 우선순위에 따라 정렬하여 관리
    """
    
    def __init__(self):
        """EngineRegistry 초기화"""
        self._engines: Dict[str, Tuple[Any, int]] = {}  # name -> (engine, priority)
    
    def register(
        self,
        name: str,
        engine: Any,
        priority: int = 0,
    ):
        """엔진 등록
        
        Args:
            name: 엔진 이름
            engine: 엔진 인스턴스
            priority: 실행 우선순위 (낮을수록 먼저 실행)
        """
        if name in self._engines:
            raise ValueError(f"엔진 {name}이 이미 등록되어 있습니다.")
        
        self._engines[name] = (engine, priority)
    
    def unregister(self, name: str):
        """엔진 등록 해제
        
        Args:
            name: 엔진 이름
        """
        if name not in self._engines:
            raise ValueError(f"엔진 {name}이 등록되어 있지 않습니다.")
        
        del self._engines[name]
    
    def get_engine(self, name: str) -> Any:
        """엔진 반환
        
        Args:
            name: 엔진 이름
        
        Returns:
            엔진 인스턴스
        """
        if name not in self._engines:
            raise ValueError(f"엔진 {name}이 등록되어 있지 않습니다.")
        
        return self._engines[name][0]
    
    def get_engines(self) -> Dict[str, Any]:
        """모든 엔진 반환 (우선순위 정렬)
        
        Returns:
            엔진 딕셔너리 (우선순위 순)
        """
        # 우선순위로 정렬
        sorted_engines = sorted(
            self._engines.items(),
            key=lambda x: x[1][1]  # priority
        )
        
        return OrderedDict((name, engine) for name, (engine, _) in sorted_engines)
    
    def get_engine_names(self) -> List[str]:
        """등록된 엔진 이름 리스트 반환
        
        Returns:
            엔진 이름 리스트
        """
        return list(self._engines.keys())
    
    def has_engine(self, name: str) -> bool:
        """엔진 등록 여부 확인
        
        Args:
            name: 엔진 이름
        
        Returns:
            등록 여부
        """
        return name in self._engines

