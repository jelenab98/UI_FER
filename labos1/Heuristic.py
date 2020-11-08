from util import *


class Heuristic:
    """
    Klasa heuristic implementira sve potrebne strukture za baratanje s heuristikom grafa i provjerom te same heuristike.
    ***********************************************************************************************************************
    Rječnik heuristics sadrži podatke o vrijednosti heuristike za pojedino stanje.
        oblik: stanje => vrijednost_heuristike

    Rječnik optimistic_error_dict pamti čvorove za koje smo kršenje kriterija optimističnosti heuristike. Dakle za taj čvor
    heuristika premašuje vrijednost stvarne cijene puta od tog čvora do ciljnog čvora.
        oblik: stanje => vrijednost stvarne cijene puta do ciljnog stanja

    Lista consistency_error_list pamti vrijednosti o kršenju kriterija monotonosti/konzistentnosti heuristike.
        oblik: lista čiji su elementi (stanje_roditelja, stanje_djeteta, cijena prijelaza)

    Rječnik optimistic_dijkstra_dict pamti za svako pojedino ciljno stanje stvarne cijene puta od pojedinog čvora do tog
    ciljnog stanja, uzimajući u obzir optimalni put, dakle najjeftiniju varijantu.
        oblik: ciljno_stanje => (stanje_čvora, stvarna_cijena_puta_do_ciljnog_stanja)

    U varijabli problems dana je refenca na strukturu problems koja sadrži podatke o grafu.

    Funkcija reading_heurostic služi za čitanje i razvrstavanje podataka o heuristici grafa.

    Funkcija dijkstra je klasična implementacija dijkstrinog algoritma koji se koristi za traženje optimalnog puta kako
    bismo lakše i brže provjerili ispravnost heuristike. Provjeru optimističnosti odlučila sam odmah optimizirati jer mi se
    ovaj način ispitivanja heuristike čini jedini logičan, a i na taj isti način bih i direktno ručno išla provjeravati.

    Funkcije za provjeru kriterija heuristike implementrane su na način da iterativno provjeravaju zadovljavanje kriterija
    za svako pojedino stanje te koriste pomoćne funkcije za ispis grešaka kako bi kod bio pregledniji.
    ************************************************************************************************************************
    Autorica: Jelena Bratulić
    """
    def __init__(self, input_file, problems):
        self.heuristics = dict()
        self.optimistic_error_dict = dict()
        self.consistency_error_list = list()
        self.reading_heuristics(input_file)
        self.problems = problems
        self.optimistic_dijkstra_dict = self.dijkstra()

    def reading_heuristics(self, input_file):
        with open(input_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        for each_line in lines:
            line = each_line.split(':')
            self.heuristics[line[0]] = float(line[1])
        return

    def dijkstra(self):
        optimal_costs = dict()
        for each_goal_state in self.problems.goal:
            costs_list = list()
            distance = dict()
            prev = dict()
            q = PriorityQueue()
            distance[each_goal_state] = 0
            q.push(each_goal_state, 0)
            while not q.isEmpty():
                state = q.pop()
                invert = False
                if len(self.problems.actions.get(state)) == 0:
                    children = self.problems.parent_dict.get(state)
                    invert = True
                else:
                    children = self.problems.actions.get(state)
                for every_child in children:
                    # print(state, every_child)
                    if invert:
                        cost = distance.get(state) + self.problems.costs.get((every_child, state))
                    else:
                        cost = distance.get(state) + self.problems.costs.get((state, every_child))
                    if every_child in distance:
                        if cost < distance.get(every_child):
                            distance[every_child] = cost
                            prev[every_child] = state
                    else:
                        distance[every_child] = cost
                        prev[every_child] = state
                        q.push(every_child, cost)
            for each_pair in distance.items():
                costs_list.append((each_pair[0], each_pair[1]))
            optimal_costs[each_goal_state] = costs_list
        return optimal_costs

    def consistency_check(self):
        print("Checking if heuristic is consistent.")
        for each_parent in self.problems.actions.keys():
            for each_child in self.problems.actions.get(each_parent):
                if self.heuristics.get(each_parent) > \
                        self.heuristics.get(each_child) + self.problems.costs.get((each_parent, each_child)):
                    self.consistency_error_list.append((each_parent, each_child,
                                                        self.problems.costs.get((each_parent, each_child))))
        if len(self.consistency_error_list) == 0:
            print("Heuristic is consistent")
        else:
            self.print_consistency_error()
            print("Heuristic is not consistent")
        return

    def optimistic_check(self):
        print("Checking if heuristic is optimistic.")
        for each_goal_state in self.optimistic_dijkstra_dict.keys():
            for each_state in self.optimistic_dijkstra_dict.get(each_goal_state):
                if each_state[1] < self.heuristics.get(each_state[0]):
                    self.optimistic_error_dict[each_state[0]] = each_state[1]
        if len(self.optimistic_error_dict.keys()) == 0:
            print("Heuristic is optimistic")
        else:
            self.print_optimistic_error()
            print("Heuristic is not optimistic")
        return

    def print_consistency_error(self):
        if len(self.consistency_error_list) >= 20:
            print("\t[ERR] {} errors, omitting output.".format(len(self.consistency_error_list)))
        else:
            for each_error in self.consistency_error_list:
                print("\t[ERR] h({}) > h({}) + c: {} > {} + {}".format(each_error[0], each_error[1],
                                                                       self.heuristics[each_error[0]],
                                                                       self.heuristics[each_error[1]],
                                                                       each_error[2]))

    def print_optimistic_error(self):
        if len(self.optimistic_error_dict.keys()) >= 20:
            print("\t[ERR] {} errors, omitting output.".format(len(self.optimistic_error_dict.keys())))
        else:
            for each_error in self.optimistic_error_dict.keys():
                print("\t[ERR] h({}) > h*: {} > {}".format(each_error,
                                                           self.heuristics[each_error],
                                                           self.optimistic_error_dict[each_error]))
