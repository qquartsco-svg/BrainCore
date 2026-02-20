#!/usr/bin/env python3
"""
BrainCore 코드 해시 계산 스크립트

PHAM 블록체인 서명을 위한 SHA256 해시 계산

Author: GNJz (Qquarts)
Version: 0.3.0
"""

import hashlib
import os
from datetime import datetime
from pathlib import Path


def calculate_directory_hash(directory):
    """디렉토리 내 모든 Python 파일의 해시 계산"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        # 제외할 디렉토리
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'build', 'dist']]
        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                files.append(filepath)
    
    files.sort()
    content = ''
    file_count = 0
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content += f.read()
            file_count += 1
        except Exception as e:
            print(f"Warning: Could not read {filepath}: {e}")
    
    hash_value = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return hash_value, file_count, files


def main():
    """메인 함수"""
    print("=" * 60)
    print("BrainCore (CookiieKernel) v0.3.0 - PHAM 서명 준비")
    print("=" * 60)
    
    hash_value, file_count, files = calculate_directory_hash('src')
    
    print(f"\nSHA256 해시: {hash_value}")
    print(f"파일 개수: {file_count}")
    print(f"\n계산 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n주요 파일:")
    for f in files[:10]:
        print(f"  - {f}")
    if len(files) > 10:
        print(f"  ... 외 {len(files) - 10}개 파일")
    
    print("\n" + "=" * 60)
    print("PHAM 블록체인 서명 정보:")
    print("=" * 60)
    print(f"모듈명: BrainCore (CookiieKernel)")
    print(f"버전: 0.3.0")
    print(f"SHA256: {hash_value}")
    print(f"설명: 상태 중심 동역학 통합 인프라")
    print("=" * 60)
    
    # PHAM_SIGNATURE.md에 해시값 기록
    signature_file = Path("PHAM_SIGNATURE.md")
    if signature_file.exists():
        content = signature_file.read_text(encoding='utf-8')
        content = content.replace(
            "**SHA256**: [계산 완료 - 서명 대기]",
            f"**SHA256**: {hash_value}"
        )
        content = content.replace(
            "**파일 수**: [계산 완료 - 서명 대기]",
            f"**파일 수**: {file_count}"
        )
        signature_file.write_text(content, encoding='utf-8')
        print("\n✅ PHAM_SIGNATURE.md 업데이트 완료")


if __name__ == "__main__":
    main()

