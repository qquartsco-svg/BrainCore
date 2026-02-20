"""
Engine Adapters - 엔진 어댑터

기존 엔진들을 BrainEngine 인터페이스에 맞추는 어댑터

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import logging

from .interfaces import BrainEngineBase

__version__ = "0.1.0"


class EngineAdapter(BrainEngineBase):
    """엔진 어댑터 기본 클래스
    
    기존 엔진을 BrainEngine 인터페이스에 맞추는 어댑터
    """
    
    def __init__(
        self,
        engine: Any,
        name: str,
        mode: str = "production",
        enable_logging: bool = True,
    ):
        """EngineAdapter 초기화
        
        Args:
            engine: 원본 엔진 인스턴스
            name: 엔진 이름
            mode: "production" (산업용) 또는 "research" (연구용)
            enable_logging: 로깅 활성화 여부
        """
        super().__init__(name=name, mode=mode)
        self.engine = engine
        self.enable_logging = enable_logging
        
        if enable_logging:
            self.logger = logging.getLogger(f"EngineAdapter.{name}")
        else:
            self.logger = None
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """입력 처리
        
        원본 엔진의 메서드를 호출하여 처리
        
        Args:
            input_data: 입력 데이터
        
        Returns:
            처리 결과
        """
        # 원본 엔진의 process 메서드 호출
        if hasattr(self.engine, "process"):
            try:
                output = self.engine.process(input_data)
                return output
            except Exception as e:
                if self.logger:
                    self.logger.error(f"엔진 {self.name} 처리 중 오류: {e}")
                # 산업용: 오류 발생 시 기본값 반환
                if self.mode == "production":
                    return {"error": True, "error_message": str(e)}
                else:
                    raise
        
        # process 메서드가 없으면 다른 메서드 시도
        elif hasattr(self.engine, "run"):
            try:
                output = self.engine.run(input_data)
                return output if isinstance(output, dict) else {"output": output}
            except Exception as e:
                if self.logger:
                    self.logger.error(f"엔진 {self.name} 실행 중 오류: {e}")
                if self.mode == "production":
                    return {"error": True, "error_message": str(e)}
                else:
                    raise
        
        else:
            # 처리 메서드가 없으면 입력 그대로 반환
            if self.logger:
                self.logger.warning(f"엔진 {self.name}에 처리 메서드가 없습니다.")
            return input_data
    
    def get_state(self) -> Dict[str, Any]:
        """현재 상태 반환"""
        base_state = super().get_state()
        
        # 원본 엔진의 상태도 포함
        if hasattr(self.engine, "get_state"):
            try:
                engine_state = self.engine.get_state()
                base_state["engine_state"] = engine_state
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"엔진 {self.name} 상태 조회 실패: {e}")
        
        return base_state
    
    def reset(self):
        """상태 리셋"""
        super().reset()
        
        # 원본 엔진도 리셋
        if hasattr(self.engine, "reset"):
            try:
                self.engine.reset()
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"엔진 {self.name} 리셋 실패: {e}")


class MockEngineAdapter(EngineAdapter):
    """Mock 엔진 어댑터
    
    테스트용 Mock 엔진
    """
    
    def __init__(
        self,
        name: str,
        mode: str = "production",
        process_func: Optional[callable] = None,
    ):
        """MockEngineAdapter 초기화
        
        Args:
            name: 엔진 이름
            mode: 모드
            process_func: 처리 함수 (None이면 기본 함수 사용)
        """
        # Mock 엔진 객체 생성
        class MockEngine:
            def __init__(self, process_func):
                self.process_func = process_func or (lambda x: x)
            
            def process(self, input_data):
                return self.process_func(input_data)
            
            def get_state(self):
                return {"mock": True}
            
            def reset(self):
                pass
        
        mock_engine = MockEngine(process_func)
        super().__init__(engine=mock_engine, name=name, mode=mode)

