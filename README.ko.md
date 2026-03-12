# Python Pharmacovigilance Analytics Tool - 대응제약 악물감시팀 프로젝트
### Python 기반 의약품 부작용(ADR) 데이터 분석 자동화 시스템

Pharmacovigilance(PV) 팀의 **의약품 부작용(ADR) 원시 데이터**를  
**Python 기반 데이터 처리 파이프라인**으로 분석하여  
**Line Listing / Summary Tabulation 보고서**를 자동 생성하는 분석 도구입니다.

Python의 **Pandas 기반 데이터 처리**와 **Tkinter GUI 애플리케이션**을 활용하여  
비개발자도 사용할 수 있는 **데스크탑 분석 프로그램** 형태로 구현했습니다.

---

## 핵심 기능

- Python 기반 ADR 데이터 분석 자동화
- Pandas 기반 데이터 전처리 및 분석
- Line Listing / Summary Tabulation 보고서 생성
- Tkinter 기반 GUI 분석 프로그램
- PyInstaller 기반 실행파일 배포
- AWS RDS 기반 사용자 인증

---

## Python 중심 기술 스택

| Category | Technology |
|--------|-----------|
| Language | **Python** |
| Data Processing | **Pandas** |
| GUI | **Tkinter** |
| Packaging | **PyInstaller** |
| Database | MySQL |
| Cloud | AWS RDS |

---

## 프로젝트 구조

```
data/       테스트용 ADR 데이터
code/       Python 분석 로직
sub_code/   테스트 및 실험 코드
demo/       시연 영상
```

---

<details>
<summary>Python 기반 구현 상세</summary>

### Python 데이터 처리 파이프라인

ADR 원시 데이터를 Python으로 처리하여  
분석 가능한 데이터셋으로 변환합니다.

주요 처리

- 제품 코드 기반 데이터 필터링
- 기간 기반 데이터 분석
- Pandas 기반 데이터 전처리
- 보고서용 데이터 구조 생성

---

### ADR 보고서 생성

Python 스크립트를 통해 다음 보고서를 자동 생성합니다.

**Line Listing**

개별 부작용 사례 데이터 생성

**Summary Tabulation**

부작용 데이터를 집계하여 통계 형태로 제공

---

### Python GUI 프로그램

Tkinter를 활용하여 Python 기반 **데스크탑 분석 프로그램**을 구현했습니다.

기능

- 제품 코드 입력
- 분석 기간 설정
- Progress Bar
- 입력값 검증 및 오류 처리

---

### Python 실행파일 배포

Python 프로그램을 실행파일 형태로 배포했습니다.

사용 기술

- PyInstaller
- Virtual Environment

```
pyinstaller --name PV_ADR_Analyzer \
--onefile guiapp.py \
--noconsole
```

---

### Python 환경 최적화

초기 개발 환경

```
Anaconda 약 300MB
```

최적화 환경

```
Python virtualenv 약 30MB
```

→ 실행 환경 **약 90% 감소**

---

### 인증 시스템

Python 애플리케이션에서 AWS RDS(MySQL) 기반 로그인 시스템 구현

```
CREATE USER 'username'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON login.* TO 'username'@'%';
FLUSH PRIVILEGES;
```

</details>

---

## Team

- Eungchan Kang — Pharmacovigilance Team  
- Jisun Jang — IT Operations Team
