class Problem:
    """
    Klasa Problem sadrži informacije o grafu.
    ************************************************************************************************************************
    U rječniku actions, nalazi se popis djece za pojedino stanje, odnosno njegovi successori.
            oblik: roditelj => lista_djece

    U rječniku costs nalaze se podaci cijene prijelaza za pojedini prijelaz.
            oblik: (roditelj, dijete) => cijena

    U rječniku parent_dict nalazi se popis roditelja za ciljna stanja.
            oblik: ciljno_stanje => lista_roditelja

    U listi goal sprema se popis ciljnih stanja grafa.

    U varijabli initial_state sprema se početno stanje grafa.

    Funkcija reading služi za čitanje podataka o grafu iz primljene datoteke i ispis podataka o grafu.
    ************************************************************************************************************************
    Autorica: Jelena Bratulić
    """
    def __init__(self, input_file):
        self.goal = list()
        self.actions = dict()
        self.costs = dict()
        self.parent_dict = dict()
        self.reading(input_file)

    def goal_test(self, node):
        return node.state in self.goal

    def reading(self, input_file):
        index = 0
        with open(input_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        for each_line in lines:
            if each_line.startswith('#'):
                continue
            if index == 0:
                self.initial_state = each_line.strip('\n')
                index += 1
                continue
            if index == 1:
                values = each_line.split(' ')
                for each in values:
                    self.goal.append(each.strip('\n'))
                index += 1
                continue
            data = each_line.split(':')
            if data[1] == '\n':
                self.actions[data[0]] = []
                continue
            parent = data[0]
            data = data[1].strip().split(' ')
            action_list = list()
            for i in data:
                values = i.split(',')
                name = values[0]
                cost = values[1]
                action_list.append(name)
                self.costs[(parent, name)] = float(cost)
                if name in self.goal:
                    if name in self.parent_dict.keys():
                        parents = self.parent_dict.get(name)
                        parents.append(parent)
                        self.parent_dict[name] = parents
                    else:
                        parents = list()
                        parents.append(parent)
                        self.parent_dict[name] = parents
            self.actions[parent] = action_list
        print("Start state: {}".format(self.initial_state))
        print("End state(s): {}".format(self.goal))
        print("State space size: {}".format(len(self.actions)))
        print("Total transitions: {}".format(sum(len(each) for each in self.actions.values())))
        return
