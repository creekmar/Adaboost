from node_classes import *


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
            node_lst.append(Node(attr, line[8]))
    return node_lst


def main():
    node_list = read_file("dtree-data.dat")
    print(node_list)


if __name__ == '__main__':
    main()


