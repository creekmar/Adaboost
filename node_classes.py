"""
Ming Creekmore
Professor Jansen Orfan
Introduction to AI
Classes to use for training and testing data. Node is used for training data
Tree_Node is a general binary tree but is used in testing to represent the decision tree
"""

from dataclasses import dataclass
from typing import Union

# Boolean values to represent the languages
EN = False
NL = True


@dataclass
class Node:
    """
    Node to represent training data
    :attributes: a list of boolean type attributes that help determine what language
    :type: the type of language it actually is
    :weight: how much emphasis adaboost gives to identify it
    :correct: whether it was classified correctly or not
    """
    attributes: list
    type: bool
    weight: float
    correct: bool

@dataclass
class Tree_Node:
    """
    Represents a binary tree
    :value: the value of the tree node
    :left: the left node
    :right: the right node
    """
    value: str
    left: Union[None, "Tree_Node"]
    right: Union[None, "Tree_Node"]

