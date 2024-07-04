from Python.Libraries.MappingStrategies.Iterative_Anchor_Mapping import *

import difflib
from collections import Counter



class ISUBSequenceMatcher_Iterative_Occ(Iterative_Anchor_Mapping):
    def __init__(self, paths):
        super().__init__(paths, "ISUBSequenceMatcher_Iterative_Occ")

    def similarity(self, term1, term2, term1_occ, term2_occ):
        counter1 = Counter(term1_occ.keys())
        counter2 = Counter(term2_occ.keys())
        intersection = counter1 & counter2
        structural_sim = 2 * intersection.total() / (counter1.total() + counter2.total())

        # eventually integrate lexical similarity
        # TODO: currently priority queue works with minimal value first
        join_atoms = []
        for overlap in intersection:
            join_atoms.append(overlap + (term1_occ[overlap], term2_occ[overlap]))

        # based on the path to the first relation, determine path to second relation
        if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
            max_int = max(int(term1), int(term2))
            if max_int > 0:
                return structural_sim + (1 - abs(int(term1) - int(term2)) / max_int),join_atoms
            else:
                return structural_sim + 1,join_atoms
        else:
            return structural_sim + isub(term1, term2),join_atoms


def isub(st1, st2):
    if st1 is None or st2 is None or st1 == '' or st2 == '':
        return -1

    # count common substrings
    count_lcs = 0
    sm = difflib.SequenceMatcher(None,st1, st2)
    matching_blocks = sm.get_matching_blocks()
    # convert to list to reduce string sice
    l_st1 = len(st1)
    l_st2 = len(st2)
    st1 = list(st1)
    st2 = list(st2)

    # no need to recompute index overlap when we have blocks already
    winkler_st1_ind, winkler_st2_ind, winkler_size = matching_blocks[0]
    for st1_ind, st2_ind, size in matching_blocks:
        if size <= 1: continue  # reached last statement or too small match
        count_lcs += size
        st1[st1_ind:st1_ind + size] = [None] * size
        st2[st2_ind:st2_ind + size] = [None] * size


    comm = 2 * count_lcs / (l_st1 + l_st2)

    # reduce strings of lcs matching
    diff1 = len([c for c in st1 if c]) / l_st1
    diff2 = len([c for c in st2 if c]) / l_st2

    # count differenc of left-overs
    product = diff1 * diff2
    l_st_sum = diff1 + diff2
    p = 0.6
    if l_st_sum - product == 0:
        diff = 0
    else:
        diff = product / (p + (1 - p) * (l_st_sum - product))

    if winkler_st1_ind == 0 and winkler_st2_ind == 0 and winkler_size > 0:
        impr_winkler = min(winkler_size,4) * 0.1 * (1 - comm)
    else:
        impr_winkler = 0

    score =  comm - diff + impr_winkler
    return score
