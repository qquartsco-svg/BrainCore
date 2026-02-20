# PHAM 블록체인 서명 지침

**모듈명**: BrainCore (CookiieKernel)  
**버전**: 0.3.0  
**작성일**: 2026-02-05

---

## 📋 서명 전 준비사항

### 1. 코드 해시 계산

**계산 대상**:
- `src/brain_core/` 디렉토리 내 모든 Python 파일
- 제외: `.git`, `__pycache__`, `.pyc`, `build`, `dist`

**계산 방법**:
```bash
cd /Users/jazzin/Desktop/00_BRAIN/BrainCore
python3 calculate_hash.py
```

**예상 결과**:
- SHA256 해시값
- 파일 개수

---

### 2. 서명 정보 준비

**필요한 정보**:
- 모듈명: BrainCore (CookiieKernel)
- 버전: 0.3.0
- SHA256 해시값
- 서명 목적: 코드 무결성 보장

---

## 🔐 PHAM 블록체인 서명 절차

### 1단계: 해시 계산 완료 확인

- [x] 코드 해시 계산 완료
- [ ] 해시값 확인

### 2단계: PHAM 블록체인 서명

**서명 방법**:
1. PHAM 블록체인에 접속
2. 코드 해시값 입력
3. 모듈 정보 입력 (이름, 버전, 설명)
4. 서명 실행
5. TxID 기록

**서명 내용**:
```
모듈명: BrainCore (CookiieKernel)
버전: 0.3.0
SHA256: [계산된 해시값]
설명: 상태 중심 동역학 통합 인프라
```

### 3단계: 서명 결과 기록

**PHAM_SIGNATURE.md 업데이트**:
- TxID 기록
- 블록 높이 기록
- 서명 시간 기록
- 서명 검증 완료 표시

---

## ✅ 서명 완료 체크리스트

- [ ] 코드 해시 계산 완료
- [ ] PHAM 블록체인 서명 완료
- [ ] TxID 기록 완료
- [ ] 블록 높이 기록 완료
- [ ] 서명 시간 기록 완료
- [ ] PHAM_SIGNATURE.md 업데이트 완료
- [ ] 서명 검증 완료

---

## 📝 서명 후 작업

1. **PHAM_SIGNATURE.md 업데이트**
   - TxID 기록
   - 블록 높이 기록
   - 서명 시간 기록

2. **README.md 업데이트**
   - PHAM 서명 정보 추가
   - 버전 정보 업데이트

3. **Git 태그 생성**
   ```bash
   git tag -a v0.3.0 -m "BrainCore v0.3.0 - PHAM Signed"
   ```

---

**작성자**: GNJz (Qquarts)  
**상태**: 서명 준비 완료

