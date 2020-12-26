import re


def code1():
    count = 0
    for n in range(136760, 595730 + 1):
        string = str(n)
        digits = list(string)
        if digits == sorted(digits) and re.search(r'(\d)\1', string):
            count += 1
    print('1>', count)


def code2():
    count = 0
    for n in range(136760, 595730 + 1):
        string = str(n)
        digits = list(string)
        if digits == sorted(digits) and re.search(r'(\d)\1', string):
            for m in re.finditer(r'((\d)\2)', string):
                digit = m.group(2)
                if m.start() > 0 and string[m.start() - 1] == digit:
                    continue
                if m.end() < len(string) and string[m.end()] == digit:
                    continue
                count += 1
                break
    print('2>', count)


code1()
code2()
