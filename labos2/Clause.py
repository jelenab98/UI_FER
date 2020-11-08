class Clause:
    """
    2. laboratorijska vježba iz predmeta Umjetna inteligencija u ak.godini 2019./2020.
    --------------------------------------------------------------------------------------------------------------------
    Ovo je kod za drugu laboratorijsku vjezbu iz predmeta Umjetna inteligencija u akademskoj godini 2019./2020.
    Ovaj dio koda prikazuje implementaciju klase Clause koja se koristi za pohranjivanje podataka po jedinoj klauzuli.
    Klasa ima jednu varijablu, a to je set literala za koje vrijedi da su u CNF zapisu.
    --------------------------------------------------------------------------------------------------------------------
    Autorica: Jelena Bratulić
    """
    def __init__(self, set_of_input_literals):
        self.literals = set(sorted(set_of_input_literals))

    def __hash__(self):
        """
        Overrideana metoda za izračun hash vrijednosti klauzule.
        :return:
        """
        return hash(tuple(self.literals))

    def __eq__(self, other):
        """
        Overrideana metoda za izračun jednakosti klauzule.
        :param other: druga klauzula s kojom se uspoređuje.
        :return:
        """
        return tuple(self.literals) == tuple(other.literals)

    def __str__(self):
        """
        Overrideana metoda koja nam pomaze kod ispisa literala.
        :return:
        """
        return ' v '.join([str(literal) for literal in self.literals])

    def check_for_redundancy(self, clauses):
        """
        Provjeravamo postoji li u nekoj drugoj klauzuli podksup naše klauzule kako bismo znali možemo li skratiti,
        odnosno reducirati nepotrebne literale.
        Ova metoda nam je potrebna za implementaciju strategije brisanja.
        :param clauses:
        :return: True ako sadrži podskup, dakle mičemo poslanu ili False ako ne sadrži podskup
        """
        for clause in clauses:
            if clause == self:
                continue
            if clause.literals.issubset(self.literals):
                return True
        return False

    def check_for_pair_resolving(self, clause):
        """
        Provjeravamo postoji li u nekoj drugoj klauzuli negacija naših literala kako bismo znali izbaciti višak, odnosno
        nepotrebne literale. Ukoliko se nalazi negacija, moramo maknuti taj negirani i njegov suprotni jer ce oni
        davati teutologiju, odnosno uvijek istinu i to nam nista ne znaci, odnosno ne daje nam neku potrebnu informaciju
        kojom bismo nesto opovrgnuli.
        :param clause: klauzula koju provjeravamo
        :return: True ako se suprotni nalazi u drugoj klauzuli, False inace.
        """
        for literal in self.literals:
            if literal.get_negative() in clause.literals:
                return True
        return False

    def check_for_pair_resolving2(self, clauses):
        """
        Provjeravamo postoji li u nekoj drugoj klauzuli negacija naših literala kako bismo znali izbaciti višak, odnosno
        nepotrebne literale. Ukoliko se nalazi negacija, moramo maknuti taj negirani i njegov suprotni jer ce oni
        davati teutologiju, odnosno uvijek istinu i to nam nista ne znaci, odnosno ne daje nam neku potrebnu informaciju
        kojom bismo nesto opovrgnuli.
        :param clauses: skup klauzula koje provjeravamo
        :return: True ako se suprotni nalazi u drugoj klauzuli, False inace.
        """
        for clause in clauses:
            for literal in self.literals:
                if literal.get_negative() in clause.literals:
                    return True
        return False

    def create_negative_clause(self):
        """
        Metoda koja stvara novi set negiranih klauzula. Koristi se za ciljnu klauzulu kako bi se transformirale
        njezine klauzule i pretvorile u oblik za provjeru.
        Negacijom klauzule koja predstavlja literal1 V literal2 nastat ce 2 klauzule sa  zasebnim negiranim literalom
        :return: novi set negiranih klauzula
        """
        return_set = set()
        for literal in self.literals:
            return_set.add(Clause([literal.get_negative()]))
        return return_set

    def remove_tautology(self):
        """
        Vracamo klauzulu iz koje smo maknuli tautologiju, odnosno literale iz klauzule zbog kojih ce ona uvijek biti
        istinite. Takvi literali, a i klauzule ne utjecu na istinitost cijele klauzule i mogu se slobodno maknuti.
        Provjeru provodimo na nacin da gledamo ima li u samoj klauzuli neki literal u oba stanja.
        :return: klauzula s ociscenim literalima ili None ako se ciscenjem micu svi literali
        """
        set_without_tautology = set()
        for literal in self.literals:
            if literal.get_negative() not in self.literals:
                set_without_tautology.add(literal)
        if len(set_without_tautology) != 0:
            return Clause(set_without_tautology)
        else:
            return None

    def resolve_pair(self, other):
        """
        Metoda koja siri poslane klauzule na nacin da ih istodobno i fakrotrizira, odnosno mice visak.
        Ovu metodu smo malo izmijenili i ona nece vracati set mogucih rezolventi vec samo jednu za zadnji pronadeni
        literal koji se moze rezolvirati. Nema smisla vracati sve jer kada se makne tautologija, bit ce samo jedna
        klauzula. Jos jedna modifikacija je da se odmah tu maknu svi komplementarni literali pa ne moramo provoditi
        izbacivanje tautologije.
        :param other: druga klauzula koja se ispituje
        :return: None ako nema literala u novoj klauzuli ili nova klauzula
        """
        new_literals = set()
        literall = None
        for literal1 in self.literals:
            if literal1.get_negative() in other.literals or literal1.get_negative() in self.literals:
                literall = literal1
            new_literals.add(literal1)
        for literal2 in other.literals:
            new_literals.add(literal2)
        if literall:
            new_literals.remove(literall)
            new_literals.remove(literall.get_negative())
        if len(new_literals) != 0:
            return Clause(new_literals)
        else:
            return None
