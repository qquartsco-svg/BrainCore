"""
Real Engine Imports - 실제 엔진 import 경로 설정

실제 엔진들을 import하는 헬퍼 모듈

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional, Any

__version__ = "0.1.0"

# 엔진 경로 설정
BRAIN_ROOT = Path("/Users/jazzin/Desktop/00_BRAIN/Brain_Disorder_Simulation_Engine/Unsolved_Problems_Engines")

WELL_FORMATION_PATH = BRAIN_ROOT / "WellFormationEngine" / "src"
STATE_MANIFOLD_PATH = BRAIN_ROOT / "StateManifoldEngine" / "src"
HISTORICAL_DATA_PATH = BRAIN_ROOT / "HistoricalDataReconstructor" / "src"
NEURAL_DYNAMICS_PATH = Path("/Users/jazzin/Desktop/00_BRAIN/Engines/Independent/Dynamics_Engine")


def add_engine_paths():
    """엔진 경로를 sys.path에 추가"""
    paths = [
        str(WELL_FORMATION_PATH),
        str(STATE_MANIFOLD_PATH),
        str(HISTORICAL_DATA_PATH),
    ]
    
    if NEURAL_DYNAMICS_PATH:
        paths.append(str(NEURAL_DYNAMICS_PATH))
    
    for path in paths:
        if Path(path).exists() and path not in sys.path:
            sys.path.insert(0, path)


def import_well_formation_engine() -> Optional[Any]:
    """WellFormationEngine import"""
    try:
        add_engine_paths()
        from well_formation_engine.engine import WellFormationEngine
        return WellFormationEngine
    except ImportError as e:
        print(f"Warning: WellFormationEngine import failed: {e}")
        return None


def import_state_manifold_engine() -> Optional[Any]:
    """StateManifoldEngine import"""
    try:
        add_engine_paths()
        from state_manifold_engine.state_manifold_engine import StateManifoldEngine
        return StateManifoldEngine
    except ImportError as e:
        print(f"Warning: StateManifoldEngine import failed: {e}")
        return None


def import_historical_data_reconstructor() -> Optional[Any]:
    """HistoricalDataReconstructor import"""
    try:
        add_engine_paths()
        from historical_data_reconstructor.engine import HistoricalDataReconstructor
        return HistoricalDataReconstructor
    except ImportError as e:
        print(f"Warning: HistoricalDataReconstructor import failed: {e}")
        return None


def import_neural_dynamics_core() -> Optional[Any]:
    """NeuralDynamicsCore import"""
    try:
        add_engine_paths()
        
        # 여러 가능한 import 경로 시도
        try:
            from dynamics_engine.dynamics_engine import NeuralDynamicsCore
            return NeuralDynamicsCore
        except ImportError:
            try:
                from dynamics_engine import NeuralDynamicsCore
                return NeuralDynamicsCore
            except ImportError:
                try:
                    from neural_dynamics_core import NeuralDynamicsCore
                    return NeuralDynamicsCore
                except ImportError:
                    pass
    except ImportError as e:
        print(f"Warning: NeuralDynamicsCore import failed: {e}")
        return None
    except Exception as e:
        print(f"Warning: NeuralDynamicsCore import error: {e}")
        return None

