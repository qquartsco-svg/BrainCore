"""
Engine Wrappers - 엔진 래퍼

기존 엔진들을 상태계 중심 구조로 래핑

수학적 배경:
각 엔진은 GlobalState를 입력받아 상태를 perturb하는 함수:
    state_{t+1} = engine.update(state_t)

여기서:
- state_t: 시간 t에서의 GlobalState
- engine.update: 엔진별 상태 변환 함수
- state_{t+1}: 시간 t+1에서의 업데이트된 상태

Author: GNJz (Qquarts)
Version: 0.2.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional, List
import numpy as np
import sys
from pathlib import Path

from .global_state import GlobalState
from .execution_modes import SelfOrganizingEngine

__version__ = "0.2.0"


class WellFormationEngineWrapper(SelfOrganizingEngine):
    """WellFormationEngine 래퍼
    
    역할: L0 초기화기 (W, b 설정)
    
    수학적 배경:
    WellFormationEngine은 Hebbian 학습을 통해 W, b를 생성:
        Δw_ij = η · pre_i · post_j - λ · w_ij
    
    여기서:
    - η: 학습률 (hebbian_config.eta)
    - λ: 가중치 감쇠 계수 (hebbian_config.weight_decay)
    - pre_i: pre-synaptic 뉴런 i의 활동
    - post_j: post-synaptic 뉴런 j의 활동
    
    생성된 W, b는 L0 (NeuralDynamicsCore)의 에너지 지형을 형성:
        E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
    """
    
    def __init__(self, well_formation_engine: Any):
        """WellFormationEngineWrapper 초기화
        
        Args:
            well_formation_engine: WellFormationEngine 인스턴스
        """
        self.engine = well_formation_engine
        self.name = "well_formation"
    
    def update(self, state: GlobalState) -> GlobalState:
        """L0 초기화 (W, b 설정)
        
        수식:
        - 입력: episodes (Episode 리스트)
        - 출력: W (가중치 행렬), b (바이어스 벡터)
        - 과정: Hebbian 학습 → 안정성 제약 적용
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태 (state.extensions["L0"]에 W, b 저장)
        """
        # L0 가중치가 없으면 생성
        l0_data = state.get_extension("L0")
        if l0_data is None or l0_data.get("weights") is None:
            # WellFormationEngine으로 W, b 생성
            # episodes는 state.extensions에서 가져오거나 기본값 사용
            well_formation_data = state.get_extension("well_formation", {})
            episodes = well_formation_data.get("episodes", [])
            
            if episodes:
                # Hebbian 학습으로 W, b 생성
                well_result = self.engine.generate_well(episodes)
                
                # L0 extension에 저장
                # 수식: E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
                state.set_extension("L0", {
                    "weights": np.array(well_result.W),  # W 행렬
                    "bias": np.array(well_result.b),     # b 벡터
                    "converged": False,                   # 수렴 여부
                    "analysis": well_result.analysis,     # 형성 원인 분석
                })
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        return state.energy
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        return {"name": self.name, "engine": str(self.engine)}
    
    def reset(self):
        """상태 리셋"""
        pass


class StateManifoldEngineWrapper(SelfOrganizingEngine):
    """StateManifoldEngine 래퍼
    
    역할: L0 제약 조건 생성기 (risk_map 설정)
    
    수학적 배경:
    StateManifoldEngine은 여러 난제의 위험 지형을 통합:
        risk(condition) = f(risk_1(condition), risk_2(condition), ...)
    
    여기서:
    - risk_i: i번째 난제의 위험도
    - f: 유기적 결합 함수 (단순 평균 + 유기적 증폭)
    
    유기적 증폭:
    여러 차원에서 동시에 위험한 경우:
        risk_amplified = risk_base · (1 + (high_risk_count - 1) · 0.2)
    
    여기서:
    - risk_base: 기본 위험도 (평균)
    - high_risk_count: 위험도 > 0.7인 차원 수
    """
    
    def __init__(self, state_manifold_engine: Any):
        """StateManifoldEngineWrapper 초기화
        
        Args:
            state_manifold_engine: StateManifoldEngine 인스턴스
        """
        self.engine = state_manifold_engine
        self.name = "state_manifold"
    
    def update(self, state: GlobalState) -> GlobalState:
        """제약 조건 생성 (risk_map 설정)
        
        수식:
        - 입력: search_biases (SearchBias 딕셔너리)
        - 출력: risk_map (조건 서명 → 위험도)
        - 과정: 상태 공간 구축 → 위험 지형 추출
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태 (state.extensions["L1"]에 risk_map 저장)
        """
        # risk_map이 없으면 생성
        if state.risk_map is None:
            # StateManifoldEngine으로 risk_map 생성
            # search_biases는 state.extensions에서 가져오거나 기본값 사용
            state_manifold_data = state.get_extension("state_manifold", {})
            search_biases = state_manifold_data.get("search_biases", {})
            
            if search_biases:
                # 상태 공간 구축
                manifold = self.engine.build_state_space(search_biases)
                
                # L1 extension에 저장
                # risk_map 추출
                risk_map = {}
                for dim_name, bias in manifold.dimensions.items():
                    if hasattr(bias, 'risk_map'):
                        # 각 차원의 risk_map 통합
                        risk_map.update(bias.risk_map)
                    elif isinstance(bias, dict) and 'risk_map' in bias:
                        risk_map.update(bias['risk_map'])
                
                state.set_extension("L1", {
                    "risk_map": risk_map,                      # 위험 지형
                    "dimensions": manifold.dimensions,         # 상태 공간 차원
                    "organic_connections": manifold.organic_connections,  # 유기적 연결
                    "collapse_zones": manifold.collapse_zones, # 붕괴 영역
                })
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        return state.energy
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        return {"name": self.name, "engine": str(self.engine)}
    
    def reset(self):
        """상태 리셋"""
        pass


class NeuralDynamicsCoreWrapper(SelfOrganizingEngine):
    """NeuralDynamicsCore (L0) 래퍼
    
    역할: 실제 동역학 상태가 살아있는 코어
    
    수학적 배경:
    NeuralDynamicsCore는 연속시간 신경 동역학을 시뮬레이션:
        τ · dx/dt = -x + f(Wx + I + b)
    
    여기서:
    - τ: 시간 상수
    - x: 뉴런 상태 벡터
    - W: 연결 가중치 행렬
    - I: 외부 입력 벡터
    - b: 바이어스 벡터
    - f: 활성화 함수
    
    에너지 함수 (Hopfield):
        E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
    
    동역학은 에너지를 감소시키는 방향으로 진행:
        dE/dt ≤ 0 (Lyapunov 안정성)
    """
    
    def __init__(self, neural_dynamics_core: Any):
        """NeuralDynamicsCoreWrapper 초기화
        
        Args:
            neural_dynamics_core: NeuralDynamicsCore 인스턴스
        """
        self.core = neural_dynamics_core
        self.name = "neural_dynamics"
    
    def update(self, state: GlobalState) -> GlobalState:
        """동역학 실행 (state_vector, energy 업데이트)
        
        수식:
        - 입력: state.state_vector (x0), W, b
        - 출력: x_trajectory (x(t) 궤적)
        - 과정: τ · dx/dt = -x + f(Wx + I + b) 적분
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태 (state.state_vector, state.energy 업데이트)
        """
        # L0 가중치 확인
        l0_data = state.get_extension("L0")
        if l0_data:
            W = l0_data.get("weights")
            b = l0_data.get("bias")
            
            if W is not None and b is not None:
                # L0 실행
                # 수식: τ · dx/dt = -x + f(Wx + I + b)
                try:
                    x_trajectory = self.core.run(
                        x0=state.state_vector,
                        W=W.tolist() if isinstance(W, np.ndarray) else W,
                        b=b.tolist() if isinstance(b, np.ndarray) else b,
                    )
                    
                    # 상태 업데이트
                    if isinstance(x_trajectory, list) and len(x_trajectory) > 0:
                        state.state_vector = np.array(x_trajectory[-1])
                    
                    # 에너지 계산
                    # 수식: E(x) = -(1/2) Σ_ij w_ij x_i x_j - Σ_i b_i x_i
                    if hasattr(self.core, 'hopfield_energy'):
                        state.energy = self.core.hopfield_energy(state.state_vector)
                    
                    # 수렴 여부 업데이트
                    state.update_extension("L0", {
                        "converged": len(x_trajectory) < 100,  # 간단한 수렴 체크
                    })
                except Exception as e:
                    # 오류 발생 시 상태 유지
                    pass
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        return state.energy
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        return {"name": self.name, "core": str(self.core)}
    
    def reset(self):
        """상태 리셋"""
        pass


class HistoricalDataReconstructorWrapper(SelfOrganizingEngine):
    """HistoricalDataReconstructor 래퍼
    
    역할: L0 상태 기록기 (causal_links 기록)
    
    수학적 배경:
    HistoricalDataReconstructor는 인과 네트워크를 추출:
        causal_link = (fragment_i, fragment_j, strength)
    
    여기서:
    - fragment_i: 이전 데이터 단편
    - fragment_j: 이후 데이터 단편
    - strength: 인과 강도 (0.0 ~ 1.0)
    
    스토리라인 생성:
    인과 링크를 따라 역추적하여 원인을 찾음:
        storyline = [fragment_0, fragment_1, ..., fragment_n]
    """
    
    def __init__(self, historical_reconstructor: Any):
        """HistoricalDataReconstructorWrapper 초기화
        
        Args:
            historical_reconstructor: HistoricalDataReconstructor 인스턴스
        """
        self.reconstructor = historical_reconstructor
        self.name = "historical"
    
    def update(self, state: GlobalState) -> GlobalState:
        """상태 기록 (causal_links 기록)
        
        수식:
        - 입력: state.state_vector, state.energy, state.step
        - 출력: fragment (DataFragment)
        - 과정: 현재 상태를 fragment로 변환 → 인과 링크 분석
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태 (state.extensions["L2"]에 causal_links 기록)
        """
        # 현재 상태를 DataFragment로 변환
        try:
            fragment = self.reconstructor.collect_fragment(
                content=f"State at step {state.step}",
                source="BrainCore",
                timestamp=state.timestamp,
            )
            
            # 인과 링크 분석
            l2_data = state.get_extension("L2", {})
            causal_links = l2_data.get("causal_links", [])
            
            # 새 fragment 추가
            if fragment:
                causal_links.append(fragment)
            
            # L2 extension에 저장
            state.set_extension("L2", {
                "causal_links": causal_links,
                "storyline": l2_data.get("storyline", []),
            })
        except Exception as e:
            # 오류 발생 시 상태 유지
            pass
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        return state.energy
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        return {"name": self.name, "reconstructor": str(self.reconstructor)}
    
    def reset(self):
        """상태 리셋"""
        pass


class CingulateCortexEngineWrapper(SelfOrganizingEngine):
    """CingulateCortexEngine 래퍼
    
    역할: L0 안정성 모니터 (risk, health 체크)
    
    수학적 배경:
    CingulateCortexEngine은 시스템 건강 점수를 계산:
        health_score = 1.0 - (conflict_weight + error_weight)
    
    여기서:
    - conflict_weight: 갈등 가중치
    - error_weight: 오류 가중치
    
    위험도:
        risk = 1.0 - health_score
    
    Extensions별 검사:
    각 extension의 유효성을 검사하여 경고 생성
    """
    
    def __init__(self, cingulate_cortex: Any):
        """CingulateCortexEngineWrapper 초기화
        
        Args:
            cingulate_cortex: CingulateCortexEngine 인스턴스
        """
        self.cingulate = cingulate_cortex
        self.name = "cingulate"
    
    def update(self, state: GlobalState) -> GlobalState:
        """안정성 모니터링 (risk, health 체크)
        
        수식:
        - 입력: state.state_vector, state.energy, state.extensions
        - 출력: health_score, conflicts, errors
        - 과정: 모니터링 → 위험도 계산 → Extensions 검사
        
        Args:
            state: 현재 상태
        
        Returns:
            업데이트된 상태 (state.risk, state.metadata["monitoring"] 업데이트)
        """
        # 모니터링
        try:
            monitoring = self.cingulate.monitor({
                "state_vector": state.state_vector.tolist(),
                "energy": state.energy,
                "risk_map": state.risk_map,
                "extensions": state.extensions,
            })
            
            # 위험도 업데이트
            # 수식: risk = 1.0 - health_score
            health_score = monitoring.get("health_score", 1.0)
            state.risk = 1.0 - health_score  # health_score가 낮을수록 risk가 높음
            
            # 메타데이터에 모니터링 결과 저장
            state.metadata["monitoring"] = monitoring
            
            # Extensions별 검사 (Cingulate 확장)
            # get_extension()을 사용하여 접근
            for engine_name in state.extensions.keys():
                extension_data = state.get_extension(engine_name)
                # 각 extension의 유효성 검사
                if isinstance(extension_data, dict):
                    # 간단한 검사: None 값 체크
                    if any(v is None for v in extension_data.values()):
                        state.metadata.setdefault("extension_warnings", []).append(
                            f"{engine_name}: None 값 발견"
                        )
        except Exception as e:
            # 오류 발생 시 상태 유지
            pass
        
        return state
    
    def get_energy(self, state: GlobalState) -> float:
        """상태의 에너지 반환
        
        Args:
            state: 상태
        
        Returns:
            에너지
        """
        return state.energy
    
    def get_state(self) -> Dict[str, Any]:
        """엔진 내부 상태 반환"""
        return {"name": self.name, "cingulate": str(self.cingulate)}
    
    def reset(self):
        """상태 리셋"""
        pass
