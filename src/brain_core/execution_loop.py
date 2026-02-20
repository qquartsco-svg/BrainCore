"""
Execution Loop - 실행 루프

엔진들을 순차적으로 실행하는 루프

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional, List
import logging

from .data_flow import DataFlowManager

__version__ = "0.1.0"


class ExecutionLoop:
    """실행 루프
    
    엔진들을 우선순위에 따라 순차적으로 실행
    """
    
    def __init__(
        self,
        mode: str = "production",
        enable_logging: bool = True,
        data_flow: Optional[DataFlowManager] = None,
    ):
        """ExecutionLoop 초기화
        
        Args:
            mode: "production" (산업용) 또는 "research" (연구용)
            enable_logging: 로깅 활성화 여부
            data_flow: 데이터 흐름 관리자 (None이면 자동 생성)
        """
        self.mode = mode
        self.enable_logging = enable_logging
        self.data_flow = data_flow or DataFlowManager(mode=mode, enable_logging=enable_logging)
        
        if enable_logging:
            self.logger = logging.getLogger("ExecutionLoop")
        else:
            self.logger = None
    
    def execute(
        self,
        input_data: Dict[str, Any],
        engines: Dict[str, Any],
        return_intermediate: bool = False,
    ) -> Dict[str, Any]:
        """실행 루프 실행
        
        Args:
            input_data: 입력 데이터
            engines: 엔진 딕셔너리 (우선순위 정렬됨)
            return_intermediate: 중간 결과 반환 여부
        
        Returns:
            실행 결과
        """
        current_data = input_data
        intermediate_results = {} if return_intermediate else None
        
        # 엔진 순차 실행
        prev_engine = None
        for name, engine in engines.items():
            try:
                # 데이터 전달 (이전 엔진 → 현재 엔진)
                if prev_engine:
                    current_data = self.data_flow.transfer(
                        source_data=current_data,
                        source_engine=prev_engine,
                        target_engine=name,
                        validate=(self.mode == "production"),  # 산업용에서만 검사
                    )
                
                # 엔진 실행
                if hasattr(engine, "process"):
                    output = engine.process(current_data)
                else:
                    if self.logger:
                        self.logger.warning(f"엔진 {name}에 process 메서드가 없습니다.")
                    continue
                
                # 상태 동기화
                if hasattr(engine, "get_state"):
                    try:
                        engine_state = engine.get_state()
                        self.data_flow.synchronize_state(name, engine_state)
                    except Exception as e:
                        if self.logger:
                            self.logger.warning(f"엔진 {name} 상태 동기화 실패: {e}")
                
                # 중간 결과 저장 (연구용)
                if return_intermediate:
                    intermediate_results[name] = {
                        "input": current_data,
                        "output": output,
                    }
                
                # 다음 엔진의 입력으로 사용
                current_data = output
                prev_engine = name
                
                if self.logger and self.mode == "research":
                    self.logger.debug(f"엔진 {name} 실행 완료")
            
            except Exception as e:
                if self.logger:
                    self.logger.error(f"엔진 {name} 실행 중 오류: {e}")
                
                # 산업용: 오류 발생 시 기본값 반환
                if self.mode == "production":
                    return {
                        "error": True,
                        "error_engine": name,
                        "error_message": str(e),
                        "output": current_data,  # 마지막 성공한 결과
                    }
                else:
                    # 연구용: 오류 정보 포함
                    if return_intermediate:
                        intermediate_results[name] = {
                            "input": current_data,
                            "error": str(e),
                        }
                    raise
        
        # Cingulate Cortex 모니터링 (있는 경우)
        monitoring_result = None
        if "cingulate" in engines:
            cingulate = engines["cingulate"]
            if hasattr(cingulate, "monitor"):
                # 시스템 상태 구성
                system_state = {"final_output": current_data}
                if return_intermediate and intermediate_results:
                    system_state.update(intermediate_results)
                monitoring_result = cingulate.monitor(system_state)
        
        # 최종 결과 구성
        result = {
            "output": current_data,
            "success": True,
        }
        
        if return_intermediate:
            result["intermediate"] = intermediate_results
        
        if monitoring_result:
            result["monitoring"] = monitoring_result
            # 안정화 필요 시 플래그 설정
            if monitoring_result.get("needs_stabilization", False):
                result["needs_stabilization"] = True
        
        return result

