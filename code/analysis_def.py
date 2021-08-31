import pandas as pd
import numpy as np
import time
import pymysql
import re
from datetime import datetime


# MedDRA
conn = pymysql.connect(host='db-2.cjfiturksrlr.ap-northeast-2.rds.amazonaws.com', user='yeschan', password='yeschan119',
                    db='PV_DB', charset='utf8')

curs = conn.cursor()
sql= 'SELECT * FROM MedDRA;'
MedDRA = pd.read_sql(sql, conn)
#MedDRA.drop('ID',axis=1,inplace=True)
MedDRA = MedDRA.fillna(0)
MedDRA['ARRN'] = MedDRA['ARRN'].astype(int)

# line listing & summary tabulation class - saving file

# line listing & summary tabulation class
class Build_Table:
    def __init__(self,data,choice):
        self.data = data
        self.SOC = {} # SOC column을 기준을 데이터를 처리
        self.result = {}
        self.choice = choice  # choose line listing or summary tabulation
        self.columns = ['기간계 용어/대표 용어']
    # data quality
    # nan value를 해당 값으로 채우기
    def isNaN(self,string):
        return string != string # is Nan or value?

    def do_DQ(self,i):
        try:
            soc = self.data.columns[i]  # 컬럼값을 표준으로 바꾸기.
            pt = self.data.columns[i+1] # i가 0이면 summary, 1이면 line listing
            self.data = self.data.rename(columns={soc:'SOC',pt:'PT'},errors='raise')
            # 출력을 위해 input data에서 column들을 가져오기
            # i + 2 == 3? line listing columns, 2? summary columns
            [self.columns.append(column) for column in self.data.columns[i+2:]]
            for i in range(len(self.data)):
                if self.isNaN(self.data['SOC'][i]):
                    self.data.at[i,'SOC'] = self.data['SOC'][i-1] # nan이전의 값으로 채우기
        except:
            print("Errors for do_DQ()")
    #SOC의 해당 row와 같은 행에 있는 데이터를 전부 추출 => PT:
    def map_contents(self,i):
        try:
            contents = []
            for row in self.data.loc[i]['PT':]:
                if '보고일자' in self.data.columns and row == self.data['보고일자'][i]:  # str형태의 보고일자를 date 형식으로
                    row = self.str_to_date(str(row))
                contents.append(row)
                # PT에서 한글만 추출하기 위해 regex 를 사용하여 한글만 추출하고 공백도 다 지우기
                # contents[0]은 PT에 해당하는 하나의 셀
            contents[0] = re.compile('[^ ㄱ-ㅣ가-힣]+').sub('',contents[0]).replace(' ','')
        except:
            print("Errors for get_contents({})".format(i))
        return contents

    # string to date
    def str_to_date(self,date_time_str):
        date_time_obj = datetime.strptime(date_time_str, '%Y%m%d')
        return str(date_time_obj.date()).replace('-','.')
    '''
    data preprocessing
    {soc {PT number [PT value, 안전관리번호, 보고일자, 보고국가...]}}
    ex : {각종 면역계 장애 : {0 : [과민성, 155812029, 대한민국...]}}
    '''
    def build_SOC_tree(self):
        for i in range(len(self.data)):
            soc_list = {}   # list to store {PT number {PT value, 안전관리번호, 보고일자, 보고국가...}}
            soc = self.data['SOC'][i]
            soc_hangul = re.compile('[^ ㄱ-ㅣ가-힣]+').sub('',soc).replace(' ','')
            if soc_hangul not in self.SOC:
                soc_list[1] = self.map_contents(i)
                self.SOC[soc_hangul] = soc_list
            else:
                last_key = int(list(self.SOC[soc_hangul].keys())[-1]) + 1
                #soc_list[last_key] = get_contents(i)
                self.SOC[soc_hangul][last_key] = self.map_contents(i)
                
    '''
    tree parsing and build sheet
    soc을 parsing하면서 각 컬럼별로 값을 채우기
    ex : 기관계용어에 해당하는 SOC와 대표용어에 해당하는 PT values을 tmp 리스트로 만들고
    result dic에 key : 기관계용어, value : tmp
    다른 컬럼값들도 똑같이 채우기.
    '''
    def build_Appendix_table(self):
        try:
            for c, i in zip(self.columns, range(len(self.columns))):
                tmp = []
                for sub_soc in self.SOC.keys():
                    if i == 0:
                        tmp.append(sub_soc)  #기관계 용어
                    else:
                        tmp.append('')   # 기관계용어와 대표용어를 구별하기 위해
                    for key in self.SOC[sub_soc].keys():
                        tmp.append(self.SOC[sub_soc][key][i])
                self.result[c] = tmp
        except:
            print('Errors for build_Appendix_table()')
        return self.result
    
    def start_appendix_table(self):
        self.do_DQ(self.choice)
        self.build_SOC_tree()
        self.result = self.build_Appendix_table()
        export_file = pd.DataFrame(self.result)
        return export_file
    
