from Node import Node
from Problem import Problem
from Heuristic import Heuristic
from util import *
from time import time


def printing_cost(node, explored):
    path = []
    total_cost = node.cost
    while not node.is_root():
        path.append(node.action)
        node = node.parent
    path.append(node.state)
    path.reverse()
    print("States visited = {}".format(len(explored)))
    print("Found path of length {} with total cost {}:".format(len(path), total_cost))
    for each in path:
        if each != path[-1]:
            print("{} =>".format(each))
        else:
            print("{}".format(each))
    return


def printing_no_cost(node, explored):
    path = []
    while not node.is_root():
        path.append(node.action)
        node = node.parent
    path.append(node.state)
    path.reverse()
    print("States visited = {}".format(explored))
    print("Found path of length {}:".format(len(path)))
    for each in path:
        if each != path[-1]:
            print("{} =>".format(each))
        else:
            print("{}".format(each))
    return


class Algorithms:
    """
    Klasa Algorithms implementira 3 algoritma pretraživanja prostora.
    ************************************************************************************************************************
    Varijabla problems sadrži referncu na klasu Problem u kojem se nalaze informacije o grafu.

    Varijabla heuristics sadrži referncu na klasu Heuristic u kojoj su informacije o heuristici grafa.

    Funkcija heuristic_check poziva provjeru heuristike za kriterije optimističnosti i konzistentnosti.

    Funkcija child_node implementirana je po uzoru na algoritam i objašnjenje iz knjige. Funkcija vraća novi čvor djeteta
    za poslanog čvora roditelja i akciju prijelaza. U našem slučaju, sve akcije prijelaza bit će istoimene s novim stanjem
    djeteta.

    Funkcija bfs implementira algoritam BFS-pretraživanje u širinu. Algoritam je implementiran po uputi iz knjige AI: A
    Modern Approach. Radi se o klasičnom algoritmu pretraživanja koji kao strukturu koristi čvorove i queue za baratanje
    s čvorovima. Algoritam je optimalan i potpun.

    Funkcija ucs implementira algoritam UCS-pretraživanje po jednolikoj cijeni. Algoritam je također implementiran po uputi
    iz knjige, a zapravo je proširena verzija BFS-a na način da se koristi prioritetni red i sortiranje po kriteriju cijene
    puta.

    Funkcija astar implementira algoritam a*. Algoritam je također implementiran po uputi iz knjige, dakle on je verzija
    UCS-a, ali se sortiranje reda radi po kriteriju zbroja cijene puta i heuristike tog stanja.

    Napomena: Dobar primjer s Istrom, ali neoprostivo što ste stavili Žminj na kartu, a Sveti Petar u Šumi ne!
                        Sveti Petar u Šumi >> Žminj      Samo Sveti Petar <3

    Final score: 9/10, too much Žminj :)
    ************************************************************************************************************************
    Autorica: Jelena Bratulić
    """
    def __init__(self, input_file_map, input_file_heuristics):
        self.problems = Problem(input_file_map)
        self.heuristics = Heuristic(input_file_heuristics, self.problems)

    def heuristic_check(self):
        print("\nChecking heuristic")
        time_start = time()
        self.heuristics.optimistic_check()
        print("Running time for optimistic check: {} ms".format(1000*(time() - time_start)))
        time_start = time()
        self.heuristics.consistency_check()
        print("Running time for consistency check: {} ms\n".format(1000*(time() - time_start)))
        return

    def child_node(self, parent, action):
        return Node(action, parent, action,
                    self.heuristics.heuristics[action],
                    parent.cost + self.problems.costs[(parent.state, action)])

    def bfs(self):
        print("\nRunning bfs:")
        node = Node(self.problems.initial_state)
        frontier = Queue()
        frontier_state = dict()
        frontier.push(node)
        frontier_state[node.state] = True   # pamti explored i open nodes
        explored = 0
        while not frontier.isEmpty():
            node = frontier.pop()
            frontier_state[node.state] = True
            explored += 1
            if self.problems.goal_test(node):
                printing_no_cost(node, explored)
                return
            for each_action in self.problems.actions[node.state]:
                child = self.child_node(node, each_action)
                if child.state not in frontier_state:
                    frontier.push(child)
                    frontier_state[child.state] = True
        print("Nešto je krivo ups! Put nije pronađen :(")
        return

    def ucs(self):
        print("\nRunning ucs:")
        node = Node(self.problems.initial_state)
        explored = dict()
        frontier_state = dict()
        frontier = PriorityQueue()
        frontier.push(node, node.cost)
        while frontier:
            node = frontier.pop()
            if node.state in frontier_state:
                del frontier_state[node.state]
            explored[node.state] = node.cost
            if self.problems.goal_test(node):
                printing_cost(node, explored)
                return
            for each_action in self.problems.actions[node.state]:
                child = self.child_node(node, each_action)
                if child.state not in explored and child.state not in frontier_state:
                    frontier.push(child, (child.cost, child.state))
                    frontier_state[child.state] = child.cost
                elif child.state in frontier_state:
                    if child.cost < frontier_state.get(child.state):
                        frontier.push(child, (child.cost, child.state))
                        frontier_state[child.state] = child.cost
                elif child.state in explored:
                    if child.cost < explored.get(child.state):
                        del explored[child.state]
                        frontier.push(child, (child.cost, child.state))
                        frontier_state[child.state] = child.cost
        print("Nešto je krivo ups! Put nije pronađen :(")
        return

    def a_star(self):
        print("\nRunning astar:")
        node = Node(self.problems.initial_state)
        explored = dict()
        frontier_state = dict()
        frontier = PriorityQueue()
        frontier.push(node, node.cost)
        while frontier:
            node = frontier.pop()
            if node.state in frontier_state:
                del frontier_state[node.state]
            explored[node.state] = node.cost
            if self.problems.goal_test(node):
                printing_cost(node, explored)
                return
            for each_action in self.problems.actions[node.state]:
                child = self.child_node(node, each_action)
                if child.state not in explored and child.state not in frontier_state:
                    frontier.push(child, (child.cost+child.heuristic, child.state))
                    frontier_state[child.state] = child.cost
                elif child.state in frontier_state:
                    if child.cost < frontier_state.get(child.state):
                        frontier.push(child, (child.cost + child.heuristic, child.state))
                        frontier_state[child.state] = child.cost
                else:
                    if child.cost < explored.get(child.state):
                        frontier.push(child, (child.cost + child.heuristic, child.state))
                        frontier_state[child.state] = child.cost
                        del explored[child.state]
        print("Nešto je krivo ups! Put nije pronađen :(")
        return


if __name__ == '__main__':

    inputs = [('ai.txt', 'ai_pass.txt'),
              ('ai.txt', 'ai_fail.txt'),
              ('istra.txt', 'istra_heuristic.txt'),
              ('istra.txt', 'istra_pessimistic_heuristic.txt'),
              ('3x3_puzzle.txt', '3x3_misplaced_heuristic.txt')]

    for input_file_graph, input_file_heuristic in inputs:
        print("\nReading from {} and {}\n".format(input_file_graph, input_file_heuristic))
        searching_algorithms = Algorithms(input_file_graph, input_file_heuristic)
        searching_algorithms.bfs()
        searching_algorithms.ucs()
        searching_algorithms.a_star()
        searching_algorithms.heuristic_check()
        print("#######################################################################################################")
