import qbootstrapper as qb
import re


def parse_form(form):
    '''Takes Flask request object and parses to dict for bootstrapping'''
    insts = {}
    insts['insts'] = {}
    for key, value in form.items():
        if key == '': continue
        num = re.sub('\D', '', key)
        try:
            num = int(num)
            if num not in insts['insts']: insts['insts'][num] = {}
            term = key.split('-')[-1]
            insts['insts'][num][term] = value
        except ValueError:
            insts[key] = value
    return insts

