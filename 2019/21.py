"""
1ère remarque :
    Quand ça crashe, on voit la partie autour de trou...
2ème remarque :
    Les sauts sont de longueurs 4
3ème remarque :
    Le springscript permet (au moins) de coder systématiquement les expressions du
    type (x|not x and|or y and|or z ...) and|or (x|not x and|or y and|or z ...) and|or ...
    Autrement dit, dans un des termes seul le premier élément peut être nié. Ça
    permet de calculer chaque terme dans T (ou directement dans J pour le premier)
    et d'accumuler dans J.

En avançant dans la solution, on détecte les trous à sauter. Pour la première partie:
#.#
#...#
# # #
#  # #
# #  #
sachant qu'il faut détecter assez tot certaines configurations pour ne pas tomber
dans un trou. Après tatonnements, voici les configurations à sauter pour la 1ère partie :

@
#.      --> not A

@
##..#   --> A and not B and not C and D

@
##.##   --> A et non B et C et D

@
###.#   --> A et B et non C et D

Ce qui donne l'expression :

not A or (A and not B and not C and D) or (A and not B and C and D) or (A and B and not C and D)

On simplifie (après l premier or ) dans Wolfram pour trouver :

not A or (not B and A and D) or (not C and A and D)

qui est sous la forme décrite au dessus et qui donne la solution CODE1.

Pour la 2ème partie, on tombre dans la configuration :

  S   S   !
#####.#.##.##.###

Le premier saut est déclenché par (A and B and not C and D) qu'on contraint en
testant le point d'arrivée du deuxième saut (A and B and not C and D and H).

"""

import intcode


DATA = '21.txt'


CODE1 = '''\
NOT A J
NOT B T
AND D T
OR  T J
NOT C T
AND D T
OR  T J
WALK
'''


CODE2 = '''\
NOT A J
NOT B T
AND D T
OR  T J
NOT C T
AND D T
AND H T
OR  T J
RUN
'''


def run(springscript):
    with open(DATA) as f:
        strcode = f.readline().strip()
        code = intcode.parse_data(strcode)
    computer = intcode.Intcode(code)
    computer.verbose_output = False
    computer.trace = False

    code = [line.strip() for line in springscript.splitlines()]
    codeascii = list()
    for line in code:
        codeascii.extend([ord(char) for char in line] + [10])

    computer.run(codeascii, return_output=False)
    s = ''.join([(chr(x) if x < 256 else str(x)) for x in computer.outvalues])
    print(s)


#run(CODE1)
run(CODE2)
