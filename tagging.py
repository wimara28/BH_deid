#-*- coding: utf-8 -*-
import os
import argparse

import pandas as pd
import collections
import re
import copy
"""
의료노트를 regular expression rules 를 적용한 비식별 완료 형식으로 변환하는 코드
Input 형식 : NOTE_ID / NOTE_TEXT 열이 존재하는 csv 파일
Output 형식 : idx(=NOTE_ID) / origin / transformed 열이 존재하는 csv 파일
기본적으로 ===[PHI: category]=== 형식으로 output을 내지만, -a 를 통해 asterisk(*) 형식으로 결과를 낼 수 있음
"""

def load_notes(pd_data):
    """
    :param pd_data: input note
    :return: idx(NOTE_ID) & note(NOTE_TEXT) set in the form of dictionary,
    / return for processing(notes_raw) and saving(origins_raw)
    """
    notes_raw = {}
    for i in range(len(pd_data)):
        notes_raw[pd_data['NOTE_ID'][i]] = pd_data['NOTE_TEXT'][i]

    origins_raw = copy.deepcopy(notes_raw)

    return notes_raw, origins_raw


def load_regex(regex_path):
    """
    :param regex_path: path where the regular expression rules set is stored.
    This path should contain sub-folders separated by each regular expression category
    ex) regex/date, regex/name, ...
    :return: Dict of {specific file name : the path of it}
    """
    regex_dir = {}

    for file in os.listdir(regex_path):
        if os.path.isdir(regex_path + file):
            if file == '.ipynb_checkpoints':
                continue
            else:
                regex_dir[file] = regex_path + file + '/'

    return regex_dir


def find_span(note_dict, patterns):
    """
    Find span with patterns stored in regular expression rules
    :return: {index with notes containing pattern : span of it}
    """
    span_dict = collections.defaultdict(list)
    for n in note_dict.items():
        note_idx = n[0]
        note = n[1]

        for p in patterns:
            if p.search(note) is not None:
                for m in re.finditer(p, note):
                    span_dict[note_idx].append(m.span())

    return span_dict


def tagging(notes_raw, regex_dir):
    patterns = []

    for key in regex_dir:
        i = regex_dir[key]

        for files in os.listdir(i):
            if files.endswith('_transformed.txt'):
                with open(i + files, encoding='utf-8') as r:
                    patterns.append(re.compile(r.readline()))

        raw_span = find_span(notes_raw, patterns)

        if asterisk:
            for phis in raw_span.items():
                for spans in phis[1]:
                    notes_raw[phis[0]] = notes_raw[phis[0]][:spans[0]] + '*' * (spans[1] - spans[0]) + notes_raw[phis[0]][spans[1]:]
        else:
            for phis in raw_span.items():
                for spans in phis[1]:
                    notes_raw[phis[0]] = notes_raw[phis[0]][:spans[0]] + '$' * (spans[1] - spans[0]) + notes_raw[phis[0]][spans[1]:]
                notes_raw[phis[0]] = re.sub('\${1,}', fr'==[PHI: {key.upper()}]==', notes_raw[phis[0]])

        print(f'>>> {key.upper()} Done')

    return notes_raw


def print_output(notes_tra, origins):
    transformed = pd.DataFrame(columns=['idx', 'origin', 'transformed'])
    idx, tra, ori = [], [], []

    for n in notes_tra.items():
        tra.append(n[1])

    for n in origins.items():
        idx.append(n[0])
        ori.append(n[1])

    if len(tra) == len(ori):
        for i in range(len(tra)):
            transformed.loc[i] = [idx[i], ori[i], tra[i]]
    else:
        print('Not same notes')


    if os.path.exists(output):
        os.remove(output)
    transformed.to_csv(output, index=False, encoding='utf-8-sig')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Select how to de-identify information')
    parser.add_argument('--input', '-i', default='data/tagging_input.csv')  # notes
    parser.add_argument('--regex', '-r', default='regex/')  # regular expression rules set
    parser.add_argument('--output', '-o', default='data/tagging_output.csv')  # path to save the results
    parser.add_argument('--asterisk', '-a', default=False)

    args = parser.parse_args()

    inputNote = args.input
    regex = args.regex
    output = args.output
    asterisk = args.asterisk

    dat = pd.read_csv(inputNote, encoding='utf-8')


    notes, save_origins = load_notes(dat)
    regex_all = load_regex(regex)
    regexDir = collections.OrderedDict(sorted(regex_all.items())) # Apply regex sequentially by category to control the order
    notes_transformed = tagging(notes, regexDir)
    print_output(notes_transformed, save_origins)
