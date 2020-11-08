import math


def accuracy(predictions, ground_truth):
    """
    Metoda koja implementira računanje točnosti po kriteriju accuracy = correct/total.
    Ovaj način mjerenja točnosti nije dobar za evaluiranje ukoliko se u skupu podataka nalazi veliki disbalans
    između klasa.
    :param predictions: lista predikcija
    :param ground_truth: lista stvarnih vrijednosti
    :return: vrijednost točnosti
    """
    total = len(predictions)
    correct = 0
    for prediction, truth in zip(predictions, ground_truth):
        if prediction == truth:
            correct += 1
    return float(correct)/total


def confusion_matrix(predictions, ground_truth):
    """
    Metoda koja implementira matricu zabune. Pozicija (x,y) označava da je x predikcija, dok je y istina
    :param predictions: lista predikcija
    :param ground_truth: lista stvarnih vrijednosti
    :return: ispisuje matricu na stdout
    """
    matrix_of_confusion = dict()
    for pred, truth in zip(predictions, ground_truth):
        if (pred, truth) not in matrix_of_confusion:
            matrix_of_confusion[(pred, truth)] = 1
        else:
            matrix_of_confusion[(pred, truth)] += 1
    return matrix_of_confusion


def printing_metrics(predictions, ground_truth, categories):
    """
    Pomoćna metoda za printanje metrika, odnosno točnosti i matrice zabune.
    :param predictions: lista predikcija
    :param ground_truth: lista stvarnih vrijednosti
    :param categories: lista kategorija koje se ispituju
    :return: ispis na stdout
    """
    acc = accuracy(predictions, ground_truth)
    print("{:.5f}".format(acc))
    matrix = confusion_matrix(predictions, ground_truth)
    for cat_h in sorted(categories):
        for cat_v in sorted(categories):
            print("{} ".format(matrix.get((cat_v, cat_h), 0)), end='')
        print('')


def entropy(vals):
    """
    Metoda koja računa vrijednost entropije. Entropija se računa kao suma -p*log(p,2)
    :param vals: lista koja sadrži kvantitetu svake kategorije za pojedini atribut, oblik [broj_za_p, broj_za_n]
    :return: vrijednost entropije za određeni atribut
    """
    total = sum(vals)
    h = 0
    for val in vals:
        if val == 0:
            continue
        h -= float(val)/total * math.log(float(val)/total, 2)
    return h


def calculate_d(dataset, goal):
    """
    Metoda koja računa ukupnu entropiju cijelog dataseta. Izvajamo van vrijednosti ciljnog atributa, računamo odnose
    jedinstvenih odnosa te računamo entropiju.
    :param dataset: skup primjera s definiranim vrijednostima atributa
                    oblik: {redni_broj: {atr1:vrijednost1, atr2:vrijednost2,..., goal:labela}}
    :param goal: ciljni atribut, za lakšu navigaciju po kodu
    :return: vrijednost entropije za ciljne vrijednosti
    """
    labels = list()
    for values in dataset.values():
        labels.append(values[goal])
    stats = calculate_unique_categorical_frequency(labels)
    return entropy(stats)


def information(d, total,  vals_categorical):
    """
    Metoda koja računa gain za određeni atribut.
    :param d: ukupna entropija
    :param total: broj uzoraka u datasetu
    :param vals_categorical: lista vrijednosti pojavaljivanja određene kategorije unutar atributa
                            oblik: {kategorija: [broj_pojavljivanja_p, broj_pojavljivanja_n,]}
    :return: gain za taj atribut
    """
    h = d
    for category, vals_category in vals_categorical.items():
        n = sum(vals_category)
        h_category = entropy(vals_category)
        h -= float(n)/total * h_category
    return h


def plurality_value(dataset, goal_attribute):
    """
    Metoda koja traži najzastupljeniju klasu u ciljnim klasama i vraća tu klasu
    :param dataset: skup podataka na kojima treniramo
    :param goal_attribute: oznaka ciljnog atributa
    :return: vrijednost ciljne klase koja je najzastupljenija, bira onu koja je alfabetski manje vrijednosti
    """
    goal_dict = dict()
    for example in dataset.values():
        g = example.get(goal_attribute)
        if g in goal_dict:
            goal_dict[g] += 1
        else:
            goal_dict[g] = 1
    g_max = -1
    for k, v in goal_dict.items():
        if v > g_max:
            g_max = v
            k_max = k
        elif v == g_max:
            k_max = min(k, k_max)
    return k_max


