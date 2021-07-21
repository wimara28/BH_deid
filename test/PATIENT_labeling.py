# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:09:26 2021

@author: JY
"""


import re

p = "환자\s?이름\s?[:|;]\s?[가-힣]{2,}"
s1 = '환자이름 : 홍길동'
s2 = '환자 이름: 홍길동'
s3 = '환자이름:홍길동' # In this case, only 'PER-B'
s4 = '환자 이름 ;홍길동'

def convert_pname(matchObj):
	
	match = matchObj.group()	
	resultString = "'O'," * (len(match.split())-1) + "'PER-B'"
	
	return resultString

print(f"{s1} ====> {re.sub(p, convert_pname, s1)}")
print(f"{s2} ====> {re.sub(p, convert_pname, s2)}")
print(f"{s3} ====> {re.sub(p, convert_pname, s3)}")
print(f"{s4} ====> {re.sub(p, convert_pname, s4)}")
"""
output:
환자이름 : 홍길동 ====> 'O','O','PER-B'
환자 이름: 홍길동 ====> 'O','O','PER-B'
환자이름:홍길동 ====> 'PER-B'
환자 이름 ;홍길동 ====> 'O','O','PER-B'
"""

