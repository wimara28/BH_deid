import re

s1 = '2012-04-03에 확인되었고 2012-07- 17에 치료하였음'
p1 = '\d{4}\s?[-]\s?\d{2}\s?[-]\s?\d{2}'

matches = re.findall(p, s)

def convert_date(matchObj):

    match = matchObj.group()
    resultString = 'DATE-B ' + 'DATE-I ' * (len(match.split())-1)

    return resultString

print(re.sub(p1, convert_test, s1) + '\n')
"""
output : DATE-B 에 확인되었고 DATE-B DATE-I 에 치료하였음
"""