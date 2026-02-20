"""
Data Flow - 데이터 흐름 관리

엔진 간 데이터 전달 및 변환 관리

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

from typing import Dict, Any, Optional, List
import time
import logging

from .interfaces import DataConverter, StateSynchronizer

__version__ = "0.1.0"


class DataFlowManager:
    """데이터 흐름 관리자
    
    엔진 간 데이터 전달 및 변환 관리
    """
    
    def __init__(
        self,
        mode: str = "production",
        enable_logging: bool = True,
    ):
        """DataFlowManager 초기화
        
        Args:
            mode: "production" (산업용) 또는 "research" (연구용)
            enable_logging: 로깅 활성화 여부
        """
        self.mode = mode
        self.enable_logging = enable_logging
        self.converter = DataConverter()
        self.synchronizer = StateSynchronizer()
        
        # 데이터 흐름 이력 (연구용)
        self.flow_history: List[Dict[str, Any]] = []
        
        # 로깅 설정
        if enable_logging:
            self.logger = logging.getLogger("DataFlow")
            self.logger.setLevel(logging.INFO if mode == "production" else logging.DEBUG)
        else:
            self.logger = None
    
    def transfer(
        self,
        source_data: Dict[str, Any],
        source_engine: str,
        target_engine: str,
        validate: bool = True,
    ) -> Dict[str, Any]:
        """데이터 전달
        
        Args:
            source_data: 원본 데이터
            source_engine: 소스 엔진 이름
            target_engine: 목표 엔진 이름
            validate: 유효성 검사 여부
        
        Returns:
            변환된 데이터
        """
        start_time = time.time()
        
        # 데이터 변환
        converted_data = self.converter.convert(
            source_data=source_data,
            source_engine=source_engine,
            target_engine=target_engine,
        )
        
        # 유효성 검사
        if validate:
            is_valid, error_msg = self.converter.validate(converted_data)
            if not is_valid:
                if self.logger:
                    self.logger.warning(
                        f"데이터 유효성 검사 실패 ({source_engine} → {target_engine}): {error_msg}"
                    )
                # 산업용: 오류 발생 시 원본 데이터 반환
                if self.mode == "production":
                    return source_data
                else:
                    # 연구용: 오류 정보 포함
                    converted_data["_validation_error"] = error_msg
        
        elapsed_time = time.time() - start_time
        
        # 데이터 흐름 이력 기록 (연구용)
        if self.mode == "research":
            flow_record = {
                "timestamp": time.time(),
                "source": source_engine,
                "target": target_engine,
                "data_size": len(str(converted_data)),
                "elapsed_time": elapsed_time,
                "validated": validate,
            }
            self.flow_history.append(flow_record)
            # 최근 1000개만 유지
            if len(self.flow_history) > 1000:
                self.flow_history = self.flow_history[-1000:]
        
        if self.logger and self.mode == "research":
            self.logger.debug(
                f"데이터 전달: {source_engine} → {target_engine} "
                f"({elapsed_time*1000:.2f}ms)"
            )
        
        return converted_data
    
    def synchronize_state(
        self,
        engine_name: str,
        state: Dict[str, Any],
    ):
        """상태 동기화
        
        Args:
            engine_name: 엔진 이름
            state: 상태 정보
        """
        self.synchronizer.update_state(engine_name, state)
        
        if self.logger and self.mode == "research":
            self.logger.debug(f"상태 동기화: {engine_name}")
    
    def get_flow_statistics(self) -> Dict[str, Any]:
        """데이터 흐름 통계 반환 (연구용)
        
        Returns:
            통계 정보
        """
        if self.mode != "research":
            return {"mode": "production", "statistics_disabled": True}
        
        if not self.flow_history:
            return {"total_transfers": 0}
        
        # 통계 계산
        total_transfers = len(self.flow_history)
        total_time = sum(record["elapsed_time"] for record in self.flow_history)
        avg_time = total_time / total_transfers if total_transfers > 0 else 0.0
        
        # 엔진별 통계
        engine_stats = {}
        for record in self.flow_history:
            source = record["source"]
            target = record["target"]
            key = f"{source}→{target}"
            if key not in engine_stats:
                engine_stats[key] = {"count": 0, "total_time": 0.0}
            engine_stats[key]["count"] += 1
            engine_stats[key]["total_time"] += record["elapsed_time"]
        
        # 평균 시간 계산
        for key, stats in engine_stats.items():
            stats["avg_time"] = stats["total_time"] / stats["count"]
        
        return {
            "total_transfers": total_transfers,
            "total_time": total_time,
            "avg_time": avg_time,
            "engine_stats": engine_stats,
        }
    
    def get_state(self) -> Dict[str, Any]:
        """현재 상태 반환"""
        return {
            "mode": self.mode,
            "flow_history_count": len(self.flow_history),
            "synchronized_engines": list(self.synchronizer.engine_states.keys()),
            "statistics": self.get_flow_statistics(),
        }
    
    def reset(self):
        """상태 리셋"""
        self.flow_history.clear()
        self.synchronizer.reset()
        
        if self.logger:
            self.logger.info("DataFlowManager 상태 리셋 완료")

