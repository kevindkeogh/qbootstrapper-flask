import qbootstrapper as qb
import re


def parse_request(request):
    '''Takes Flask request object and parses to dict for bootstrapping'''
    nums = []
    for key in request.form.keys():
        nums.append(re.sub('\D', '', key))
    nums = sorted(set(nums))
    insts = dict.fromkeys(nums, None)
    for key, value in request.form.items():
        if key == '': continue
        num = re.sub('\D', '', key)
        try:
            num = int(num)
        except ValueError:
            continue
        if num not in insts: insts[num] = {}
        term = key.split('-')[-1]
        insts[num][term] = value
    return insts

