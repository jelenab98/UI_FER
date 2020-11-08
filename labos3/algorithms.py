from metrics import *
import random
from pprint import pprint


class ID3:
    def __init__(self, train_unique_values, goal, mode, max_depth=-1):
        self.category_dict = train_unique_values
        self.goal = goal
        self.max_depth = max_depth
        self.mode = mode
        self.tree = {}

    def fit(self, examples_main, attributes_main, parent_examples_main):
        """
        Metoda koja implementira učenje modela, a ujedno i wrappa metodu fun u kojoj se događa samo učenje modela.
        Budući da imamo rekurziju, a koristimo, odnosno stablo mora biti varijabla razreda, koristimo sljedeći oblik
        koda.
        :param examples_main: ulazni set za učenje, svakom iteracijom se iz njega miču određene vrijednosti
        :param attributes_main: ulazni set svih atributa koji se provjeravaju za usporedbu vrijednosti informacije,
        oni se također svakom iteracijom smanjuju
        :param parent_examples_main: roditeljske klauzule koje koriste za određivanje lista ukoliko se isprazne primjeri
        :return: pohranjivanje vrijednosti u varijablu razreda tree
        """
        goal = self.goal
        cat_dict = self.category_dict
        max_depth = self.max_depth
        mode = self.mode

        def fun(examples, attributes, parent_examples, depth):
            """
            Metoda koja implementira operaciju učenja modela. Metoda je reukruzivna kako bi se moglo izraditi stablo, a
            postoji nekoliko uvjeta zaustavljanja - dostignuta maksimalna dubina (vraća se najčešća vrijednost čvora),
            prazan skup za učenje, istoimene klase u listovima i prazan skup atributa. U slučaju praznih skupova vraća
            se najčešća vrijednost čvora.
            :param examples: skup za učenje kojeg svakim korakom reduciramo
            :param attributes: lista atributa koje možemo ispitivati
            :param parent_examples: skup roditeljskih primjera za učenje
            :param depth: trenutna razina stabla
            :return: rječnik koji predstavlja jedan dio stabla
            """
            if depth == max_depth:
                if len(examples) != 0:
                    return plurality_value(examples, goal)
                else:
                    return plurality_value(parent_examples, goal)
            if len(examples) == 0:
                return plurality_value(parent_examples, goal)
            flag, label = same_class_check(examples, goal)
            if flag:
                return label
            elif len(attributes) == 0:
                return plurality_value(examples, goal)
            else:
                a = importance(examples, attributes, goal, mode)
                tree = {a: {}}
                attrs = cat_dict.get(a)
                for atr in attrs:
                    exs = extract_examples(examples, a, atr)
                    subtree = fun(exs, attributes - {a}, examples, depth + 1)
                    tree[a][atr] = subtree
            return tree

        self.tree = fun(examples_main, attributes_main, parent_examples_main, 0)

    def predict(self, examples, class_for_error, trainset):
        """
        Metoda koja određuje predikciju za poslani primjer atributa. Primjer se šalje rekurzivno po stablu i u svakom
        koraku se određuje podstablo u koje treba ući. Budući da je ovo rekurzivna funkcija, a stablo je pohranjeno kao
        varijabla razreda, koristila sam wrappanje funkcije kako se ne bi poremetile vrijednosti u stablu.
        :param trainset: skup za ucenje koji sluzi da bi se odredila najcesca vrijednost
        :param examples: ulazni skup podataka za testiranje
        :param class_for_error: ukoliko neke vrijednosti nema u stablu, ispisuje se najčešća vrijednost
        :return: labela ciljnog atributa
        """
        attributes = self.category_dict.keys()
        goal = self.goal

        def fun(test_data, tree, d, dataset):
            """
            Pomoćna metoda koja traži predikciju po stablu.
            :param test_data: ulazni primjerak za koji se traži predikcija
            :param tree: primjerak trenuatčnog drva
            :param d: najcesca vrijednost ciljnog atributa za ispis u slucaju nepoznate vrijednosti
            :param dataset: skup za ucenje na temelju kojeg se racuna najcesca vrijednost
            :return: jedna od vrijednosti ciljnog atributa
            """
            if isinstance(tree, dict):
                for key in test_data.keys():
                    if key not in tree:
                        continue
                    try:
                        if key in attributes:
                            d = plural_subvalue(dataset, key, test_data[key], goal)
                        subtree = tree[key][test_data[key]]
                    except KeyError:
                        return d
                    if isinstance(subtree, dict):
                        return fun(test_data, subtree, d, dataset)
                    else:
                        return subtree
        predictions = list()

        for example in examples.values():
            predictions.append(fun(example, self.tree, class_for_error, trainset))
        return predictions

    def predict2(self, example, class_for_error, trainset):
        """
        Metoda koja određuje predikciju za poslani primjer atributa. Primjer se šalje rekurzivno po stablu i u svakom
        koraku se određuje podstablo u koje treba ući. Budući da je ovo rekurzivna funkcija, a stablo je pohranjeno kao
        varijabla razreda, koristila sam wrappanje funkcije kako se ne bi poremetile vrijednosti u stablu.
        Ova metoda je namijenjena za RF.
        :param trainset: skup za ucenje da bi mogli odrediti najcescu vrijednost
        :param example: ulazni skup podataka za testiranje
        :param class_for_error: ukoliko neke vrijednosti nema u stablu, ispisuje se najčešća vrijednost
        :return: labela ciljnog atributa
        """
        attributes = self.category_dict.keys()
        goal = self.goal

        def fun(test_data, tree, d, dataset):
            if isinstance(tree, dict):
                for key in test_data.keys():
                    if key not in tree:
                        continue
                    try:
                        if key in attributes:
                            d = plural_subvalue(dataset, key, test_data[key], goal)
                        subtree = tree[key][test_data[key]]
                    except KeyError:
                        return d
                    if isinstance(subtree, dict):
                        return fun(test_data, subtree, d, dataset)
                    else:
                        return subtree
            else:
                return tree
        predictions = fun(example, self.tree, class_for_error, trainset)
        return predictions


