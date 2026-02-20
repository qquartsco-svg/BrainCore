"""
BrainCore Engines - 뇌 엔진 모듈

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from .cingulate_cortex import (
    CingulateCortexEngine,
    Conflict,
    Error,
    SystemHealth,
    ConflictType,
    ErrorSeverity,
)

__version__ = "0.1.0"

__all__ = [
    "CingulateCortexEngine",
    "Conflict",
    "Error",
    "SystemHealth",
    "ConflictType",
    "ErrorSeverity",
]

