# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 15:34:39 2021

@author: JY
"""

label = ['PER']
s1 = ['O', 'O', 'PER']
s2 = ['PER', 'O', 'O']

for i, tk in enumerate(s2):
	if tk in label:
		s1[i] = tk

print(s1)
		