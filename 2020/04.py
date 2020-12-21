import re


with open('04.txt') as f:
    lines = [_.strip() for _ in f.readlines()]


def passports():
    passport = ''
    for line in lines:
        if not line:
            yield passport
            passport = ''
        else:
            passport += ' ' + line
    if passport:
        yield passport


def code1():
    n_valid = 0
    for passport in passports():
        bools = [re.search(r'\b%s:' % _, passport) for _ in 'byr iyr eyr hgt hcl ecl pid'.split()]
        if all(bools):
            print(passport)
            n_valid += 1
    print(n_valid)


def valid(passport):
    field = dict()
    bools = [re.search(r'\b%s:' % _, passport) for _ in 'byr iyr eyr hgt hcl ecl pid'.split()]
    if all(bools):
        for _ in 'byr iyr eyr hgt hcl ecl pid'.split():
            m = re.search(r'\b%s:([^ ]+)' % _, passport)
            field[_] = m.group(1)
        if (1920 <= int(field['byr']) <= 2002) is False:
            return False
        if (2010 <= int(field['iyr']) <= 2020) is False:
            return False
        if (2020 <= int(field['eyr']) <= 2030) is False:
            return False
        m = re.match(r'(\d+)(cm|in)', field['hgt'])
        if not m:
            return False
        height = int(m.group(1))
        unit = m.group(2)
        if (unit == 'cm' and 150 <= height <= 193 or unit == 'in' and 59 <= height <= 76) is False:
            return False
        if not re.match(r'^#[0-9a-f]{6}$', field['hcl']):
            return False
        if field['ecl'] not in 'amb blu brn gry grn hzl oth':
            return False
        if not re.match(r'^\d{9}$', field['pid']):
            return False
        return True
    else:
        return False


def code2():
    n_valid = 0
    for passport in passports():
        if valid(passport):
            print(passport)
            n_valid += 1
    print(n_valid)


code2()
