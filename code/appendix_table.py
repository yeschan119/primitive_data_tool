#!/usr/bin/env python
# coding: utf-8

# In[24]:


# 담당자 : 강응찬
# Email : yeschan119@gmail.com
# 회사 : 대웅제약 PV팀
# 날짜 : 2021.07.13

import pandas as pd
import re
# 화면 늘리기
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))

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
        try:
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
        except:
            print("Error for build_SOC_tree")

                
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
        
'''
excel파일을 불러와서 dataframe으로 변환
Build_Table 클래스를 호출
클래스를 호출할 때 해당 데이터와 정수를 파라미터로 전달
정수는 : 해당 데이터가 line listing이면 1, summary tabulation이면 0
start_appendix_table()을 실행시키면 파일을 처리하고 dataframe type으로 리턴
리턴받은 파일을 excel파일로 내보내기
'''
if __name__ == '__main__':
    line_listing = pd.read_excel('test/임팩타민정_200709544_1.xlsx')
    summary_tabulation = pd.read_excel('test/임팩타민정_200709544.xlsx')
    Test = Build_Table(line_listing, 1)  # line listing일 경우 1 전달
    #Test = Build_Table(summary_tabulation, 0) # summary tabulation일 경우 0 전달
    result = Test.start_appendix_table()
    result.to_excel('test.xlsx', encoding='euc-kr',index=False)


# In[21]:


data = pd.DataFrame()
print(type(data))


# In[ ]:




