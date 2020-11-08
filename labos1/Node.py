class Node:
    """
    Klasa Node služi nam kao struktura za čvorove grafa.
    Klasa je implementirana po uzoru na primjer iz knjige, ali uz male preinake.
    ************************************************************************************************************************
    Varijabla state pamti stanje čvora s grafa.

    Varijabla parent pamti referncu na roditelja u stablu pretraživanja.

    Varijabla action pamti prijelaz koji je napravljen, za naše slučajeve prijelaz će biti istoznačan sa stanjem.

    Varijabla heuristic pamti vrijednost heuristike.

    Varijabla cost pamti trošak puta do tog čvora.

    Funkcija is_root služi nam kao provjera je li neki čvor početni, odnosno korijenski.

    Napomena: varijabla action je u našim slučajevima suvišna jer je u sva tri testna slučaja, novo stanje je istoimeno s
    prijelazom/akcijom. Primjer kada bismo na temelju akcije određivali stanje je da je svaki prijelaz definiran imenom,
    tada bismo koristili drukčiju strukturu ulaznih podataka i imali bismo rječnik koji bilježi prijelate,
    npr na karti Istre konkretno:
        parent: čvor sa stanjem Pula
        action: Medulinska cesta/Biškupija
        state: problems.transitions.get((Pula, Medulinska cesta/Biškupija))
        heuristic : heuristics.get(state)
        cost : parent.cost + problems.costs((Pula, Medulin))
    Još jedan primjer bio bi za 3x3 puzzle kada bi action označavale kuda pomičemo pločicu, npr desno/dolje/gore,...
    ************************************************************************************************************************
    Autorica: Jelena Bratulić
    """
    def __init__(self, state, parent=None, action=None, heuristic=0.0, cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.heuristic = heuristic
        self.cost = cost

    def is_root(self):
        return self.parent == None
