# Daewoong/PV-team project
develop tool for pharmacovigilance

# PV팀 의약품 부작용 원시자료 분석/처리 툴 구현

## **📢 Purpose**
  + PV팀 summarization Tool 개발
  + 1년, 1달 등 기간/횟수 제한하여 고객 제약사에 판매

## **👨‍👧‍👦 Members**
  + PV팀 권순길님
  + PV팀 강응찬님
  + IT운영팀 장지선님
  
<br>

## **👩‍💻 Tech**
+ Python
+ MySQL
+ AWS RDS

<br>

## **🗂 File explanation**
1. data : primitive data for testing
    + 제품코드 : 201701182
    + 시작일자 : 20170213
    + 종료일자 : 현재
2. code : main code for project
3. sub_code : testing code for main code
4. demo : 테스팅 및 시연 영상

<br>

## **✍ TASK**  
### [7월 Time Table]
+ ipynb -> py (linelisting)
+ github 연결
+ 고객사 파일 위치 인식하게끔 변경 (개발자로컬X)
+ startdate, enddate 설정
+ GUI 함수 class 제작
+ 대상품목 코드 연결 (openAPI)
+ exe 확인

+ **7/10 개발사항**
  + tkinter에서 불러올 수 있도록 주피터 파일 → py 파일 변환
  (analysis_def.py에 class 형식으로 함수 불러올 수 있도록 linelisting과 summary 함수 제작)
  + 파일 추가 시 해당 PC의 로컬 경로를 직접 받아 어떠한 PC든 해당 PC내에 있는 파일로 읽을 수 있도록 변경
  + line listing과 summary tabulation으로 종류를 나눠 다운받을 수 있도록 추가
  + 제품코드 입력 시 해당 제품코드의 파일 제작
  + 보고 시작 및 종료기한 설정
  + open API 내에서 drugname과 code 추출은 하였으나 자동으로 불러오는 것까지 연동은 아직 미진행 (아래 문의사항1 관련 이슈)


+ **7/13(화) 진행사항**
  + 프로그레스 바 생성
  + 코드암호화 → 암호화한 코드를 exe화
  → pyinstaller aes 사용하면 괜찮을지? (python2에서만 가능)
  → cython으로 변환한다음 dll로 pyinstaller 만들기 
  + 외부환경 테스트 진행 (맥 → 윈도우, 윈도우→ 맥, 윈도우→어나더윈도우)

+ **7/30(금) 진행사항**
  + python 용량문제 해결 (anaconda 아닌 cmd에서 직접 가상환경 제작하면 300MB → 30MB)
    + cmd 들어가는 법
    ```text
    cd 가상환경이름
    가상환경이름\Scripts\activate.bat
    ```
  + pyinstaller 제작
    ```
    pyinstaller --name PV_이상사례탐지 --onefile guiapp.py --paths anywhere --noconsole --icon=icon path
    ```
  + 로그인 DB 구현 (아래는 local 코드, 현재는 AWS로 변환)
    ```mysql
    # user 새로 생성 (%는 모든 host에 대하여 라는 뜻)
    create user '이름'@'%' identified by '비밀번호';

    # 모든 권한 제공 (모든 ip에 대해 허용)
    grant all privileges on login.* to 'outside'@'%';

    # user별 허용된 host 확인
    SELECT User,Host FROM mysql.user;

    # refresh
    flush privileges;
    ```
  + AWS RDS 제작 및 연결
    + RDS 제작 과정 : https://dashing-guarantee-065.notion.site/AWS-RDS-with-MySQL-Maria-DB-af96a475fc1249d98e0b5d7d23c62e25
  + 제품코드,시작일자,종료일자 누락되면 에러메세지 띄우기

### [8월 Time Table]


+ **8월3주차 진행필요사항**
  + PV현업에서 바로 사용 가능하도록 대분류 소분류 나눠서 저장하는 function apply 
  + 맥, window용 pyinstaller 제작 후 appendix tool 활용해서 한번 더 보안
    + server 및 웹 구현 시 관리자 부재로 install형식 선택
  + 프로그레스바 초단위로 변경해서 진행상황 수치화
  + AWS RDS에 MedDRA 파일 추가
    + 고객사에 제공하는 것보다 보안으로 유지하는 것이 더 유리
  + USER모드: 비밀번호를 관리자가 랜덤생성 후 USER에게 전달 (이메일주소 포함)


## **🛠 Issue Point**  
+ ex. 내용 (이슈일자 - 해결일자) 


<br>

## **📌Questions**
  1) 아래 파일 업로드 시 MedDRA dictionary의 경우, 타 사에서 활용 시 exe와 함께 파일이 제공/다운로드 되는지 혹은 제공이 불가한지?  
  → 제공 불가로 서버 진행 필요 (별도 서버 구축 해야하는지 이미 있는지 확인필요)  
  → 새로 api 받아오는 내용은 코드도 계속 변하고 누적관리 가능한지 확인필요 (drugcode가 계속 바뀌는 이슈)   
  2) summary tabulation은 나오는데 linelisting은 안나오는 경우가 있는지?  
  테스트를 위해 우루사 연질캡슐 197000040로 테스트 결과 summary tabulation은 잘 나오지만 line listing의 경우 빈 데이터 프레임이 나와 현재 에러가 발생  
  linelisting이 빈 프레임이면 해당 제품에 대한 보고가 없다고 안내  
  → 없는경우도 발생함 / 제품코드 잘못입력한경우, 제품이 없는경우 없다고 말해줘야할듯  
  3) 타 회사도 데이터를 저희와 똑같은 파일이름으로 받게되는지?  
  → 똑같음  
  4) 아래 파일은 코드에서 사용이 되지 않았는데 코드 진행 시 필요 없는 파일이 맞는지?  
  → 필요없음  
  5) 제품코드 자리수가 항상 똑같은지?  
  → 다름 제한없이 두는 것이 좋을듯 


+ **8/13(금) 부록테이블 생성 코드 porting**
  + code 실행 방법
    + data(line listing or summary tabulation)를 pandas로 불러오기
    + data type은 현재 excel로 지정
    + 테이블 생성을 위한 객체 생성 : test = Build_Table(data, 0)
    + 0은 summary tabulation. 1은 line listing. 즉 line listing작업을 하려면 Build_Table(data, 1)
    + test.start_appendix_table() 호출하면 결과값을 DataFrame으로 반환
    + 자세한 내용은 코드 메인 함수에 있음
 
## **테스팅 성공**
## **싱행파일 제작 사용**

