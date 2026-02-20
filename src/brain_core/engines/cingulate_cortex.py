"""
Cingulate Cortex Engine - 시스템 모니터링 및 오류 감지

갈등 모니터링, 오류 감지, 시스템 건강 점검을 담당하는 엔진

산업용 중심:
- 실시간 모니터링
- 자동 복구
- 알림 시스템

연구용 확장:
- 상세 오류 분석
- 통계 수집
- 생물학적 정확성 검증

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import time
import logging

__version__ = "0.1.0"


class ConflictType(Enum):
    """갈등 유형"""
    VALUE_MISMATCH = "value_mismatch"  # 값 불일치
    TYPE_MISMATCH = "type_mismatch"    # 타입 불일치
    RANGE_VIOLATION = "range_violation"  # 범위 위반
    LOGIC_CONFLICT = "logic_conflict"   # 논리 충돌


class ErrorSeverity(Enum):
    """오류 심각도"""
    LOW = "low"          # 낮음 (경고)
    MEDIUM = "medium"    # 중간 (주의)
    HIGH = "high"        # 높음 (오류)
    CRITICAL = "critical"  # 치명적 (시스템 중단)


@dataclass
class Conflict:
    """갈등 정보"""
    conflict_type: ConflictType
    engine1: str
    engine2: str
    description: str
    severity: ErrorSeverity
    timestamp: float = field(default_factory=time.time)


@dataclass
class Error:
    """오류 정보"""
    engine: str
    error_type: str
    message: str
    severity: ErrorSeverity
    timestamp: float = field(default_factory=time.time)
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemHealth:
    """시스템 건강 상태"""
    overall_score: float  # 0.0 ~ 1.0
    engine_health: Dict[str, float]  # 엔진별 건강 점수
    conflicts_count: int
    errors_count: int
    warnings_count: int
    timestamp: float = field(default_factory=time.time)


class CingulateCortexEngine:
    """Cingulate Cortex 엔진
    
    시스템 모니터링 및 오류 감지 담당
    """
    
    def __init__(
        self,
        mode: str = "production",
        enable_logging: bool = True,
        conflict_threshold: float = 0.5,  # 갈등 감지 임계값
        health_check_interval: float = 1.0,  # 건강 점검 간격 (초)
    ):
        """CingulateCortexEngine 초기화
        
        Args:
            mode: "production" (산업용) 또는 "research" (연구용)
            enable_logging: 로깅 활성화 여부
            conflict_threshold: 갈등 감지 임계값 (0.0 ~ 1.0)
            health_check_interval: 건강 점검 간격 (초)
        """
        self.mode = mode
        self.enable_logging = enable_logging
        self.conflict_threshold = conflict_threshold
        self.health_check_interval = health_check_interval
        
        # 로깅 설정
        if enable_logging:
            self.logger = logging.getLogger("CingulateCortex")
            self.logger.setLevel(logging.INFO if mode == "production" else logging.DEBUG)
        else:
            self.logger = None
        
        # 상태 관리
        self.conflicts: List[Conflict] = []
        self.errors: List[Error] = []
        self.warnings: List[Error] = []
        self.health_history: List[SystemHealth] = []
        
        # 통계 (연구용)
        self.stats = {
            "total_conflicts": 0,
            "total_errors": 0,
            "total_warnings": 0,
            "conflict_types": {},
            "error_types": {},
        }
    
    def monitor(
        self,
        system_state: Dict[str, Any],
    ) -> Dict[str, Any]:
        """시스템 상태 모니터링
        
        Args:
            system_state: 시스템 상태 정보
                {
                    'thalamus': {...},
                    'amygdala': {...},
                    'memory': {...},
                    'actions': [...],
                    'selected': {...},
                }
        
        Returns:
            모니터링 결과
            {
                'has_error': bool,
                'has_conflict': bool,
                'conflicts': List[Conflict],
                'errors': List[Error],
                'warnings': List[Error],
                'health_score': float,
                'recommendations': List[str],
                'needs_stabilization': bool,
            }
        """
        # 1. 갈등 모니터링
        conflicts = self._detect_conflicts(system_state)
        
        # 2. 오류 감지
        errors = self._detect_errors(system_state)
        
        # 3. 시스템 건강 점검
        health = self._check_health(system_state)
        
        # 4. 복구 권장사항 생성
        recommendations = self._generate_recommendations(conflicts, errors, health)
        
        # 5. 안정화 필요 여부 판단
        needs_stabilization = (
            len(conflicts) > 0 or
            len([e for e in errors if e.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]]) > 0 or
            health.overall_score < 0.5
        )
        
        result = {
            "has_error": len(errors) > 0,
            "has_conflict": len(conflicts) > 0,
            "conflicts": conflicts,
            "errors": errors,
            "warnings": self.warnings,
            "health_score": health.overall_score,
            "health": health,
            "recommendations": recommendations,
            "needs_stabilization": needs_stabilization,
        }
        
        # 연구용: 상세 정보 추가
        if self.mode == "research":
            result["stats"] = self.stats.copy()
            result["health_history"] = self.health_history[-10:]  # 최근 10개
        
        if self.logger:
            if needs_stabilization:
                self.logger.warning(
                    f"안정화 필요: 건강 점수 {health.overall_score:.2f}, "
                    f"갈등 {len(conflicts)}개, 오류 {len(errors)}개"
                )
            elif self.mode == "research":
                self.logger.debug(f"시스템 건강 점수: {health.overall_score:.2f}")
        
        return result
    
    def _detect_conflicts(
        self,
        system_state: Dict[str, Any],
    ) -> List[Conflict]:
        """갈등 감지
        
        여러 엔진의 출력이 충돌하는지 확인
        
        Args:
            system_state: 시스템 상태
        
        Returns:
            갈등 리스트
        """
        conflicts = []
        
        # 엔진 출력 추출
        engine_outputs = {}
        for key in ['thalamus', 'amygdala', 'memory', 'actions', 'selected']:
            if key in system_state:
                engine_outputs[key] = system_state[key]
        
        # 엔진 쌍 간 갈등 검사
        engine_names = list(engine_outputs.keys())
        for i, name1 in enumerate(engine_names):
            for name2 in engine_names[i+1:]:
                output1 = engine_outputs[name1]
                output2 = engine_outputs[name2]
                
                # 값 불일치 검사
                if isinstance(output1, dict) and isinstance(output2, dict):
                    conflict = self._check_value_conflict(name1, output1, name2, output2)
                    if conflict:
                        conflicts.append(conflict)
                
                # 타입 불일치 검사
                if type(output1) != type(output2):
                    conflict = Conflict(
                        conflict_type=ConflictType.TYPE_MISMATCH,
                        engine1=name1,
                        engine2=name2,
                        description=f"타입 불일치: {type(output1).__name__} vs {type(output2).__name__}",
                        severity=ErrorSeverity.MEDIUM,
                    )
                    conflicts.append(conflict)
        
        # 갈등 기록
        self.conflicts.extend(conflicts)
        self.stats["total_conflicts"] += len(conflicts)
        
        for conflict in conflicts:
            conflict_type = conflict.conflict_type.value
            self.stats["conflict_types"][conflict_type] = \
                self.stats["conflict_types"].get(conflict_type, 0) + 1
        
        return conflicts
    
    def _check_value_conflict(
        self,
        name1: str,
        output1: Dict[str, Any],
        name2: str,
        output2: Dict[str, Any],
    ) -> Optional[Conflict]:
        """값 갈등 검사"""
        # 공통 키 확인
        common_keys = set(output1.keys()) & set(output2.keys())
        
        for key in common_keys:
            val1 = output1[key]
            val2 = output2[key]
            
            # 숫자 값 비교
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                diff = abs(val1 - val2)
                max_val = max(abs(val1), abs(val2), 1.0)
                relative_diff = diff / max_val
                
                if relative_diff > self.conflict_threshold:
                    return Conflict(
                        conflict_type=ConflictType.VALUE_MISMATCH,
                        engine1=name1,
                        engine2=name2,
                        description=f"키 '{key}' 값 불일치: {val1} vs {val2} (차이: {relative_diff:.2%})",
                        severity=ErrorSeverity.HIGH if relative_diff > 0.8 else ErrorSeverity.MEDIUM,
                    )
            
            # 범위 위반 검사
            if isinstance(val1, (int, float)):
                if val1 < 0 or val1 > 1:
                    return Conflict(
                        conflict_type=ConflictType.RANGE_VIOLATION,
                        engine1=name1,
                        engine2=name2,
                        description=f"키 '{key}' 범위 위반: {val1}",
                        severity=ErrorSeverity.MEDIUM,
                    )
        
        return None
    
    def _detect_errors(
        self,
        system_state: Dict[str, Any],
    ) -> List[Error]:
        """오류 감지
        
        예상과 다른 결과 발생 시 감지
        
        Args:
            system_state: 시스템 상태
        
        Returns:
            오류 리스트
        """
        errors = []
        
        # 각 엔진 출력 검사
        for key, value in system_state.items():
            if key == "selected" and value is None:
                # 선택된 행동이 없음
                error = Error(
                    engine=key,
                    error_type="no_action_selected",
                    message="선택된 행동이 없습니다.",
                    severity=ErrorSeverity.HIGH,
                    context={"system_state": system_state},
                )
                errors.append(error)
            
            elif isinstance(value, dict):
                # 예상 키 확인
                if "error" in value:
                    error = Error(
                        engine=key,
                        error_type=value.get("error_type", "unknown"),
                        message=value.get("error_message", "알 수 없는 오류"),
                        severity=ErrorSeverity.HIGH,
                        context=value,
                    )
                    errors.append(error)
        
        # 오류 기록
        self.errors.extend(errors)
        self.stats["total_errors"] += len(errors)
        
        for error in errors:
            error_type = error.error_type
            self.stats["error_types"][error_type] = \
                self.stats["error_types"].get(error_type, 0) + 1
        
        return errors
    
    def _check_health(
        self,
        system_state: Dict[str, Any],
    ) -> SystemHealth:
        """시스템 건강 점검
        
        Args:
            system_state: 시스템 상태
        
        Returns:
            시스템 건강 상태
        """
        engine_health = {}
        total_score = 0.0
        count = 0
        
        # 각 엔진의 건강 점수 계산
        for key, value in system_state.items():
            if isinstance(value, dict):
                # 오류가 있으면 점수 감점
                score = 1.0
                
                if "error" in value:
                    score -= 0.5
                
                if "warning" in value:
                    score -= 0.2
                
                # 값 유효성 검사
                for k, v in value.items():
                    if isinstance(v, (int, float)):
                        if v < 0 or v > 1:
                            score -= 0.1
                
                score = max(0.0, min(1.0, score))
                engine_health[key] = score
                total_score += score
                count += 1
        
        # 전체 건강 점수
        overall_score = total_score / count if count > 0 else 0.0
        
        # 갈등 및 오류 수
        conflicts_count = len(self.conflicts)
        errors_count = len([e for e in self.errors if e.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]])
        warnings_count = len(self.warnings)
        
        health = SystemHealth(
            overall_score=overall_score,
            engine_health=engine_health,
            conflicts_count=conflicts_count,
            errors_count=errors_count,
            warnings_count=warnings_count,
        )
        
        # 건강 이력 저장 (연구용)
        if self.mode == "research":
            self.health_history.append(health)
            # 최근 100개만 유지
            if len(self.health_history) > 100:
                self.health_history = self.health_history[-100:]
        
        return health
    
    def _generate_recommendations(
        self,
        conflicts: List[Conflict],
        errors: List[Error],
        health: SystemHealth,
    ) -> List[str]:
        """복구 권장사항 생성
        
        Args:
            conflicts: 갈등 리스트
            errors: 오류 리스트
            health: 건강 상태
        
        Returns:
            권장사항 리스트
        """
        recommendations = []
        
        # 건강 점수가 낮으면
        if health.overall_score < 0.5:
            recommendations.append("시스템 건강 점수가 낮습니다. 안정화가 필요합니다.")
        
        # 갈등이 있으면
        if len(conflicts) > 0:
            recommendations.append(f"갈등이 {len(conflicts)}개 발생했습니다. 엔진 간 데이터 일관성을 확인하세요.")
        
        # 오류가 있으면
        if len(errors) > 0:
            high_severity_errors = [e for e in errors if e.severity in [ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]]
            if high_severity_errors:
                recommendations.append(f"심각한 오류 {len(high_severity_errors)}개 발생. 즉시 조치가 필요합니다.")
            else:
                recommendations.append(f"오류 {len(errors)}개 발생. 점검이 필요합니다.")
        
        # 특정 엔진 건강 점수가 낮으면
        for engine, score in health.engine_health.items():
            if score < 0.5:
                recommendations.append(f"엔진 '{engine}'의 건강 점수가 낮습니다 ({score:.2f}). 점검이 필요합니다.")
        
        return recommendations
    
    def get_state(self) -> Dict[str, Any]:
        """현재 상태 반환"""
        return {
            "mode": self.mode,
            "conflicts_count": len(self.conflicts),
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings),
            "stats": self.stats.copy(),
            "latest_health": self.health_history[-1] if self.health_history else None,
        }
    
    def reset(self):
        """상태 리셋"""
        self.conflicts.clear()
        self.errors.clear()
        self.warnings.clear()
        self.health_history.clear()
        self.stats = {
            "total_conflicts": 0,
            "total_errors": 0,
            "total_warnings": 0,
            "conflict_types": {},
            "error_types": {},
        }
        
        if self.logger:
            self.logger.info("Cingulate Cortex 상태 리셋 완료")

