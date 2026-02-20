"""
Cognitive Kernel 엔진 통합

Cognitive_Kernel의 엔진들을 BrainCore에 통합

Author: GNJz (Qquarts)
Version: 0.1.0
"""

from __future__ import annotations

from typing import Dict, Any, Optional
import sys
from pathlib import Path

from ..engine_adapters import EngineAdapter
from ..brain_core import BrainCore

__version__ = "0.1.0"


class CognitiveKernelIntegration:
    """Cognitive Kernel 엔진 통합 헬퍼"""
    
    def __init__(self, cognitive_kernel_path: Optional[str] = None):
        """CognitiveKernelIntegration 초기화
        
        Args:
            cognitive_kernel_path: Cognitive_Kernel 경로 (None이면 자동 탐색)
        """
        if cognitive_kernel_path is None:
            # 자동 탐색
            base_path = Path(__file__).parent.parent.parent.parent.parent.parent
            cognitive_kernel_path = str(base_path / "Cognitive_Kernel")
        
        self.cognitive_kernel_path = cognitive_kernel_path
        self._engines_loaded = {}
    
    def load_thalamus(self) -> Optional[Any]:
        """Thalamus 엔진 로드
        
        Returns:
            Thalamus 엔진 인스턴스 (None이면 로드 실패)
        """
        try:
            thalamus_path = Path(self.cognitive_kernel_path) / "Thalamus" / "src"
            if thalamus_path.exists():
                sys.path.insert(0, str(thalamus_path))
                from thalamus import ThalamusEngine
                self._engines_loaded["thalamus"] = ThalamusEngine
                return ThalamusEngine
        except ImportError as e:
            print(f"Thalamus 엔진 로드 실패: {e}")
            return None
    
    def load_amygdala(self) -> Optional[Any]:
        """Amygdala 엔진 로드
        
        Returns:
            Amygdala 엔진 인스턴스 (None이면 로드 실패)
        """
        try:
            amygdala_path = Path(self.cognitive_kernel_path) / "Amygdala" / "src"
            if amygdala_path.exists():
                sys.path.insert(0, str(amygdala_path))
                from amygdala import AmygdalaEngine
                self._engines_loaded["amygdala"] = AmygdalaEngine
                return AmygdalaEngine
        except ImportError as e:
            print(f"Amygdala 엔진 로드 실패: {e}")
            return None
    
    def integrate_to_core(
        self,
        core: BrainCore,
        engine_names: Optional[list] = None,
    ) -> Dict[str, bool]:
        """엔진들을 BrainCore에 통합
        
        Args:
            core: BrainCore 인스턴스
            engine_names: 통합할 엔진 이름 리스트 (None이면 모두)
        
        Returns:
            통합 결과 딕셔너리 {엔진명: 성공여부}
        """
        if engine_names is None:
            engine_names = ["thalamus", "amygdala"]
        
        results = {}
        
        for engine_name in engine_names:
            try:
                if engine_name == "thalamus":
                    EngineClass = self.load_thalamus()
                    if EngineClass:
                        engine = EngineClass()
                        adapter = EngineAdapter(
                            engine=engine,
                            name="thalamus",
                            mode=core.mode,
                        )
                        core.register_engine("thalamus", adapter, priority=1)
                        results["thalamus"] = True
                    else:
                        results["thalamus"] = False
                
                elif engine_name == "amygdala":
                    EngineClass = self.load_amygdala()
                    if EngineClass:
                        engine = EngineClass()
                        adapter = EngineAdapter(
                            engine=engine,
                            name="amygdala",
                            mode=core.mode,
                        )
                        core.register_engine("amygdala", adapter, priority=2)
                        results["amygdala"] = True
                    else:
                        results["amygdala"] = False
                
            except Exception as e:
                print(f"엔진 {engine_name} 통합 실패: {e}")
                results[engine_name] = False
        
        return results

