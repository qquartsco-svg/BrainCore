#!/bin/bash
# 문서 정리 스크립트
# 실행: bash organize_docs.sh

cd "$(dirname "$0")"

# docs 폴더 생성
mkdir -p docs/{phases,implementation,concepts,pham,archive}

# phases 폴더로 이동
mv PHASE_*_COMPLETE.md PHASE_*_PROGRESS.md docs/phases/ 2>/dev/null

# implementation 폴더로 이동
mv IMPLEMENTATION_*.md FEEDBACK_IMPLEMENTATION.md STATECENTRIC_REDESIGN.md STRATEGIC_DIAGNOSIS.md docs/implementation/ 2>/dev/null

# concepts 폴더로 이동
mv CONCEPT_DOCUMENTATION.md CORE_CONCEPT.md ENGINE_DEVELOPMENT_*.md docs/concepts/ 2>/dev/null

# pham 폴더로 이동
mv PHAM_SIGNED.md docs/pham/ 2>/dev/null

# archive 폴더로 이동
mv COMPLETION_*.md COMPREHENSIVE_STATUS.md CURRENT_STATUS.md FINAL_*.md SUMMARY.md ENGINE_INTEGRATION_COMPLETE.md DATA_FLOW_INTEGRATION_COMPLETE.md CINGULATE_CORTEX_COMPLETE.md NEXT_STEPS_COMPLETE.md DIRECTIONAL_*.md SIMPLIFICATION_PLAN.md WORK_LOG.md TURBULENCE_ANALYSIS.md ENGINE_INTEGRATION_GUIDE.md docs/archive/ 2>/dev/null

echo "✅ 문서 정리 완료!"
echo ""
echo "메인 폴더 (핵심 문서):"
ls -1 *.md
echo ""
echo "docs 폴더 구조:"
find docs -type d | sort

