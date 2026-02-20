#!/usr/bin/env python3
"""
PHAM 블록체인 서명 스크립트

BrainCore v0.3.0을 PHAM 블록체인에 서명

Author: GNJz (Qquarts)
Version: 0.3.0
"""

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path


def calculate_code_hash():
    """코드 해시 계산"""
    files = []
    for root, dirs, filenames in Path("src").rglob("*.py"):
        # 제외할 디렉토리
        if any(excluded in str(root) for excluded in ['.git', '__pycache__', '.pytest_cache', 'build', 'dist']):
            continue
        files.append(root / filename for filename in filenames)
    
    # 중복 제거 및 정렬
    files = sorted(set(files))
    
    content = ''
    for filepath in files:
        try:
            content += filepath.read_text(encoding='utf-8')
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
    
    return hashlib.sha256(content.encode('utf-8')).hexdigest(), len(files)


def prepare_signing_data():
    """서명 데이터 준비"""
    hash_value, file_count = calculate_code_hash()
    
    signing_data = {
        "module_name": "BrainCore (CookiieKernel)",
        "version": "0.3.0",
        "sha256": hash_value,
        "file_count": file_count,
        "description": "상태 중심 동역학 통합 인프라",
        "purpose": "산업용 브레인 플랫폼 (연구/철학적 확장 가능)",
        "signing_time": datetime.now().isoformat(),
    }
    
    return signing_data


def main():
    """메인 함수"""
    print("=" * 60)
    print("PHAM 블록체인 서명 준비")
    print("=" * 60)
    
    signing_data = prepare_signing_data()
    
    print("\n서명 정보:")
    print(f"  모듈명: {signing_data['module_name']}")
    print(f"  버전: {signing_data['version']}")
    print(f"  SHA256: {signing_data['sha256']}")
    print(f"  파일 수: {signing_data['file_count']}")
    print(f"  설명: {signing_data['description']}")
    print()
    
    # 서명 데이터를 JSON 파일로 저장
    signing_file = Path("pham_signing_data.json")
    signing_file.write_text(json.dumps(signing_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✅ 서명 데이터 저장: {signing_file}")
    print()
    
    print("=" * 60)
    print("PHAM 블록체인 서명 절차:")
    print("=" * 60)
    print("1. PHAM 블록체인에 접속")
    print("2. 위 서명 정보를 입력")
    print("3. 서명 실행")
    print("4. TxID를 받아서 기록")
    print("=" * 60)
    
    # PHAM API가 있다면 여기서 서명 시도
    # 현재는 수동 서명 필요
    print("\n⚠️  자동 서명을 위해서는 PHAM 블록체인 API가 필요합니다.")
    print("   현재는 수동 서명이 필요합니다.")
    print(f"\n서명 데이터 파일: {signing_file}")
    print("이 파일을 PHAM 블록체인에 업로드하여 서명하세요.")


if __name__ == "__main__":
    main()

