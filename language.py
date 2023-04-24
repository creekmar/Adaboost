"""
Ming Creekmore
Professor Jansen Orfan
Introduction to AI

6 ways to classify whether a sentence is dutch or english
Each take in a word list and compare against either common words in eng/dutch or the last
one that just counts v and w frequency
"""

def eng_art(word_lst):
    """
    Compares a word list and sees if any english articles are in them
    :param word_lst: List of words
    :return: True if there are english articles, false otherwise
    """
    for word in word_lst:
        if word == "the":
            return True
        if word == "a":
            return True
        if word == "an":
            return True
    return False


def nl_vowel(word_lst):
    """
        Compares a word list and sees if any unique dutch vowel sounds are in them
        :param word_lst: List of words
        :return: True if there are dutch vowels, false otherwise
        """
    vowel_lst = ["aa", "aai", "auw", "eeuw", "ieuw", "ouw", "uu"]
    for word in word_lst:
        for vowel in vowel_lst:
            if vowel in word:
                return True
    return False


def dutch_art(word_lst):
    """
        Compares a word list and sees if any dutch articles are in them
        :param word_lst: List of words
        :return: True if there are dutch articles, false otherwise
        """
    for word in word_lst:
        if word == "de":
            return True
        if word == "het":
            return True
        if word == "een":
            return True
        if word == "en":
            return True
        if word == "die":
            return True
    return False


def en_pronouns(word_lst):
    """
        Compares a word list and sees if any english pronouns are in them
        :param word_lst: List of words
        :return: True if there are english pronouns, false otherwise
        """
    pronouns = ["he", "she", "her", "me", "him", "them", "they", "you", "I"]
    for word in word_lst:
        if word in pronouns:
            return True
    return False


def en_connecting(word_lst):
    """
        Compares a word list and sees if any english connecting words are in them
        :param word_lst: List of words
        :return: True if there are english connecting words, false otherwise
        """
    connecting = ["to", "for", "of", "are", "was", "but", "if"]
    for word in word_lst:
        if word in connecting:
            return True
    return False


def vw_count(word_lst):
    """
        Compares a word list and sees how many v's and w's there are (this is a bit
        more arbitrary and could lead to wrong classifications depending on the sentence)
        :param word_lst: List of words
        :return: True if there are more than 5 v's and w's in the 15 words, false otherwise
        """
    count = 0
    for word in word_lst:
        for ch in word:
            if ch == 'v' or ch == 'w':
                count += 1
                if count > 5:
                    return True
    return False
