import sys
from algorithms import *
from metrics import *

if __name__ == '__main__':
    if len(sys.argv) != 4:
        exit()
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    config_file = sys.argv[3]

    train_dataset = dict()
    train_categories = dict()
    test_dataset = dict()
    ground_truth = list()
    labels_test = list()

    with open(train_file, 'r') as f:
        header = f.readline().strip('\n')
        attributes = header.split(',')
        train_lines = f.readlines()

    goal = attributes[-1]

    for attr in attributes:
        train_categories[attr] = set()

    for line in train_lines:
        elements = line.split(',')
        goal_attr = elements[-1].strip('\n')
        del elements[-1]
        for attr, value in zip(attributes, elements):
            train_categories[attr].add(value)
        train_categories[attributes[-1]].add(goal_attr)
        ground_truth.append(goal_attr)

    for idx, line in enumerate(train_lines):
        elements = line.strip('\n').split(',')
        x = dict()
        for i, attr in enumerate(attributes):
            x[attr] = elements[i]
        train_dataset[idx] = x

    with open(test_file, 'r') as f:
        header = f.readline().strip('\n')
        test_lines = f.readlines()

    for idx, line in enumerate(test_lines):
        elements = line.strip('\n').split(',')
        labels_test.append(elements[-1])
        x = dict()
        for i, attr in enumerate(attributes):
            x[attr] = elements[i]
        test_dataset[idx] = x

    mode = 'test'
    model_name = 'ID3'
    max_depth = -1
    num_trees = 1
    f_ratio = 0.5
    e_ratio = 0.5

    with open(config_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip('\n')
        if line.startswith('mode='):
            mode = line.strip('mode=')
        elif line.startswith('model='):
            model_name = line.strip('model=')
        elif line.startswith('max_depth=') and line.strip('max_depth=') not in ('', ' ', '\n'):
            max_depth = int(line.strip('max_depth='))
        elif line.startswith('num_trees='):
            num_trees = int(line.strip('num_trees='))
        elif line.startswith('feature_ratio=') and line.strip('feature_ratio=') not in ('', ' ', '\n'):
            f_ratio = float(line.strip('feature_ratio='))
        elif line.startswith('example_ratio=') and line.strip('example_ratio=') not in ('', ' ', '\n'):
            e_ratio = float(line.strip('example_ratio='))

    plural_value = plurality_value(train_dataset, goal)
    attributes = set(train_categories.keys()) - {goal}
    predictions = list()
    examples = list(test_dataset.values())

    if model_name == 'ID3':
        model = ID3(train_categories, goal, mode, max_depth)
        model.fit(train_dataset, attributes, None)
        pprint(model.tree)
        drvo_ispis = ispis_razina(model.tree, attributes, 0, [])
        for i, (var, razi) in enumerate(drvo_ispis):
            if i == len(drvo_ispis) - 1:
                print("{}:{}".format(razi, var), end='')
            else:
                print("{}:{}, ".format(razi, var), end='')
        print('')
    else:
        model = RF(train_categories, goal, mode, max_depth, num_trees, f_ratio, e_ratio, train_dataset, labels_test)
        model.fit()
        for instances, features in model.subtrees.values():
            for feature in features[0:-1]:
                print("{} ".format(feature), end='')
            print('')
            for instance in instances:
                print("{} ".format(instance), end='')
            print('')

    predictions = model.predict(test_dataset, plural_value, train_dataset)
    for prediction in predictions:
        print("{} ".format(prediction), end='')
    print('')
    printing_metrics(predictions, labels_test, train_categories.get(goal))
