"""
Ming Creekmore
Professor Jansen Orfan
Introduction to AI

Name: train.py

A program to learn how to tell the difference between English and Dutch language.
Two different methods are used: A regular decision tree, and Adaboost
The user can decide what to use based on command line arguments
The program outputs a hypothesis file with either an in-order depiction of a decision tree
or a file where every line is a hypothesis and its weight
Usage: train.py training_set.txt hypothesisOut.txt dt_or_ada
"""

import sys
from node_classes import *
import math
from language import *
import string

MAX_DEPTH = 100


def read_file(filename):
    """
    Reads in a file containing training data
    the first 3 characters in the file determine the language type: en| or nl|
    the rest of the line is a part of a sentence(s) in the corresponding language
    specifically 15 words
    :param filename: the filename to open that has the training data
    :return: A list of nodes, where each node is a representation of each training data
            Specifying the langauge it is, the attributes to decide on, the weight,
            and whether the node was classified correctly (used for adaboost)
    """
    node_lst = list()
    with open(filename) as file:
        for line in file:
            lang = line[:2]
            line = line[3:]
            line = line.translate(str.maketrans('', '', string.punctuation))
            line = line.split()
            attr = [eng_art(line), nl_vowel(line), dutch_art(line), en_pronouns(line),
                    en_connecting(line), vw_count(line)]
            if lang == "en":
                node_lst.append(Node(attr, EN, 0, True))
            else:
                node_lst.append(Node(attr, NL, 0, True))

    # default weight
    weight = 1/len(node_lst)
    for node in node_lst:
        node.weight = weight

    return node_lst


def determine_type(lst):
    """
    Determines the percentage of english type the given list has
    :param lst: List of nodes that were classified according to a specific attribute
    :return: the percentage of english type nodes in the split list
    """
    eng_count = 0
    overall_weight = 0
    for node in lst:
        overall_weight += node.weight
        if node.type == EN:
            eng_count += 1 * node.weight
    percentage = eng_count/overall_weight
    return percentage


def calc_entropy(lst, lst_type, length):
    """
    Calculates the entropy of the list of nodes, includes the weight given by adaboost
    :param lst: List of nodes that were classified according to a specific attribute
    :param lst_type: The type of language every node in the split list should be
    :param length: the total number of nodes that were considered in the split
    :return: Calculated Entropy
    """
    num_items = len(lst)/length
    count = 0
    overall_weight = 0

    for node in lst:
        if node.type == lst_type:
            count += 1*node.weight
        overall_weight += node.weight

    if count == 0 or count == overall_weight:
        return 0
    correct = count/overall_weight
    incorrect = (overall_weight-count)/overall_weight

    return num_items * (correct*math.log(1/correct, 2) + incorrect*math.log(1/incorrect, 2))


def split_and_calc(node_lst, index):
    """
    Split nodes between the chosen attribute. If True, goes to left list. If False, goes to
    right list
    :param node_lst: The training data represented as a node list, where node is a Node
        from node_classes
    :param index: The index number/attribute number to split on
    :return: A tuple of data from splitting everything
                left_lst: the list of nodes that were True on the attribute split
                left_type: which language the left group mostly represents
                right_lst: the list of nodes that were False on the attribute split
                right_type: which language the right group mostly represents
                l_entropy: the entropoy calculation of the left_lst
                r_entropy: the entropy calculation of the right_lst
    """
    left_lst = list()
    right_lst = list()
    for node in node_lst:
        if node.attributes[index]:
            left_lst.append(node)
        else:
            right_lst.append(node)

    if len(left_lst) != 0:
        left_perc_en = determine_type(left_lst)
    else:
        left_perc_en = 0
    if len(right_lst) != 0:
        right_perc_en = determine_type(right_lst)
    else:
        right_perc_en = 0
    if left_perc_en > right_perc_en:
        left_type = EN
        right_type = NL
    else:
        right_type = EN
        left_type = NL

    l_entropy = calc_entropy(left_lst, left_type, len(node_lst))
    r_entropy = calc_entropy(right_lst, right_type, len(node_lst))

    return left_lst, left_type, right_lst, right_type, l_entropy, r_entropy


def classified_wrong(node_lst, t):
    """
    Determines the error from the classification. Error is weighted based on adaboost
    weight counts
    :param node_lst: List of nodes that were classified according to a specific attribute
    :param t: the type that every node in the list classification should be
    :return: the weighted error
    """
    count = 0
    for node in node_lst:
        if node.type != t:
            node.correct = False
            count += node.weight
        else:
            node.correct = True
    return count


def get_language(language):
    """
    Given a boolean value, returns the corresponding language
    EN is False
    NL is True
    :param language: boolean value representing a language
    :return: string saying the language
    """
    if language == EN:
        return "EN"
    else:
        return "NL"