def plural_subvalue(dataset, attr, feature, goal_attribute):
    """
    Metoda koja računa najčešću vrijednost ciljnog atributa za trenutačni čvor. Uzima u obzir samo one vrijednosti koje
    imaju odgovarajuću vrijednost značajke za taj čvor.
    :param dataset: skup podataka za testiranje
    :param attr: ime atributa koji se ispituje
    :param feature: vrijednost značajke po kojoj selektiramo
    :param goal_attribute: ime ciljnog atributa za lakšu navigaciju
    :return: vrijednost najčešće značajke ciljnog atributa
    """
    goal_dict = dict()
    for example in dataset.values():
        if example[attr] == feature:
            goal = example[goal_attribute]
            if goal in goal_dict:
                goal_dict[goal] += 1
            else:
                goal_dict[goal] = 1
    g_max = -1
    for k, v in goal_dict.items():
        if v > g_max:
            g_max = v
            k_max = k
        elif v == g_max:
            k_max = min(k, k_max)
    return k_max


def calculate_unique_categorical_frequency(goal_values):
    """
    Metoda koja računa frekvenciju pojavljivanja pojedine kategorije unutar atributa
    :param goal_values: lista kategorija unutar atributa
    :return: lista pojavljivanja za svaku ciljnu mogućnost, oblik [broj_p_ponavljanja, broj_n_ponavljanja]
    """
    goal_statistics = dict()
    for val in goal_values:
        if val in goal_statistics:
            goal_statistics[val] += 1
        else:
            goal_statistics[val] = 1
    return goal_statistics.values()


def calculate_unique_categorical(values):
    """
    Metoda koja određuje frekvenciju kategorija unutar atributa s obzirom na ciljni atrbut. Dakle, za svaku kategoriju
    u atributu određuje koliko je zastupljena naspram ciljnih klasa/labela.
    :param values: lista parova oblika (kategorija, ciljna labela) za određeni atribut
    :return: rječnik oblika : {kategorija: [broj_ponavljanja_labele1, broj_ponavljanja_labele2]}
    """
    categorical_stats = dict()
    for val, goal in values:
        if val in categorical_stats:
            categorical_stats[val].append(goal)
        else:
            categorical_stats[val] = [goal]
    for category, goals in categorical_stats.items():
        categorical_stats[category] = calculate_unique_categorical_frequency(goals)
    return categorical_stats


def importance(dataset, attributes, goal_attribute, mode):
    """
    Metoda koja odabire atribut koji će postati korijen stabla.
    :param dataset: skup primjera nad kojima se gradi stablo
    :param attributes: skup atributa koji su preostali za ispitivanje
    :param goal_attribute: ciljni atribut radi lakše navigacije kroz riječnike
    :return: ime atributa s najvećom vrijednosti informacije
    """
    attr_dict = dict()
    d = calculate_d(dataset, goal_attribute)
    if mode != 'test':
        print("E = {:.4f}, ".format(d), end='')
    total = len(dataset)
    for attr in attributes:
        if attr == goal_attribute:
            continue
        attr_dict[attr] = list()
    h_max = -math.inf
    atr_max = ''
    for values in dataset.values():
        for attr in attributes:
            if attr == goal_attribute:
                continue
            attr_dict[attr].append((values[attr], values[goal_attribute]))
    for attr, values in attr_dict.items():
        stats = calculate_unique_categorical(values)
        h = information(d, total, stats)
        if mode != 'test':
            print("IG({}) = {:.4f} ".format(attr, h), end='')
        if h > h_max:
            h_max = h
            atr_max = attr
        elif h == h_max:
            atr_max = min(atr_max, attr)
    if mode != 'test':
        print('')
    return atr_max


def same_class_check(dataset, goal_attribute):
    """
    Metoda koja provjerava je su li u datasetu ostali svi primjeri s istom vrijednosti ciljnog atributa.
    :param dataset: skup primjera nad kojim se provodi učenje
    :param goal_attribute: ciljni atribut
    :return: False ukoliko su različite klase, True i ime labele ukoliko je ista vrijednost svih
    """
    class1 = ''
    for example in dataset.values():
        if class1 == '':
            class1 = example[goal_attribute]
        elif example[goal_attribute] != class1:
            return False, None
    return True, class1