class analysis:
    def __init__(self, files, folder, startdate, enddate, drug_cd):
        self.files = files
        self.folder = folder
        self.startdate = startdate
        self.enddate = enddate
        self.drug_cd = drug_cd

    # def codechange(self):
    #     drug_cd = self.drug_cd
    #     # 향후 제품 코드 -> 이름 변환하는 파일 받으면 변경예정
    #     drugname = "몬테락정"
    #     # 제품 코드에서 이름 반환
    #     return drugname

    def linelisting(self):

        # 향후 확인 시 주석 풀 것
        # def codechange(drug_cd):
        #     drug_cd = drug_cd

        #     # 향후 제품 코드 -> 이름 변환하는 파일 받으면 변경예정
        #     drugname = "몬테락정"

        #     # 제품 코드에서 이름 반환
        #     return drugname

        ###########################################
        # 1. 자료 불러오기
        ## 원시자료 및 MeDRA
        ###########################################
        files = self.files
        folder = self.folder
        startdate = self.startdate
        enddate = self.enddate
        drug_cd = self.drug_cd
        # drug_name = codechange(drug_cd)

        for i in files:
            if 'GROUP.txt' in i:
                folder1 = i
            elif 'ADR_INFO_REPORT.txt' in i:
                folder2 = i
            elif 'ADR_REPORT_BASIC.txt' in i:
                folder3 = i
            elif 'ASSESSMENT_ADR.txt' in i:
                folder4 = i
            elif 'DRUG_INFO_ADR.txt' in i:
                folder5 = i
            # elif 'MedDRA 영문_한글화.xlsx' in i:
            #     folder6 = i
        
        GROUP = pd.read_csv(folder1, sep='|', encoding="cp949")
        ADR_INFO_REPORT = pd.read_csv(folder2, sep='|', encoding="cp949")
        ADR_REPORT_BASIC = pd.read_csv(folder3, sep='|', encoding="cp949")
        ASSESSMENT_ADR = pd.read_csv(folder4, sep='|', encoding="cp949")
        DRUG_INFO_ADR = pd.read_csv(folder5, sep='|', encoding="cp949")

        # MedDRA = pd.read_excel(folder6)
        global MedDRA
        
        ###########################################
        # 2. 전처리
        # 2.1 DRUG_INFO_ADR 파일에 대한 전처리
        ###########################################

        df_drug = DRUG_INFO_ADR
        # 품목갱신 의약품으로 보고된 총 이상사례 중 의심의약품으로 보고 된 이상사례
        df_drug = df_drug[(df_drug['DOUBT_CMBT_CSF']==1) & (df_drug['DRUG_CD']==drug_cd)]
        df_drug = df_drug.loc[:,['KD_NO','DRUG_CD','DRUG_CHEM','DSAS_CD','DOSE_STR_DT','DOSE_END_DT']]
        df_drug = df_drug.rename({'KD_NO':'안전관리번호', 'DRUG_CD':'제품코드', 'DRUG_CHEM':'의약품명', 'DSAS_CD':'적응증',
                                'DOSE_STR_DT':'투여시작일', 'DOSE_END_DT': '투여종료일'}, axis = 'columns')

        # 적응증, 투여시작일, 투여종료일 컬럼값에 대한 결측치 처리
        df_drug = df_drug.fillna(0)

        # 제품코드, 투여시작일, 투여종료일 컬럼값에 대한 정수로 변환
        df_drug['제품코드'] = np.array(df_drug['제품코드'], dtype=np.int64)
        df_drug['투여시작일'] = np.array(df_drug['투여시작일'], dtype=np.int64)
        df_drug['투여종료일'] = np.array(df_drug['투여종료일'], dtype=np.int64)


        ###########################################
        # 2.2 GROUP 파일에 대한 전처리
        ###########################################

        aa = GROUP
        aa = aa.fillna(0)
        aa['GROUP'] = np.array(aa['GROUP'], dtype=np.int64)
        aa['KD_NO'] = np.array(aa['KD_NO'], dtype=np.int64)
        aa['SEQ'] = np.array(aa['SEQ'], dtype=np.int64)
        aa['TRC_RPT_RSN_CD'] = np.array(aa['TRC_RPT_RSN_CD'], dtype=np.int64)

        # 추적 번호가 "0"이면 최초 보고 건만 있고, 추적 번호가 "0"이 아니면 추적 보고 건 존재

        def GROUP(x, y):
            if y == 0:
                return x
            else: return y

        aa["GROUP1"] = aa.apply(lambda x: GROUP(x["KD_NO"], x["GROUP"]), axis=1)
        aa = aa.loc[:,['KD_NO','GROUP1','SEQ','TRC_RPT_RSN_CD']]
        aa = aa.rename({'KD_NO':'안전관리번호','GROUP1':'최초보고번호','SEQ':'추적번호','TRC_RPT_RSN_CD':'추적보고사유'}, axis = 'columns')

        # 보고 무효화 된 이상사례 건 삭제

        grouped1 = aa.groupby("최초보고번호").agg({'추적보고사유':'max'})

        aa1 = pd.merge(aa, grouped1, left_on=['최초보고번호'], right_on=['최초보고번호'], how='left')

        aa1 = aa1.rename({'추적보고사유_x':'추적보고사유','추적보고사유_y':'보고무효화'}, axis = 'columns')

        null = aa1[aa1["추적보고사유"]==4].index
        aa2 = aa1.loc[null]
        aa2

        aa3 = aa2.groupby(["최초보고번호","추적보고사유"]).agg({'추적번호':'max'})

        aa4 = pd.merge(aa1, aa3, left_on=["최초보고번호"], right_on=["최초보고번호"], how='left')

        aa4 = aa4.fillna(0)

        aa4 = aa4.rename({'추적번호_x':'추적번호','추적번호_y':'보고무효화최신추적번호'}, axis = 'columns')

        aa4["보고무효화최신추적번호"] = np.array(aa4["보고무효화최신추적번호"], dtype=np.int64)


        def delete(x,y,z):
            if x == 4:
                if y > z:
                    return 0
                else: return 1
            else: return 0
            

        aa4["제거"] = aa4.apply(lambda x: delete(x["보고무효화"], x["추적번호"], x["보고무효화최신추적번호"]), axis=1)
        null2 = aa4[aa4["제거"]==1].index
        aa4 = aa4.drop(null2)
        aa4 = aa4.loc[:,['안전관리번호','최초보고번호','추적번호','추적보고사유']]

        # 최신의 이상사례 보고 건만 남김

        aa5 = aa4.groupby(["최초보고번호"]).agg({'추적번호':'max'})
        aa6 = pd.merge(aa4, aa5, left_on=['최초보고번호'], right_on=['최초보고번호'], how='left')
        aa6 = aa6.rename({'추적번호_x':'추적번호','추적번호_y':'최종추적번호'}, axis = 'columns')
        null2 = aa6[aa6["추적번호"]<aa6["최종추적번호"]].index
        aa6 = aa6.drop(null2)
        aa6 = aa6.loc[:,['안전관리번호','최초보고번호','추적번호','추적보고사유','최종추적번호']]

        ###########################################
        # 2.3 ADR_INFO_BASIC 파일에 대한 전처리
        ###########################################

        df_BASIC = ADR_REPORT_BASIC
        df_BASIC = df_BASIC.loc[:,['KD_NO','RPT_DL_DT','CRTCL_CASE_YN','RPT_CSF','PTNT_SEX','PTNT_OCCR_THTM_AGE','AGE_UNIT',
                                'PTNT_AGEGP']]
        df_BASIC = df_BASIC.rename({'KD_NO':'안전관리번호','RPT_DL_DT':'보고일자','CRTCL_CASE_YN':'중대한이상사례여부',
                                    'RPT_CSF':'보고원', 'PTNT_SEX': '성별', 'PTNT_OCCR_THTM_AGE': '연령', 'AGE_UNIT': '연령단위',
                                    'PTNT_AGEGP': '연령군'}, axis = 'columns')
        df_BASIC = df_BASIC.fillna(0)
        df_BASIC["성별"] = df_BASIC["성별"].astype(int)
        df_BASIC["연령단위"] = df_BASIC["연령단위"].astype(int)
        df_BASIC["연령"] = df_BASIC["연령"].astype(int)
        df_BASIC["연령군"] = df_BASIC["연령군"].astype(int)

        # 성별 구분 함수
        def sex(x):
            if x==1:
                return "남자"
            elif x==2:
                return "여자"
            else:
                return "모름"

        # 보고원 구분 함수
        def source(x):
            if x == 1 or x==3 or x==4 or x==5:
                return "자발보고"
            elif x==2:
                return "조사연구"
            else:
                return "모름"

        # 이상사례 중대성 여부 판단 함수
        def SAE(x):
            if x == "Y":
                return "중대함"
            else:
                return "중대하지 않음"

        # 연령군 구분 함수
        def ageunit(x,y,z):
            if z == 1:
                return "신생아"
            elif z == 2:
                return "영아"
            elif z == 3:
                return "어린이"
            elif z == 4:
                return "청소년"
            elif z == 5:
                return "성인"
            elif z == 6:
                return "고령자"
            
            # 연령군이 결측치인 경우
            elif z==0:
                
                # 연령단위가 "세"인 경우
                if x == 4:
                    if y >= 65:
                        return "고령자"
                    elif 19 <= y < 65:
                        return "성인"
                    elif 12 <= y < 19:
                        return "청소년"
                    elif 2 <= y < 12:
                        return "어린이"
                    elif 1 == y:
                        return "영아"
                    elif 0 == y:
                        return "모름"
                    
                # 연령단위가 "개월"인 경우
                elif x==3:
                    if y >= 780:
                        return "고령자"
                    elif 228 <= y < 780:
                        return "성인"
                    elif 144 <= y < 228:
                        return "청소년"
                    elif 24 <= y < 144:
                        return "어린이"
                    elif 1 <= y < 24:
                        return "영아"
                    elif 0 <= y < 1:
                        return "신생아"
                    
                # 연령단위가 "주"인 경우
                elif x==2:
                    if y >= 3380:
                        return "고령자"
                    elif 988 <= y < 3380:
                        return "성인"
                    elif 624 <= y <988:
                        return "청소년"
                    elif 52 <= y < 624:
                        return "어린이"
                    elif 4 <= y < 52:
                        return "영아"
                    elif 0 <= y < 4:
                        return "신생아"
                    
                # 연령단위가 "일"인 경우
                elif x==1:
                    if y >= 23725:
                        return "고령자"
                    elif 6935 <= y < 23735:
                        return "성인"
                    elif 4380 <= y < 6935:
                        return "청소년"
                    elif 730 <= y < 4380:
                        return "어린이"
                    elif 28 <= y < 730:
                        return "영아"
                    elif 0 <= y < 28:
                        return "신생아"
                    
                else: return "모름"
            else: return "모름"

        # 연령단위를 문자열로 구분한 함수
        def age(x):
            if x == 4:
                return "세"
            elif x==3:
                return "개월"
            elif x==2:
                return "주"
            elif x==1:
                return "일"
            else: return "모름"

        # 연령단위를 모르는 경우, 연령은 "모름"으로 표시
        # x = 연령단위, y = 연령1
        def ageunknown(x,y):
            if x == "모름":
                return "모름"
            else: return y

        df_BASIC["성별"] = df_BASIC["성별"].apply(sex)
        df_BASIC["보고원"] = df_BASIC["보고원"].apply(source)
        df_BASIC["중대한이상사례여부"] = df_BASIC["중대한이상사례여부"].apply(SAE)
        df_BASIC["연령군"] = df_BASIC.apply(lambda x: ageunit(x["연령단위"], x["연령"], x["연령군"]), axis=1)
        df_BASIC["연령단위"] =df_BASIC["연령단위"].apply(age)
        df_BASIC["연령"] = df_BASIC["연령"].astype(str)

        df_BASIC["연령1"] = df_BASIC["연령"] + df_BASIC["연령단위"]

        df_BASIC["연령1"] = df_BASIC.apply(lambda x: ageunknown(x["연령단위"], x["연령1"]), axis=1)

        df_BASIC["연령/성별"] = df_BASIC["연령1"] + "/" + df_BASIC["성별"]

        df_BASIC = df_BASIC.loc[:,['안전관리번호','보고일자','중대한이상사례여부','보고원','연령/성별','연령군']]


        # 보고서 보고기간동안 보고된 보고서만 남기기
        reporting_date = df_BASIC[(df_BASIC['보고일자'] >= startdate)
                                & (df_BASIC['보고일자'] <= enddate)].index

        df_BASIC = df_BASIC.loc[reporting_date]


        ###########################################
        # 2.4 ADR_INFO_REPORT 전처리
        ###########################################

        df_REPORT = ADR_INFO_REPORT
        df_REPORT = df_REPORT.loc[:,['KD_NO','WHOART_ARRN','WHOART_SEQ','rvln_dt','CASE_RND_CD']]
        df_REPORT = df_REPORT.rename({'KD_NO':'안전관리번호','rvln_dt':'이상사례발현일',
                                    'CASE_RND_CD':'이상사례결과'}, axis = 'columns')

        #이상사례 결과에 대한 결측치 0으로 변환
        df_REPORT = df_REPORT.fillna(0)

        # 이상사례 발현일, 이상사례 결과에 대한 변수값 정수로 변환
        df_REPORT["이상사례발현일"] = df_REPORT["이상사례발현일"].astype(int)
        df_REPORT["이상사례결과"] = df_REPORT["이상사례결과"].astype(int)
        

        # 이상사례 결과 구분 함수
        def outcome(x):
            if x==1:
                return "회복"
            elif x==3:
                return "회복되지 않음"
            elif x==5:
                return "후유증을 동반한 회복"
            elif x==7:
                return "치명적 손상"
            elif x==9:
                return "모름"
            elif x==10:
                return "사망"
            elif x==11:
                return "사망"
            else: return "모름"

        df_REPORT["이상사례결과"] = df_REPORT["이상사례결과"].apply(outcome)


        ###########################################
        ## 2.5 ASSESSMENT_ADR 전처리
        ###########################################

        # 부작용보고원시자료마다 대문자 또는 소문자로 받을 때가 있어서, 소문자로 통일시킴.

        ASSESSMENT_ADR = ASSESSMENT_ADR.rename({'CERTAIN':'certain', 'PROBABLE':'probable',
                                            'POSSIBLE':'possible', 'UNLIKELY':'unlikely',
                                            'UNCLASSIFIED':'unclassified', 'UNASSESSABLE':'unassessable',
                                            'NOT_APPLICABLE':'not_applicable'}, axis = 'columns')

        df_ASSESSMENT = ASSESSMENT_ADR

        #인과성 평가 항목에 대한 값들의 결측치 처리 및 정수변환
        df_ASSESSMENT = df_ASSESSMENT.fillna(0)
        df_ASSESSMENT['certain'] = df_ASSESSMENT['certain'].astype(int)
        df_ASSESSMENT['probable'] = df_ASSESSMENT['probable'].astype(int)
        df_ASSESSMENT['possible'] = df_ASSESSMENT['possible'].astype(int)
        df_ASSESSMENT['unlikely'] = df_ASSESSMENT['unlikely'].astype(int)
        df_ASSESSMENT['unclassified'] = df_ASSESSMENT['unclassified'].astype(int)
        df_ASSESSMENT['unassessable'] = df_ASSESSMENT['unassessable'].astype(int)
        df_ASSESSMENT['not_applicable'] = df_ASSESSMENT['not_applicable'].astype(int)

        # 인과성 평가 구분 함수
        def causality(a, b, c, d, e, f, g):
            if a == 1:
                return "확실함"
            elif b == 1:
                return "상당히 확실함"
            elif c == 1:
                return "가능함"
            elif d == 1:
                return "가능성 적음"
            elif e == 1:
                return "판정곤란"
            elif f == 1:
                return "판정불가"
            elif g == 1:
                return "해당 없음"
            else: return "모름"

        df_ASSESSMENT["인과성평가"] = df_ASSESSMENT.apply(lambda x: causality(x["certain"], x["probable"], x["possible"],
                                                                        x["unlikely"], x["unclassified"], x["unassessable"],
                                                                        x["not_applicable"]), axis=1)

        df_ASSESSMENT = df_ASSESSMENT.loc[:,['KD_NO','DRUG_CD','DRUG_CHEM','WHOART_ARRN','WHOART_SEQ','인과성평가']]

        df_ASSESSMENT = df_ASSESSMENT.rename({'KD_NO':'안전관리번호','DRUG_CD':'제품코드','DRUG_CHEM':'의약품명'}, axis = 'columns')

        #다른 테이블과 연결시키기 위해, 제품코드 정수로 변환
        df_ASSESSMENT['제품코드'] = df_ASSESSMENT['제품코드'].astype(int)


        ###########################################
        # 3. Data-Table merge
        ###########################################

        # 최종으로 남겨진 보고서에서 의약품정보 테이블 붙이기

        merge1 = pd.merge(df_drug, aa6, on = '안전관리번호', how='inner')

        # merge1 테이블 결측치 처리 및 투여시작일, 투여종료일 정수 변경

        merge1 = merge1.fillna(0)
        merge1['투여시작일'] = merge1['투여시작일'].astype(int)
        merge1['투여종료일'] = merge1['투여종료일'].astype(int)

        # 투여 시작일 및 종료일의 값이 결측치인 경우, 모름으로 표시
        def drugstart(x):
            if x == 0:
                return "모름"
            else:
                return x

        def drugend(x):
            if x == 0:
                return "모름"
            else:
                return x
            

        merge1['투여시작일'] = merge1['투여시작일'].apply(drugstart)
        merge1['투여종료일'] = merge1['투여종료일'].apply(drugend)

        # 완성된 테이블에 보고서 기본정보 테이블 붙이기
        merge2 = pd.merge(merge1, df_BASIC, on = '안전관리번호', how='inner')

        # 완성된 테이블에 이상사례 정보 관련 테이블 붙이기
        merge3 = pd.merge(merge2, df_REPORT, on = '안전관리번호', how='left')

        # 완성된 테이블에 인과성평가 테이블 붙이기
        merge4 = pd.merge(merge3, df_ASSESSMENT, left_on =['안전관리번호', '제품코드', 'WHOART_ARRN', 'WHOART_SEQ'],
                    right_on =['안전관리번호', '제품코드', 'WHOART_ARRN', 'WHOART_SEQ'], how='left')

        #완성된 테이블에 MedDRA table 붙이기
        merge5 = pd.merge(merge4, MedDRA, left_on=['WHOART_ARRN','WHOART_SEQ'], right_on=['ARRN','SEQ'], how='left')

        # 만약 merge5에 해당 테이블이 없는 경우 0반환
        if merge5.shape[0]==0:
            return 0

        # Line-lsiting 테이블에 필요한 변수만을 남김
        merge5 = merge5.drop(["제품코드", "적응증", "최초보고번호", "추적번호", "의약품명_y", "WHOART_ARRN", "WHOART_SEQ", "의약품명_y",
                        "ARRN", "SEQ"], axis=1)

        # Merge5 테이블 정리

        # 제공받는 원시자료가 국내에서 발생한 이상사례만을 수집한 자료이기 때문에, 보고국가는 대한민국으로 작성
        # print(merge5)
        merge5.loc[:,'보고국가'] = '대한민국'

        # 필요한 변수로 table 재배열
        merge5 = merge5[['의약품명_x','SOC','PT',
                '안전관리번호','보고국가','보고일자','보고원','연령/성별','연령군',
                '투여시작일','투여종료일',
                '이상사례발현일','중대한이상사례여부','이상사례결과','인과성평가']]

        # 규제기관 보고 작성 관련 표준화된 용어로 각각의 변수 변경
        merge5 = merge5.rename({'의약품명_x':'의약품명','SOC':'기관계 대분류(SOC)', 'PT':'대표 용어(PT)',
                        '이상사례 결과1':'이상사례결과'}, axis = 'columns')

        # SOC 및 PT의 알파벳 순으로 line-listing 재배열
        merge5 = merge5.sort_values(by=['기관계 대분류(SOC)','대표 용어(PT)'], ascending = True)

        # Line-listing 테이블로 출력
        # 약품 이름 code to name
        # drug_name = codechange(drug_cd)

        # file_name ppt 기반으로 변경 (기존 사용자가 설정한 폴더/제품이름_linelisting.xlsx)
        # file_name = folder+"/"+str(drug_name)+'_'+str(drug_cd)+"_Linelisting.xlsx"
        file_name = folder+"/"+str(drug_cd)+"_Linelisting.xlsx"
        
        line_listing = Build_Table(merge5, 1) # summary tabulation일 경우 0 전달
        result = line_listing.start_appendix_table()
        result.to_excel(file_name, encoding='euc-kr',index=False)
        
        # 함수가 성공적으로 실행되어 저장까지 완료한 경우 1반환
        return 1

