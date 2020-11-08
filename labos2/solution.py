"""
2. laboratorijska vježba iz predmeta Umjetna inteligencija u ak.godini 2019./2020.
------------------------------------------------------------------------------------------------------------------------
Ovo je kod za drugu laboratorijsku vjezbu iz predmeta Umjetna inteligencija u akademskoj godini 2019./2020.
Kod je oragniziran u tri klase - Literal,Clause i Resolution koje implementiraju potrebne strukture za ostvarenje
rezolucije opovrgivanjem. Buduci da se rezolucija ostvaruje uz upravljačku strategiju skupa potpore i brisanje klauzula,
bilo je potrebno implemenirati dodatne metode za provjeru i micanje tautologije te faktorizaciju samih klauzula.
Sama logika algoritma rezolcije je jednostavna i sastoji se od toga da se prolazi kroz sve parove i one koje se moze
razrijesiti (koji imaju suprotne literale u sebi), razrijese se, odnosno spoje se, a suprotni literali se maknu.
Takoder, potrebno je provesti izbacivanje tautologije i faktorizaciju literala kako bi algoritam bio ispravan
i optimalan.
------------------------------------------------------------------------------------------------------------------------
Autorica: Jelena Bratulić
"""

import sys
from Literal import Literal
from Clause import Clause
from Resolution import Resolution


def reading_from_file(input_file_clauses, input_file_user=None):
    clauses_set = set()
    clauses_dictionary = dict()
    instructions_list = list()
    goal_c = None

    with open(input_file_clauses, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('#'):
            continue
        data = line.strip('\n')
        data = data.split(' ')
        literal_list = list()
        for char in data:
            positive = True
            if char.startswith('~'):
                positive = False
                char = char.lstrip('~')
            if char.lower() == 'v':
                continue
            char = char.lower()
            literal_list.append(Literal(char, positive))
        clauses_set.add(Clause(literal_list))
        clauses_dictionary[Clause(literal_list)] = len(clauses_dictionary)
        goal_c = Clause(literal_list)
    if input_file_user:
        with open(input_file_user, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('#'):
                continue
            data = line.strip('\n')
            data = data.split(' ')
            stat = -1
            literal_list = list()
            for char in data:
                positive = True
                char = char.lower()
                if char.startswith('~'):
                    positive = False
                    char = char.lstrip('~')
                if char == 'v':
                    continue
                if char == '+':
                    stat = 0
                if char == '-':
                    stat = 1
                if char == '?':
                    stat = 2
                if stat == -1:
                    literal_list.append(Literal(char, positive))
            instructions_list.append((Clause(literal_list), stat))

    return clauses_set, clauses_dictionary, instructions_list, goal_c


if __name__ == '__main__':

    args = sys.argv
    test_name = args[1]
    path_file_clauses = args[2]
    path_file_commands = None
    flag_for_printing = False
    if len(args) == 4:
        if args[3] == 'verbose':
            flag_for_printing = True
        else:
            path_file_commands = args[3]
    elif len(args) == 5:
        path_file_commands = args[3]
        flag_for_printing = True

    clauses, clauses_dict, instructions, goal = reading_from_file(path_file_clauses, path_file_commands)
    if len(instructions) != 0:
        for clause, status in instructions:
            if status == 0:
                if clause not in clauses_dict:
                    clauses_dict[clause] = len(clauses_dict)
                    clauses.add(clause)
            if status == 1:
                if clause in clauses_dict:
                    del clauses_dict[clause]
                    clauses.remove(clause)
            if status == 2:
                clauses_copy = clauses.copy()
                clauses_dict_copy = clauses_dict.copy()
                resolution = Resolution(clauses_copy, clauses_dict_copy,  clause, flag_for_printing)
    else:
        if test_name == 'resolution':
            del clauses_dict[goal]
            clauses.remove(goal)
            resolution = Resolution(clauses, clauses_dict, goal, flag_for_printing)
        else:     # ako je cooking_interactive
            print("Testing {} with standard resolution".format(test_name))
            print("Constructed with knowledge:")
            for c in clauses:
                print("> {}".format(c))
            line_in = input(">>> Please enter your query\n>>> ")
            while line_in.lower() != 'exit':
                if line_in.startswith('#'):
                    line_in = input(">>> Please enter your query\n>>> ")
                    continue
                data_in = line_in.strip('\n')
                data_in = data_in.split(' ')
                status = -1
                literals = list()
                for c in data_in:
                    pos = True
                    c = c.lower()
                    if c.startswith('~'):
                        c = c.lstrip('~')
                        pos = False
                    if c == 'v':
                        continue
                    if c == '+':
                        status = 0
                    if c == '-':
                        status = 1
                    if c == '?':
                        status = 2
                    if status == -1:
                        literals.append(Literal(c, pos))
                clause = Clause(literals)
                if status == 0:
                    if clause not in clauses_dict:
                        clauses_dict[clause] = len(clauses_dict)
                        clauses.add(clause)
                        print(">>> Added {}".format(clause))
                if status == 1:
                    if clause in clauses_dict:
                        del clauses_dict[clause]
                        clauses.remove(clause)
                        print(">>> Removed {}".format(clause))
                if status == 2:
                    clauses_copy = clauses.copy()
                    clauses_dict_copy = clauses_dict.copy()
                    resolution = Resolution(clauses_copy, clauses_dict_copy, clause, flag_for_printing)
                line_in = input(">>> Please enter your query\n>>> ")