class RF:
    def __init__(self, train_unique_values, goal, mode, max_depth, num_trees, f_ratio, e_ratio, data_set, ground_truth):
        self.category_dict = train_unique_values
        self.goal = goal
        self.max_depth = max_depth
        self.mode = mode
        self.num_trees = num_trees
        self.data_set = data_set
        self.ground_truth = ground_truth
        self.instance_subset = round(e_ratio * len(self.data_set))
        self.feature_subset = round(f_ratio * len(train_unique_values))
        self.trees = dict()
        self.subtrees = dict()
        self.attributes = dict()

    def fit(self):
        """
        Metoda učenja koja pokreće učenje svakog nasumično generiranog podstabla. Svako stablo se sprema kako bi se
        moglo kasnije evaluirati. Stablo se izgrađuje na temelju nasumično generiranog primjeraka iz skupa za učenje i
        koristi se samo nasumično generirani broj značajki.
        :return:
        """
        goal_set = {self.goal}
        for tree in range(self.num_trees):
            new_data_set_index = random.choices(range(0, len(self.data_set)), k=self.instance_subset)
            new_feature_index = random.sample(range(0, len(self.category_dict)-1), self.feature_subset)
            new_feature_index.append(len(self.category_dict)-1)
            new_data_set = list()
            self.attributes[tree] = list()
            for idx in new_data_set_index:
                subdict = self.data_set.get(idx)
                new_sub_dict = dict()
                for index, (feature, value) in enumerate(subdict.items()):
                    if index in new_feature_index:
                        new_sub_dict[feature] = value
                new_data_set.append(new_sub_dict)
            for index, feature in enumerate(self.category_dict.keys()):
                if index in new_feature_index:
                    self.attributes[tree].append(feature)
            train_set_reduced = dict()
            for i, example in enumerate(new_data_set):
                train_set_reduced[i] = example

            model = ID3(self.category_dict, self.goal, self.mode, self.max_depth)
            model.fit(train_set_reduced, set(self.attributes[tree]) - goal_set, None)
            self.subtrees[tree] = [new_data_set_index, self.attributes[tree]]
            self.trees[tree] = model
            print("Subtree {}:".format(tree))
            pprint(model.tree)
            print()
        return

    def predict(self, examples, error_value, trainset):
        """
        Metoda predikcije koja za svako poddrvo računa predikcije i točnost te odabire najbolje rješenje.
        Za svaki primjer iz ulaznog seta se naprave predikcije svih podstabla i ona vrijednost koja je najčešća postaje
        predikcija za taj primjer skupa za testiranje.
        :param trainset: skup za ucenje da bi mogli odrediti najcescu vrijednost
        :param examples: skup podataka za testiranje
        :param error_value: vrijednost koja se ispisuje u slučaju greške
        :return:
        """
        results = list()
        for example in examples.values():
            predictions = dict()
            val_max = -1
            for index in self.subtrees.keys():
                model = self.trees[index]
                prediction = model.predict2(example, error_value, trainset)
                if prediction in predictions:
                    predictions[prediction] += 1
                else:
                    predictions[prediction] = 1
            for pred, val in predictions.items():
                if val > val_max:
                    val_max = val
                    k_max = pred
                elif val == val_max:
                    k_max = min(k_max, pred)
            results.append(k_max)
        return results


def ispis_razina(drvo, kategorije, razina, lista):
    """
    Pomoćna metoda za ispisivanje razina stabla odluka. Standardna metoda za ispisivanje rekurzivno postavljenih
    rječnika kada se čita svaki sljedeći ključ
    :param drvo: stablo odluke po kojem se krece
    :param kategorije: lista kategorija da se zna koje treba ispisivat
    :param razina: razina u odnosu na korijen
    :param lista: pomocna struktura za ispis tih vrijednosti
    :return: lista u kojoj su zapamcene razine za pojedinu kategoriju
    """
    if isinstance(drvo, dict):
        for key in drvo.keys():
            if key in kategorije:
                lista.append((key, razina))
                lista = ispis_razina(drvo[key], kategorije, razina+1, lista)
            else:
                lista = ispis_razina(drvo[key], kategorije, razina, lista)
    return lista


def extract_examples(examples, attribute, category):
    """
    Metoda koja stvara novi podskup primjera za ucenje ovisno o vrijednosti atributa.
    :param examples: skup primjera za učenje
    :param attribute: atribut za koji izdvajamo vrijednosti
    :param category: kategorija unutar atributa za koju tražimo podskup
    :return: riječnik reduciranog broj primjera
    """
    new_examples = dict()
    for idx, (ex, values) in enumerate(examples.items()):
        if values[attribute] == category:
            new_examples[idx] = values
    return new_examples
