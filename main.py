from node_classes import *
import math

def read_file(filename):
    node_lst = list()
    with open(filename) as file:
        for line in file:
            line = line.split()
            attr = list()
            for i in range(8):
                if line[i] == "True":
                    attr.append(True)
                else:
                    attr.append(False)
            if line[8] == "A":
                node_lst.append(Node(attr, A))
            else:
                node_lst.append(Node(attr, B))
    return node_lst


def determine_type(lst):
    countA = 0
    for node in lst:
        if node.type == A:
            countA += 1
    percentage = countA/len(lst)
    if percentage > 0.5:
        return A
    else:
        return B


def calc_entropy(lst, lst_type, length):
    num_items = len(lst)/length
    count = 0
    for node in lst:
        if node.type == lst_type:
            count += 1
    if count == 0 or count == len(lst):
        return 0
    correct = count/len(lst)
    incorrect = (len(lst)-count)/len(lst)
    return num_items * (correct*math.log(1/correct, 2) + incorrect*math.log(1/incorrect, 2))


def split_and_calc(node_lst, index):
    true_lst = list()
    false_lst = list()
    for node in node_lst:
        if node.attributes[index]:
            true_lst.append(node)
        else:
            false_lst.append(node)
    if len(true_lst) != 0:
        true_type = determine_type(true_lst)
        false_type = not true_type
    else:
        false_type = determine_type(false_lst)
        true_type = not false_type
    t_entropy = calc_entropy(true_lst, true_type, len(node_lst))
    f_entropy = calc_entropy(false_lst, false_type, len(node_lst))
    return true_lst, true_type, false_lst, false_type, t_entropy, f_entropy


def find_best_split(node_lst, index_lst, count):
    print("BRANCH:", count)
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
    index_lst.remove(best_index)

    print(best_tup[1])
    print(best_tup[0])
    print(best_tup[3])
    print(best_tup[2])
    print("Remaining:", remaining)
    print("True Remain:", best_tup[4])
    print("False Remain:", best_tup[5])
    print("Best index:", best_index, "\n\n")

    # splitting the True list
    if len(index_lst) != 0:
        if best_tup[4] != 0:
            print("TRUE_SPLIT")
            find_best_split(best_tup[0], index_lst.copy(), count + 1)
        if best_tup[5] != 0:
            print("FALSE_SPLIT")
            find_best_split(best_tup[2], index_lst.copy(), count + 1)


def main():
    node_list = read_file("dtree-data.dat")
    find_best_split(node_list, [0,1,2,3,4,5,6,7], 0)


if __name__ == '__main__':
    main()


