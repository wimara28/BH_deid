# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:40:50 2021

@author: JY
"""

import pandas as pd
import copy
import os
import re

"""
filename
NAME OF PHI
Column name of note_id
Column name of note_text
PATH to PHI regex folder
"""

dat = pd.read_csv({filename}, encoding='utf-8')

phis = {}
phis_none = {}

for i in range(len(dat)):
    if pd.isnull(dat[{NAME OF PHI}][i]):
        phis_none[dat[{Column name of note_id}][i]] = dat[{Column name of note_text}][i]
    else:
        phis[dat[Column name of note_id][i]] = dat[{Column name of note_text}][i]


regex_path = {PATH to PHI regex folder}
file_list = os.listdir(regex_path)


patterns = []
for file in file_list:
    if file.endswith('_transformed.txt'):
        with open(regex_path + file) as r:
            patterns.append(re.compile(r.readline()))
			
# Search Type 1 error (non-detected PHI)
			
non_detected_dict_keys = []

for notes in phis.items():
    """
    패턴에 하나라도 detect되면 match된 것이기 때문에
    스위치 형태로 처리한다.
    """
    phisSwitch = False
    
    for p in patterns:
        if p.search(notes[1]) is not None: 
            phisSwitch = True
            continue
    
    if phisSwitch == False:
        non_detected_dict_keys.append(notes[0])

if len(non_detected_dict_keys) > 0:
	print(non_detected_dict_keys)



# Search Type 2 error (detected non-PHI)
false_detected_dict_keys = []

for notes in phis_none.items():
    phisSwitch = True
    
    for p in patterns:
        if p.search(notes[1]) is None: 
            phisSwitch = False
            continue
    
    if phisSwitch == True:
        false_detected_dict_keys.append(notes[0])



if len(false_detected_dict_keys) > 0 :
	print(false_detected_dict_keys)