################################
####  SUMMARY TABULATION    ####
################################

    def summary(self):
        # def codechange(drug_cd):
        #     drug_cd = drug_cd
        #     # 향후 제품 코드 -> 이름 변환하는 파일 받으면 변경예정
        #     drugname = "몬테락정"
        #     # 제품 코드에서 이름 반환
        #     return drugname

        ###########################################
        # 1. 자료 불러오기
        ## 원시자료 및 MeDRA
        ###########################################
        files = self.files
        folder = self.folder
        startdate = self.startdate
        enddate = self.enddate
        drug_cd = self.drug_cd
        # drug_name = codechange(drug_cd)

        for i in files:
            if 'GROUP.txt' in i:
                folder1 = i
            elif 'ADR_INFO_REPORT.txt' in i:
                folder2 = i
            elif 'ADR_REPORT_BASIC.txt' in i:
                folder3 = i
            elif 'ASSESSMENT_ADR.txt' in i:
                folder4 = i
            elif 'DRUG_INFO_ADR.txt' in i:
                folder5 = i
            elif 'MedDRA 영문_한글화.xlsx' in i:
                folder6 = i
        
        GROUP = pd.read_csv(folder1, sep='|', encoding="cp949")
        ADR_INFO_REPORT = pd.read_csv(folder2, sep='|', encoding="cp949")
        ADR_REPORT_BASIC = pd.read_csv(folder3, sep='|', encoding="cp949")
        ASSESSMENT_ADR = pd.read_csv(folder4, sep='|', encoding="cp949")
        DRUG_INFO_ADR = pd.read_csv(folder5, sep='|', encoding="cp949")

        global MedDRA
        # MedDRA = pd.read_excel(folder6)
        # MedDRA = MedDRA.fillna(0)
        # MedDRA['ARRN'] = MedDRA['ARRN'].astype(int)

        ###########################################
        # 2. 전처리
        ## 변수명 정리
        ###########################################
        # ADR_INFO = ADR_INFO_REPORT
        ADR_REPORT = ADR_REPORT_BASIC
        DRUG_INFO = DRUG_INFO_ADR
        ASSESSMENT= ASSESSMENT_ADR

        # 품목갱신 의약품으로 보고된 총 이상사례 중 의심의약품으로 보고 된 이상사례
        suspectindex = DRUG_INFO[DRUG_INFO["DOUBT_CMBT_CSF"]==1].index
        DRUG_suspect = DRUG_INFO.loc[suspectindex]

        # 제품코드 컬럼값에 대한 결측치 처리 및 정수 전환
        DRUG_suspect = DRUG_suspect.fillna(0)
        DRUG_suspect["DRUG_CD"] = DRUG_suspect["DRUG_CD"].astype(int)
        DRUG_suspect = DRUG_suspect.loc[:,['KD_NO','DRUG_CD','DRUG_CHEM']]
        
        # 품목갱신 의심 제품코드만 sorting
        DRUG_suspect = DRUG_suspect[(DRUG_suspect['DRUG_CD'] == drug_cd)]
        DRUG_suspect['KD_NO'] = np.array(DRUG_suspect['KD_NO'], dtype=np.int64)
        DRUG_suspect['DRUG_CD'] = np.array(DRUG_suspect['DRUG_CD'], dtype=np.int64)

        ###########################################
        # 2.1 GROUP 파일에 대한 전처리
        ###########################################
        GROUP = GROUP.fillna(0)
        GROUP['GROUP'] = np.array(GROUP['GROUP'], dtype=np.int64)
        GROUP['KD_NO'] = np.array(GROUP['KD_NO'], dtype=np.int64)
        GROUP['SEQ'] = np.array(GROUP['SEQ'], dtype=np.int64)
        GROUP['TRC_RPT_RSN_CD'] = np.array(GROUP['TRC_RPT_RSN_CD'], dtype=np.int64)

        def var(x, y):
            if y == 0:
                return x
            else: return y

        GROUP["GROUP1"] = GROUP.apply(lambda x: var(x["KD_NO"], x["GROUP"]), axis=1)

        GROUP_max = GROUP.groupby(['GROUP1']).agg({'SEQ':'max'})

        GROUP_merge = pd.merge(GROUP, GROUP_max, left_on =["GROUP1"], right_on=["GROUP1"], how="left")
        GROUP_merge = GROUP_merge.loc[:,["KD_NO","GROUP1","SEQ_x","TRC_RPT_RSN_CD", "SEQ_y"]]
        GROUP_merge = GROUP_merge.rename({'KD_NO':'안전관리번호', 'GROUP':'최초보고번호','SEQ_x':'추적번호', 'TRC_RPT_RSN_CD':'추적보고사유',
                        'SEQ_y':'최종추적번호'}, axis = 'columns')

        final = GROUP_merge[GROUP_merge["추적번호"]==GROUP_merge["최종추적번호"]].index
        GROUP_final = GROUP_merge.loc[final]

        ###########################################
        ## 2.2 ADR_REPORT 파일에 대한 전처리
        ###########################################
        # 보고일자 구분
        reporting_date = ADR_REPORT[(ADR_REPORT['RPT_DL_DT'] >= startdate)
                                & (ADR_REPORT['RPT_DL_DT'] <= enddate)].index

        ADR_REPORT = ADR_REPORT.loc[reporting_date]

        def SAE(x):
            if x == "Y":
                return 1
            else: return 0

        ADR_REPORT["CRTCL_CASE_YN"] = ADR_REPORT["CRTCL_CASE_YN"].apply(SAE)

        ADR_class = ADR_REPORT.loc[:,['KD_NO','CRTCL_CASE_YN','RPT_CSF']]

        def source(x):
            if x == 2:
                return 2
            else: return 1

        ADR_class["RPT_CSF"] = ADR_class["RPT_CSF"].apply(source)

        sourceindex = ADR_class[ADR_class["RPT_CSF"]== 0].index
        ADR_class = ADR_class.drop(sourceindex, axis=0)

        PBRER_info = pd.merge(GROUP_final, DRUG_suspect, left_on =['안전관리번호'], right_on=['KD_NO'], how='inner')
        PBRER_info = PBRER_info.loc[:,['KD_NO','DRUG_CD','DRUG_CHEM']]

        PBRER_class = pd.merge(PBRER_info, ADR_class, left_on=['KD_NO'], right_on=['KD_NO'], how='inner')

        PBRER_assess = pd.merge(PBRER_class, ASSESSMENT, left_on =['KD_NO', 'DRUG_CD'], right_on=['KD_NO', 'DRUG_CD'], how='left')
        PBRER_assess = PBRER_assess.loc[:,['WHOART_ARRN','WHOART_SEQ','KD_NO','DRUG_CD','DRUG_CHEM_x','CRTCL_CASE_YN','RPT_CSF']]


        def count_non_spo(x,y):
            if x == 0:
                if y==1:
                    return 1
                else: return 0
            else: return 0

        def count_serious_spo(x,y):
            if x == 1:
                if y==1:
                    return 1
                else: return 0
            else: return 0
            
        def count_non_PMS(x,y):
            if x == 0:
                if y==2:
                    return 1
                else: return 0
            else: return 0

        def count_serious_PMS(x,y):
            if x == 1:
                if y==2:
                    return 1
                else: return 0
            else: return 0
        
        # 만약 PBRER_assess 해당 테이블이 없는 경우 0반환
        if PBRER_assess.shape[0]==0:
            return 0

        PBRER_assess["자발보고_중대하지않음"] = PBRER_assess.apply(lambda x: count_non_spo(x["CRTCL_CASE_YN"], x["RPT_CSF"]), axis=1)
        PBRER_assess["자발보고_중대함"] = PBRER_assess.apply(lambda x: count_serious_spo(x["CRTCL_CASE_YN"], x["RPT_CSF"]), axis=1)
        PBRER_assess["조사연구_중대하지않음"] = PBRER_assess.apply(lambda x: count_non_PMS(x["CRTCL_CASE_YN"], x["RPT_CSF"]), axis=1)
        PBRER_assess["조사연구_중대함"] = PBRER_assess.apply(lambda x: count_serious_PMS(x["CRTCL_CASE_YN"], x["RPT_CSF"]), axis=1)

        PBRER_col = PBRER_assess.loc[:,["KD_NO","WHOART_ARRN","WHOART_SEQ","자발보고_중대하지않음","자발보고_중대함","조사연구_중대하지않음","조사연구_중대함"]]
        PBRER_col1 = PBRER_col.groupby(["WHOART_ARRN","WHOART_SEQ"]).agg({"자발보고_중대하지않음":"sum"})
        PBRER_col2 = PBRER_col.groupby(["WHOART_ARRN","WHOART_SEQ"]).agg({"자발보고_중대함":"sum"})
        PBRER_col3 = PBRER_col.groupby(["WHOART_ARRN","WHOART_SEQ"]).agg({"조사연구_중대하지않음":"sum"})
        PBRER_col4 = PBRER_col.groupby(["WHOART_ARRN","WHOART_SEQ"]).agg({"조사연구_중대함":"sum"})
        PBRER_col5 = pd.merge(PBRER_col1, PBRER_col2, left_on=["WHOART_ARRN","WHOART_SEQ"], right_on=["WHOART_ARRN","WHOART_SEQ"], how="left")
        PBRER_col6 = pd.merge(PBRER_col5, PBRER_col3, left_on=["WHOART_ARRN","WHOART_SEQ"], right_on=["WHOART_ARRN","WHOART_SEQ"], how="left")
        PBRER_final = pd.merge(PBRER_col6, PBRER_col4, left_on=["WHOART_ARRN","WHOART_SEQ"], right_on=["WHOART_ARRN","WHOART_SEQ"], how="left")

        PBRER_final["자발보고_총합"] = PBRER_final["자발보고_중대하지않음"] + PBRER_final["자발보고_중대함"]
        PBRER_final["조사연구_총합"] = PBRER_final["조사연구_중대하지않음"] + PBRER_final["조사연구_중대함"]
        PBRER_final = PBRER_final.loc[:,["자발보고_중대하지않음","자발보고_중대함","자발보고_총합","조사연구_중대하지않음",
                        "조사연구_중대함","조사연구_총합"]]

        mm = MedDRA
        mm['ARRN'] = np.array(mm['ARRN'], dtype=np.int64)

        PBRER = pd.merge(PBRER_final, mm, left_on=["WHOART_ARRN","WHOART_SEQ"], right_on=["ARRN","SEQ"], how='left')
        PBRER = PBRER.loc[:,["SOC","PT","자발보고_중대하지않음","자발보고_중대함","자발보고_총합","조사연구_중대하지않음",
                        "조사연구_중대함","조사연구_총합"]]
        PBRER = PBRER.rename({'SOC':'기관계 대분류(System Organ Class)','PT':'대표 용어(Preferred Term)'}, axis = 'columns')
        PBRER = PBRER.sort_values(by=['기관계 대분류(System Organ Class)','자발보고_총합', '조사연구_총합'], ascending = [True,False,False])
        PBRER = PBRER.groupby(["기관계 대분류(System Organ Class)","대표 용어(Preferred Term)"]).sum()
        
        # 만약 PBRER에 해당 테이블이 없는 경우 0반환
        if PBRER.shape[0]==0:
            return 0

        ###########################################
        # 3. Summary form 테이블로 출력
        ###########################################
        # file_name = folder+"/"+str(drug_name)+'_'+str(drug_cd)+"_Summarytabulation.xlsx"
        file_name = folder+"/"+str(drug_cd)+"_Summarytabulation.xlsx"
        PBRER.to_excel(file_name)
        
        PBRER = pd.read_excel(file_name)
        summary = Build_Table(PBRER, 0) # summary tabulation일 경우 0 전달
        result = summary.start_appendix_table()
        result.to_excel(file_name, encoding='euc-kr',index=False)
        # 함수가 잘 실행되어 저장까지 완료된 경우 1반환
        return 1

if __name__ == '__main__':
    ###########################################
    # TEST용도
    ###########################################
    starttime = time.time()
    # 제 workspace여서 테스트 시에는 경로를 바꿔서 실행하셔야 합니다 (아래 코드는 단순히 함수가 잘 돌아가는지 확인용)
    # 자료분석GUI.py로 실행시킬 경우 파일을 해당 PC의 경로에서 불러오므로 따로 설정하실 필요는 없습니다.
    files = ('data/need/ADR_INFO_REPORT.txt',
    'data/need/ADR_REPORT_BASIC.txt',
    'data/need/ASSESSMENT_ADR.txt',
    'data/need/DRUG_INFO_ADR.txt',
    'data/need/GROUP.txt')
    # 'data/need/MedDRA 영문_한글화.xlsx

    folder = 'data/need'
    startdate = 20170101 # 시작일자
    enddate = 20210424 # 종료일자
    drug_cd = 200810868 # 이상의약품
    drug_cd = 197000040

    lt = analysis(files, folder,startdate,enddate,drug_cd)

    # linelisting 만들기
    lt.linelisting()
    # summarytabulation 만들기
    lt.summary()
    endtime = time.time()
    print("WorkingTime: {} sec".format(endtime-starttime))
