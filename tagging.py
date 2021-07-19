import os
import argparse

import pandas as pd
import collections
import re
import copy

parser = argparse.ArgumentParser(description='Select how to de-identify information')
parser.add_argument('--input', '-i', default='phis.csv')  # notes
parser.add_argument('--regex', '-r', default='filters/regex/')  # regular expressions
parser.add_argument('--output', '-o', default='output/tagging_phis.csv')
parser.add_argument('--asterisk', '-a', default=False)

args = parser.parse_args()

inputNote = args.input
regex = args.regex
output = args.output
asterisk = args.asterisk

dat = pd.read_csv(inputNote, encoding='utf-8')


def load_notes(pd_data):
    notes_raw = {}

    for i in range(len(pd_data)):
        notes_raw[pd_data['NOTE_ID'][i]] = pd_data['note_text'][i]

    origins_raw = copy.deepcopy(notes_raw)

    return notes_raw, origins_raw


def load_regex(regex_path):
    regex_dir = {}

    for file in os.listdir(regex_path):
        if os.path.isdir(regex_path + file):
            if file == '.ipynb_checkpoints':
                continue
            else:
                regex_dir[file] = regex_path + file + '/'

    return regex_dir


def find_span(span_dict, note_dict, patterns):
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
                with open(i + files) as r:
                    patterns.append(re.compile(r.readline()))

        phis_span_dict = collections.defaultdict(list)
        raw_span = find_span(phis_span_dict, notes_raw, patterns)

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

    transformed.to_csv(output, index=False)


if __name__ == '__main__':
    notes, save_origins = load_notes(dat)
    regex_all = load_regex(regex)
    regexDir = collections.OrderedDict(sorted(regex_all.items()))
    notes_transformed = tagging(notes, regexDir)
    print_output(notes_transformed, save_origins)
