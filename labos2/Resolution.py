class Resolution:
    """
    2. laboratorijska vježba iz predmeta Umjetna inteligencija u ak.godini 2019./2020.
    --------------------------------------------------------------------------------------------------------------------
    Ovo je kod za drugu laboratorijsku vjezbu iz predmeta Umjetna inteligencija u akademskoj godini 2019./2020.
    Ovaj dio koda prikazuje implementaciju klase Resolution koja obavlja logiku iz rezolucije opovrgavanjem i za
    poslani set klauzula javlja je li premisa logička posljedica ili ne.
    Prilikom stvaranja instance klase, odmah se i provjerava premisa te se ispisuje prigodna poruka ovisno o rezultatu.
    Ovaj dio koda sam implementirala kao klasu kako bi cjelokupni kod bio pregledniji i sistematicniji.
    --------------------------------------------------------------------------------------------------------------------
    Autorica: Jelena Bratulić
    """
    def __init__(self, clauses, clauses_dict, goal, printing_flag=False):
        """
        Prilikom inicijalzacije klase, klasi je potrebno poslati set klauzula, rječnik podataka o klauzulama, ciljnu
        klauzulu koju se ispituje te, ako je definirana, zastavicu koja označava treba li printati sve ili samo krajnju
        odluku.
        Dodatno u klasi jos postoje i pomocne varijable:
            + searching - sadrzi redoslijed ispitivanja i rezolvenata kako bismo mogli ispisati duzu verziju premisa
            + resolved_pairs_set - pamti parove klauzula koje smo razrijesili
            + number_of_initial_clauses - pamti pocetni broj klauzula kako bismo mogli ispravno formulirati ispis
            + sos_set - set koji u sebi sadrzi negiranu ciljnu klauzulu i nove klauzule
        :param clauses: set klauzula koje cemo provjeravati
        :param clauses_dict: rjecnik klauzula koji nam je pomoc prilikom ispisvanja detaljne pretrage premisa
        :param goal: ciljna premisa koja se ispituje
        :param printing_flag: zastavica koja oznacava hocemo li printati duzu ili kracu verziju
        """
        self.clauses = set(clauses)
        self.clauses_dict = clauses_dict
        self.goal = goal
        self.printing_flag = printing_flag
        self.resolved_pairs_set = set()
        self.searching = list()
        self.number_of_initial_clauses = len(self.clauses)
        self.sos_set = self.goal.create_negative_clause()
        for sos in self.sos_set:
            self.clauses_dict[sos] = len(self.clauses_dict)
        self.resolution()

    def resolution(self):
        """
        Metoda koja implementira algoritam rezolucije opovrgavanjem uz koristenje strategije brisanja i faktoriziranja.
        Moramo provjeriti je li konjukcija svih klauzula i negiranih ciljnih klauzula NIL, ukoliko je tada vrijedi da je
        goal logicka posljedica od clauses.
        :return: True ako je logicka posljedica i false ako nije
        """
        while True:
            new_set = set()
            flag = False
            self.clauses = self.remove_redundant(self.clauses, self.sos_set)
            for clause1, clause2 in self.select_clause():
                resolvent = clause1.resolve_pair(clause2)
                if not resolvent:
                    self.searching.append((self.clauses_dict.get(clause1),
                                           self.clauses_dict.get(clause2), resolvent))
                    if self.printing_flag:
                        self.printing()
                    else:
                        print("{} is true".format(self.goal))
                    return
                self.resolved_pairs_set.add((clause1, clause2))
                flag = True
                resolvent = resolvent.remove_tautology()
                if not resolvent:
                    continue
                if resolvent.check_for_redundancy(self.sos_set) or resolvent in self.sos_set:
                    continue
                if resolvent.check_for_redundancy(new_set) or resolvent in new_set:
                    continue
                if resolvent.check_for_redundancy(self.clauses) or resolvent in self.clauses:
                    continue
                probni = set()
                probni.add(resolvent)
                self.clauses = self.remove_redundant(self.clauses, probni)
                self.sos_set = self.remove_redundant(self.sos_set, probni)
                new_set = self.remove_redundant(new_set, probni)
                new_set.add(resolvent)
                self.clauses_dict[resolvent] = len(self.clauses_dict)
                self.searching.append((self.clauses_dict.get(clause1), self.clauses_dict.get(clause2), resolvent))
            if not flag:
                print("{} is unknown".format(self.goal))
                return
            self.sos_set |= self.remove_redundant(new_set, self.sos_set)

    def remove_redundant(self, set1, set2):
        """
        Vracamo set klauzula u kojima su ostale samo one klauzule
        u kojima nema redudantnih, dakle maknuti su podskupovi.
        Podskupove saznajemo preko provjere redudantnih iz klase Clauses, ako metoda vrati False, znamo da ih ne trebamo
        izbaciti jer su razliciti, odnosno jedan nije podskup drugog.
        :return:set novih klauzula s ociscenim literalima
        """
        clauses_without_redundancy = set()
        for clause in set1:
            if not clause.check_for_redundancy(set2):
                clauses_without_redundancy.add(clause)
        return clauses_without_redundancy

    def select_clause(self):
        """
        Metoda koja vraca sljedeci par klauzula za obradu.
        Uvijek je barem jedna klauzula iz sosa (negativni ciljni i novi), a odabire se ona koja nije obradena, a druga
        je iz klauzula koja sadrzi u sebi neki literal koji je i u klauzuli iz sosa kako bi se mogli oni skratiti.
        Metoda je dodatno optimizirana na način da odmah pronalazi parove koji se mogu rezolvirati pa zapravo prolazi
        kroz manji broj stanja/parova klauzula sveukupno.
        Korisitimo yield da se pamti stanje, ukoliko nije pronaslo parove iz klauzula i sosa, ide jos i po samom sosu
        trazit i onda vraca taj par.
        :return: parovi  koji cekaju na obradu i provjeru
        """

        for clause1 in self.sos_set:
            for clause2 in self.sos_set:
                if (clause1, clause2) not in self.resolved_pairs_set \
                        and (clause2, clause1) not in self.resolved_pairs_set \
                        and clause1.check_for_pair_resolving(clause2):
                    yield clause1, clause2

        for clause1 in self.clauses:
            for clause2 in self.sos_set:
                if (clause1, clause2) not in self.resolved_pairs_set \
                        and (clause2, clause1) not in self.resolved_pairs_set \
                        and clause1.check_for_pair_resolving(clause2):
                    yield clause1, clause2

    def printing(self):
        """
        Pomocna metoda za ispis tijeka pretrazivanja i ispisivanja zakljucka.
        :return:
        """
        i = self.number_of_initial_clauses + 1
        for c, index in self.clauses_dict.items():
            if index < self.number_of_initial_clauses:
                print("{}. {}".format(index + 1, c))
            else:
                break
        print("=============")
        goal_neg = self.goal.create_negative_clause()
        for goal_clause in goal_neg:
            print("{}. {}".format(i, goal_clause))
            i += 1
        print("=============")
        for cl1, cl2, rez in self.searching:
            if not cl1:
                cl1 = 0
            if not cl2:
                cl2 = 0
            if not rez:
                print("{}. NIL ({}, {})".format(i, cl1 + 1, cl2 + 1))
                break
            print("{}. {} ({}, {})".format(i, rez, cl1 + 1, cl2 + 1))
            i += 1
        print('=============')
        print("{} is true".format(self.goal))
        print('')
