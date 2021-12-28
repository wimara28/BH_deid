#-*- coding: utf-8 -*-

"""
저장된 regular expression을 바탕으로 pseudo-labeling하는 코드
주의점 : 코드가 작성 된 시점에 저장된 regular expression만을 바탕으로 하므로,
regular expression 파일이 수정되거나 삭제 시 적절한 결과가 나오지 않을 수 있다.
마찬가지로 추가되는 파일에 대해서도 고려되지 않으므로, pseudo-labeling formula를 일일이 추가해주어야 한다.
"""

import argparse
import copy
import re
import pandas as pd


def main():
    notes = {}

    for i in range(len(dat)):
        notes[dat['NOTE_ID'][i]] = dat['NOTE_TEXT'][i]

    save_origins = copy.deepcopy(notes)
    pattern = Pattern()
    formula = Formula()

    for k in notes.keys(): # Set order if want
        notes[k] = re.sub(pattern.patient_name(), formula.patient_name, notes[k])
        notes[k] = re.sub(pattern.medical_staff_01(), formula.medical_staff_01, notes[k])
        notes[k] = re.sub(pattern.medical_staff_02(), formula.medical_staff_02, notes[k])
        notes[k] = re.sub(pattern.medical_staff_03(), formula.medical_staff_03, notes[k])
        notes[k] = re.sub(pattern.medical_staff_04(), formula.medical_staff_04, notes[k])
        notes[k] = re.sub(pattern.medical_staff_05(), formula.medical_staff_05, notes[k])
        notes[k] = re.sub(pattern.medical_staff_06(), formula.medical_staff_06, notes[k])

        patterns = pattern.date() # get several patterns from directory
        for p in patterns:
            notes[k] = re.sub(p, formula.date, notes[k])

        patterns = pattern.org()
        for p in patterns:
            notes[k] = re.sub(p, formula.org, notes[k])

        notes[k] = re.sub(pattern.region(), formula.region, notes[k])
        notes[k] = re.sub(pattern.nums(), formula.nums, notes[k])

        patterns = pattern.etc()
        for p in patterns:
            notes[k] = re.sub(p, formula.etc, notes[k])

    return

class Pattern():
    def __init__(self):
        pass

    def patient_name(self):
        regex = 'regex/name_patients/patients_transformed.txt'  # path to patient regular expression texts
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_01(self):
        regex = 'regex/name_medicalStaff/PF_NAME_kor_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_02(self):
        regex = 'regex/name_medicalStaff/confirmed_01_medical_staff_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_03(self):
        regex = 'regex/name_medicalStaff/confirmed_02_medical_staff_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_04(self):
        regex = 'regex/name_medicalStaff/confirmed_03_medical_staff_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_05(self):
        regex = 'regex/name_medicalStaff/salutations_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def medical_staff_06(self):
        regex = 'regex/name_medicalStaff/prepos_NAME_kor_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def date(self):
        patterns = [] # If the category has several patterns
        regex = 'regex/dates/'
        if file.endswith('_transformed.txt'):
            with open(regex + file, encoding='utf-8') as r:
                patterns.append(re.compile(r.readline()))
        return patterns

    def org(self):
        patterns = []
        regex = 'regex/organizations/'
        if file.endswith('_transformed.txt'):
            with open(regex + file, encoding='utf-8') as r:
                patterns.append(re.compile(r.readline()))
        return patterns

    def region(self):
        regex = 'regex/district_kor_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def nums(self):
        regex = 'regex/phone/nums_transformed.txt'
        with open(regex, encoding='utf-8') as r:
            patterns = re.compile(r.readline())
        return patterns

    def etc(self):
        patterns = []
        regex = 'regex/etc/'
        if file.endswith('_transformed.txt'):
            with open(regex + file, encoding='utf-8') as r:
                patterns.append(re.compile(r.readline()))
        return patterns


class Formula():
    def __init__(self):
        pass

    def patient_name(self, matchObj):
        match = matchObj.group()
        if not match:  # if a note doesn't contain any PHI
            return
        convertString = " 'O'" * (len(match.split()) - 1) + " 'PER-B'"
        return convertString

    def medical_staff_01(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'O' " * (len(match.split()) - 1) + "'PER-B'"
        return convertString

    def medical_staff_02(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'O'" + " 'PER-B'" * (len(match.split())-1)
        return convertString

    def medical_staff_03(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'O' 'O'" + " 'PER-B'" * (len(match.split())-2)
        return convertString

    def medical_staff_04(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'O' 'O'" + " 'PER-B'" * (len(match.split())-2)
        return convertString

    def medical_staff_05(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'PER-B'" + " 'O'"
        return convertString

    def medical_staff_06(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'O'" + " 'PER-B'"
        return convertString

    def date(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'DAT-B'" + " 'DAT-I'" * (len(match.split())-1)
        return convertString

    def org(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'ORG-B'" + " 'ORG-I'" * (len(match.split())-1)
        return convertString

    def region(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'LOC-B'"
        return convertString

    def nums(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'NUM-B'" + " 'NUM-I'" * (len(match.split())-1)
        return convertString

    def etc(self, matchObj):
        match = matchObj.group()
        if not match:
            return
        convertString = "'ETC-B'" + " 'ETC-I'" * (len(match.split())-1)
        return convertString


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Select how to de-identify information')
    parser.add_argument('--input', '-i', default='data/tagging_input.csv')  # notes
    parser.add_argument('--regex', '-r', default='regex/')  # regular expression rules set
    parser.add_argument('--output', '-o', default='data/pseudoLabeling_output.csv')  # path to save the results

    args = parser.parse_args()

    inputNote = args.input
    regex = args.regex
    output = args.output

    dat = pd.read_csv(inputNote, encoding='utf-8')
    label = ["'PER-B'", "'PER-I'", "'DAT-B'", "'DAT-I'", "'ORG-B'",
             "'ORG-I'", "'LOC-B'", "'LOC-I'", "'NUM-B'", "'NUM-I'", "'ETC-B'", "'ETC-I'"] # modify it if labels changed

    main()