def find_best_split(node_lst, index_lst):
    """
    Makes a stump with the attribute giving the least remaining entropy
    :param node_lst: The training data represented as a node list, where node is a Node
        from node_classes
    :param index_lst: index_lst: a list of indexes (representing attribute branching) that
        should be considered for creating stump
    :return: best_tup: which is a tuple containing a collection of the data
                left_lst, left_type, right_lst, right_type, l_entropy, r_entropy
             best_index: which is the index number that we split on
    """
    best_tup = tuple()
    remaining = 1.0
    best_index = -1
    for i in index_lst:
        info_tup = split_and_calc(node_lst, i)
        temp_rem = info_tup[4] + info_tup[5]
        if temp_rem <= remaining:
            remaining = temp_rem
            best_tup = info_tup
            best_index = i
    return best_tup, best_index


def best_dt(node_lst, index_lst, count = 0, max_depth = 2):
    """
    Determines the best decision tree using entropy. Decision tree will only go
    as deep as max_depth
    :param node_lst: The training data represented as a node list, where node is a Node
        from node_classes
    :param index_lst: index_lst: a list of indexes (representing attribute branching) that
        should be considered for creating stump
    :param count: The depth we are at
    :param max_depth: The max depth the decision tree should be
    :return: A string representing the tree where each new line represents a different level
        The string represents the tree in pre-order
        Numbers mean to keep splitting, EN and NL represent the leaves (english or dutch)
    """
    # splitting
    best_tup, best_index = find_best_split(node_lst, index_lst)
    index_lst.remove(best_index)
    tree_string = ""
    tree_string += str(best_index) + "\n"

    # branching on other attributes if we can
    if len(index_lst) != 0:
        # Only split if there is remaining info and max_depth not hit
        # Else we have hit the end result and found a language
        # Left
        if best_tup[4] != 0 and max_depth != count+1:
            tree_string += best_dt(best_tup[0], index_lst.copy(), count + 1, max_depth)
        else:
            tree_string += get_language(best_tup[1]) + "\n"
        # Right
        if best_tup[5] != 0 and max_depth != count+1:
            tree_string += best_dt(best_tup[2], index_lst.copy(), count + 1, max_depth)
        else:
            tree_string += get_language(best_tup[3]) + "\n"
    else:
        tree_string += get_language(best_tup[1]) + "\n"
        tree_string += get_language(best_tup[3]) + "\n"

    return tree_string


def adaboost(node_lst, index_lst, k, f):
    """
    Performs adaboost using the entropy method. The ensemble proposed is written out
    to a file
    The file is written with a header: ada to determine that this is an adaboost method
    Each line represents one hypothesis, and split on space to get the individual hypothesis info
        splitting_attribute_num language_true language_false weight
    :param node_lst: The training data represented as a node list, where node is a Node
        from node_classes
    :param index_lst: a list of indexes (representing attribute branching) that
        should be considered for creating stump
    :param k: the number of hypothesis to give
    :param f: the already open file to write to
    :return: None
    """
    f.write("ada\n")
    for i in range(k):
        best_tup, best_index = find_best_split(node_lst, index_lst)

        # checking error and making sure not dividing by 0
        error = classified_wrong(best_tup[0], best_tup[1]) + classified_wrong(best_tup[2], best_tup[3])
        e = 0.00000000001
        if error > .5:
            pass
        if (1-e) < error:
            error = 1-e
        if error == 0:
            error = node_lst[0].weight/10

        update = error/(1-error)
        h_weight = math.log((1-error)/error)

        # updating weights
        for node in node_lst:
            if node.correct:
                node.weight = node.weight*update

        # normalizing weights
        total_update = 0
        for node in node_lst:
            total_update += node.weight
        for node in node_lst:
            node.weight = node.weight/total_update

        f.write(str(best_index) + " " + get_language(best_tup[1]) + " " + get_language(best_tup[3])
                + " " + str(h_weight) + "\n")



def main():
    """
    Use command line arguments to determine which learning model to use and to give files to use
    Usage: train.py training_set.txt hypothesisOut.txt dt_or_ada
    Will train on the data using either a decision tree or adaboost
    Writes the proposed decision tree or ensemble to given filename
    :return: None
    """
    if len(sys.argv) != 4:
        print("Usage: train.py training_set.txt hypothesisOut.txt dt_or_ada")
    else:
        node_list = read_file(sys.argv[1])
        index_lst = [0,1,2,3,4,5]  # there are only 6 attributes
        with open(sys.argv[2], "w") as f:
            if "dt" == sys.argv[3]:
                tree = best_dt(node_list, index_lst)
                f.write("dt\n")  # used to mark the file as a model of a decision tree
                f.write(tree)
            else:
                adaboost(node_list, index_lst, 3, f)


if __name__ == '__main__':
    main()


