#!/usr/bin/env python3
"""
문서 정리 스크립트
실행: python3 organize_docs.py
"""

import os
import shutil
from pathlib import Path

def main():
    base = Path(".")
    docs = base / "docs"
    
    # 폴더 생성
    for subdir in ["phases", "implementation", "concepts", "pham", "archive"]:
        (docs / subdir).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created docs/{subdir}/")
    
    # 파일 이동
    moves = {
        "phases": [
            "PHASE_1_2_COMPLETE.md",
            "PHASE_3_COMPLETE.md",
            "PHASE_4_PROGRESS.md",
        ],
        "implementation": [
            "IMPLEMENTATION_PLAN.md",
            "IMPLEMENTATION_STATUS.md",
            "IMPLEMENTATION_SUMMARY.md",
            "IMPLEMENTATION_ANALYSIS.md",
            "FEEDBACK_IMPLEMENTATION.md",
            "STATECENTRIC_REDESIGN.md",
            "STRATEGIC_DIAGNOSIS.md",
        ],
        "concepts": [
            "CONCEPT_DOCUMENTATION.md",
            "CORE_CONCEPT.md",
            "ENGINE_DEVELOPMENT_PHILOSOPHY.md",
            "ENGINE_DEVELOPMENT_ROADMAP.md",
        ],
        "pham": [
            "PHAM_SIGNED.md",
        ],
        "archive": [
            "COMPLETION_REPORT.md",
            "COMPLETION_SUMMARY.md",
            "COMPREHENSIVE_STATUS.md",
            "CURRENT_STATUS.md",
            "FINAL_COMPLETION_REPORT.md",
            "FINAL_STATUS.md",
            "FINAL_SUMMARY.md",
            "SUMMARY.md",
            "ENGINE_INTEGRATION_COMPLETE.md",
            "DATA_FLOW_INTEGRATION_COMPLETE.md",
            "CINGULATE_CORTEX_COMPLETE.md",
            "NEXT_STEPS_COMPLETE.md",
            "DIRECTIONAL_REVIEW.md",
            "DIRECTIONAL_ASSESSMENT.md",
            "SIMPLIFICATION_PLAN.md",
            "WORK_LOG.md",
            "TURBULENCE_ANALYSIS.md",
            "ENGINE_INTEGRATION_GUIDE.md",
        ],
    }
    
    moved = 0
    for category, files in moves.items():
        for filename in files:
            src = base / filename
            dst = docs / category / filename
            if src.exists():
                if dst.exists():
                    print(f"⚠ {filename} already exists in docs/{category}/, skipping")
                else:
                    try:
                        shutil.move(str(src), str(dst))
                        moved += 1
                        print(f"✓ {filename} → docs/{category}/")
                    except Exception as e:
                        print(f"✗ {filename}: {e}")
            else:
                print(f"⚠ {filename} not found, skipping")
    
    print(f"\n✅ 총 {moved}개 파일 이동 완료")
    
    # 결과 확인
    print("\n=== 메인 폴더 남은 문서 ===")
    remaining = list(base.glob("*.md"))
    for f in sorted(remaining):
        print(f"  {f.name}")
    
    print(f"\n메인 폴더에 {len(remaining)}개 문서가 남아있습니다.")

if __name__ == "__main__":
    main()

