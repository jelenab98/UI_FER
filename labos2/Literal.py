class Literal:
    """
    2. laboratorijska vježba iz predmeta Umjetna inteligencija u ak.godini 2019./2020.
    --------------------------------------------------------------------------------------------------------------------
    Ovo je kod za drugu laboratorijsku vjezbu iz predmeta Umjetna inteligencija u akademskoj godini 2019./2020.
    Ovaj dio koda prikazuje implementaciju klase Literal koji implementira strukturu potrebnu za pohranjivanje podataka
    o literalima. Svaki literal je definiran labelom/imenom i oznakom stanja, odnosno je li normalan ili negiran.
    Incijalno je stanje postavljeno u normalno, dakle pozitivno stanje.
    --------------------------------------------------------------------------------------------------------------------
    Autorica: Jelena Bratulić
    """
    def __init__(self, label, state=True):
        self.label = label
        self.positive_state = state

    def __key(self):
        """
        Metoda pomoću koje računamo hash vrijednost literala. Javlja error ako ju nemamo.
        :return:
        """
        return self.label, self.positive_state

    def __hash__(self):
        """
        Overrideana metoda za izracun hash vrijednosti literala, potrebna nam je za razlikovanje instanci literala.
        :return:
        """
        return hash(self.__key())

    def __eq__(self, other):
        """
        Overrideana metoda koja nam je potrebna za lakse i brze usporedivanje literala.
        Dva literala su ista ako imaju iste vrijednosti naziva i oznake stanja.
        :param other: drugi literal s kojim se usporeduje
        :return: True ako su isti, False ako nisu
        """
        return self.label == other.label and self.positive_state == other.positive_state

    def __str__(self):
        """
        Overrideana metoda kako bismo mogli lakše ispisivati rezultat.
        :return:
        """
        if self.positive_state:
            return self.label
        else:
            return '~'+self.label

    def __lt__(self, other):
        """
        Overrideana metoda za usporedbu kako bismo mogli sortirati ulazni set literala
        :param other:
        :return:
        """
        return self.label < other.label

    def get_negative(self):
        """
        Metoda koja vraca negirani literal.
        Vraca ~L.
        :return:
        """
        return Literal(self.label, not self.positive_state)
