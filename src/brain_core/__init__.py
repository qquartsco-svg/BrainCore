"""
BrainCore - 뇌 코어 오케스트레이터

산업용 중심 + 연구/철학적 확장 가능한 뇌 통합 시스템

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from .brain_core import BrainCore
from .engine_registry import EngineRegistry
from .execution_loop import ExecutionLoop
from .state_centric_execution_loop import StateCentricExecutionLoop
from .data_flow import DataFlowManager
from .interfaces import BrainEngine, BrainEngineBase, DataConverter, StateSynchronizer
from .engine_adapters import EngineAdapter, MockEngineAdapter
from .global_state import GlobalState
from .execution_modes import ExecutionMode, SelfOrganizingEngine, ControllerEngine
from .engine_wrappers import (
    WellFormationEngineWrapper,
    StateManifoldEngineWrapper,
    NeuralDynamicsCoreWrapper,
    HistoricalDataReconstructorWrapper,
    CingulateCortexEngineWrapper,
)

__version__ = "0.2.0"

__all__ = [
    "BrainCore",
    "EngineRegistry",
    "ExecutionLoop",
    "StateCentricExecutionLoop",
    "DataFlowManager",
    "BrainEngine",
    "BrainEngineBase",
    "DataConverter",
    "StateSynchronizer",
    "EngineAdapter",
    "MockEngineAdapter",
    "GlobalState",
    "ExecutionMode",
    "SelfOrganizingEngine",
    "ControllerEngine",  # 확장 가능성 (현재 사용 안 함)
    "WellFormationEngineWrapper",
    "StateManifoldEngineWrapper",
    "NeuralDynamicsCoreWrapper",
    "HistoricalDataReconstructorWrapper",
    "CingulateCortexEngineWrapper",
]

