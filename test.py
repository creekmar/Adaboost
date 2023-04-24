"""
Ming Creekmore
Professor Jansen Orfan
Introduction to AI
Program used to test a model, where the model is either a decision tree or an ensemble.
"""

import string
import sys

from node_classes import *
from language import *

def make_tree(f):
    """
    Given an open file, makes a binary decision tree
    :precondition: Must be written in-order with each node going to a new line
        The leaves are alpha while the nodes are numbers
    :param f: the open file to read the data in
    :return: a binary decision tree
    """
    for line in f:
        value = line.strip()
        if value.isalpha():
            return Tree_Node(value, None, None)
        else:
            return Tree_Node(value, make_tree(f), make_tree(f))


def read_test_data(filename):
    """
    Reads in the data to classify. Each line represents a new test to classify
    :param filename: Name of the file that contains the test data
    :return: A list of each test data represented as a list of attributes used to classify
            the language
    """
    test_lst = []
    with open(filename) as f:
        for line in f:
            line = line.translate(str.maketrans('', '', string.punctuation))
            line = line.split()
            attr = [eng_art(line), nl_vowel(line), dutch_art(line), en_pronouns(line),
                    en_connecting(line), vw_count(line)]
            test_lst.append(attr)
    return test_lst


def dt_testing(tree, attr):
    """
    Classifies the language that is represented by the given attribute list
    :param tree: the decision tree to use to classify
    :param attr: the list of binary attributes to test on
    :return: EN or NL as a string
    """
    value = tree.value
    if value.isalpha():
        return value
    else:
        value = int(value)
        if attr[value]:
            return dt_testing(tree.left, attr)
        else:
            return dt_testing(tree.right, attr)


def read_ensemble(f):
    """
    Read in from an open file the hypothesis that will be used to classify language
    :param f: the opened file
    :return: a list of hypothesis, where each hypothesis is just a list of hypothesis data
    """
    ens = []
    for line in f:
        line = line.strip().split()
        line[0] = int(line[0])   # first number is the feat to split on
        line[3] = float(line[3]) # last number is the hyp_weight
        ens.append(line)
    return ens


def ensemble_test(ensemble, attr):
    """
    Given an ensemble of hypothesis, determines what the classification of a language is
    based on the given attributes
    :param ensemble: A list of hypotheses
    :param attr: The attributes that are used to describe the language
    :return: NL or EN as a string
    """
    nl = 0
    en = 0
    for hyp in ensemble:
        if attr[hyp[0]]:
            if hyp[1] == "NL":
                nl += hyp[3]
            else:
                en += hyp[3]
        else:
            if hyp[2] == "NL":
                nl += hyp[3]
            else:
                en += hyp[3]
    if nl > en:
        return "NL"
    else:
        return "EN"


def main():
    """
    Main program to take in a hypothesis model or decision tree model and test data to
    classify the test data
    Prints out what language the model predicts for each line
    Command line arguments are used to determine the filenames
        Usage: test.py hypothesis.txt test_file.txt
    The first line in the model file is used to determine whether adaboost or a decision
    tree model is loaded
    :return: None
    """
    if len(sys.argv) != 3:
        print("Usage: test.py hypothesis.txt test_file.txt")
    else:
        with open(sys.argv[1]) as f:
            test_lst = read_test_data(sys.argv[2])
            dt_ada = f.readline().strip()
            if dt_ada == "dt":
                tree = make_tree(f)
                for attr in test_lst:
                    lang = dt_testing(tree, attr)
                    print(lang)
            else:
                ens = read_ensemble(f)
                for attr in test_lst:
                    lang = ensemble_test(ens, attr)
                    print(lang)

if __name__ == '__main__':
    main()
