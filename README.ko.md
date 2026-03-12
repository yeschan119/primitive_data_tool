# Pharmacovigilance Analytics Tool
### 의약품 부작용(ADR) 데이터 분석 및 보고 시스템

대웅제약 **Pharmacovigilance(PV)팀**에서 사용하는  
의약품 부작용(ADR: Adverse Drug Reaction) 원시 데이터를 분석하고  
보고서를 자동 생성하기 위해 개발한 **Pharmacovigilance 데이터 분석 도구**입니다.

본 시스템은 대량의 의약품 부작용 데이터를 처리하여  
**Line Listing** 및 **Summary Tabulation** 형태의 안전성 보고서를 자동 생성합니다.

또한 개발 환경 없이도 실행할 수 있도록 **Standalone Executable Application** 형태로 배포할 수 있도록 설계되었습니다.

---

# 프로젝트 개요

Pharmacovigilance 팀은 의약품 부작용 데이터를 지속적으로 분석하여  
잠재적인 안전성 신호(Safety Signal)를 탐지해야 합니다.

이 프로젝트는 이러한 분석 과정을 자동화하여  
데이터 처리부터 보고서 생성까지의 과정을 **데이터 파이프라인 형태로 구현**한 시스템입니다.

주요 기능

- ADR 원시 데이터 자동 처리
- 의약품 코드 기반 데이터 분석
- 기간 기반 보고서 생성
- GUI 기반 분석 도구
- 실행파일 형태 배포
- 클라우드 기반 인증 시스템

---

# 주요 기능

## ADR 데이터 처리

Pharmacovigilance 원시 데이터를 자동으로 처리하는 기능을 구현했습니다.

기능

- 제품 코드 기반 데이터 필터링
- 기간 기반 데이터 분석
- Pandas 기반 데이터 전처리 및 변환

---

## 보고서 생성

다음 두 가지 형태의 보고서를 생성합니다.

### Line Listing

개별 부작용 사례에 대한 상세 데이터를 제공하는 보고서

사용 목적

- 개별 부작용 사례 분석
- 규제기관 보고

---

### Summary Tabulation

부작용 데이터를 집계하여 통계 형태로 제공하는 보고서

사용 목적

- 안전성 신호 탐지
- 부작용 발생 패턴 분석

---

## GUI 기반 분석 도구

Tkinter를 활용하여 **데스크탑 GUI 프로그램**을 개발했습니다.

주요 기능

- 제품 코드 입력
- 분석 시작일 / 종료일 설정
- 보고서 생성 진행 상태 표시 (Progress Bar)
- 입력값 검증 및 오류 메시지 출력

이를 통해 **개발 지식이 없는 PV 분석가도 쉽게 사용할 수 있는 도구**를 구현했습니다.

---

## 실행파일 배포

개발 환경 없이 실행할 수 있도록  
**Standalone Executable Application** 형태로 패키징했습니다.

구현 과정

1. Jupyter Notebook 코드 → Python Module 변환
2. GUI 프로그램 개발
3. PyInstaller를 이용한 실행파일 생성

예시 명령어

```
pyinstaller --name PV_ADR_Analyzer \
--onefile guiapp.py \
--noconsole
```

---

## 실행 환경 최적화

초기 개발 환경

```
Anaconda 환경 약 300MB
```

최적화 이후

```
Custom virtualenv 약 30MB
```

결과

- 약 **90% 실행 환경 크기 감소**
- 실행파일 배포 효율 향상

---

## 클라우드 기반 인증 시스템

AWS RDS(MySQL)를 활용하여  
사용자 인증 시스템을 구축했습니다.

기능

- 사용자 로그인 인증
- 클라이언트 접근 제어
- 중앙 인증 관리

예시 SQL

```
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON login.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

---

# 기술 스택

| 분야 | 기술 |
|-----|------|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | MySQL |
| Cloud | AWS RDS |
| GUI | Tkinter |
| Packaging | PyInstaller |

---

# 프로젝트 구조

```
data/
  테스트용 Pharmacovigilance 데이터

code/
  ADR 분석 및 보고서 생성 핵심 로직

sub_code/
  테스트 및 실험 코드

demo/
  시스템 시연 영상
```

테스트 데이터 예시

```
제품코드 : 201701182
시작일자 : 2017-02-13
종료일자 : 현재
```

---

# 보안 고려사항

소스 코드 보호를 위해 다음 방법을 검토했습니다.

검토 방법

- Python 코드 암호화
- Cython 컴파일
- PyInstaller 패키징

최종 적용

- 실행파일 형태 배포
- 코드 난독화
- 인증 시스템 적용

---

# Cross Platform 테스트

다양한 환경에서 테스트를 수행했습니다.

테스트 환경

- Mac → Windows
- Windows → Mac
- Windows → Windows

목적

다양한 OS 환경에서도 실행파일이 정상 동작하도록 검증

---

# 주요 이슈

## MedDRA Dictionary 라이선스 문제

MedDRA Dictionary는 라이선스 문제로  
실행파일과 함께 배포가 어렵습니다.

해결 방안

- MedDRA 데이터를 서버에 저장
- API 형태로 조회

---

## 데이터 Edge Case 처리

테스트 사례

```
제품코드 : 197000040
```

결과

- Summary Tabulation 정상 생성
- Line Listing 데이터 없음

해결

Line Listing 데이터가 없는 경우

```
해당 제품에 대한 부작용 보고가 없습니다
```

메시지 출력

---

# 프로젝트 결과

- Pharmacovigilance ADR 분석 도구 개발
- 의약품 부작용 보고 자동화
- 실행파일 형태 분석 프로그램 제공
- 클라우드 기반 인증 시스템 구축
- 실행 환경 크기 약 **90% 감소**

---

# 팀 구성

Eungchan Kang — Pharmacovigilance Team  
Jisun Jang — IT Operations Team
