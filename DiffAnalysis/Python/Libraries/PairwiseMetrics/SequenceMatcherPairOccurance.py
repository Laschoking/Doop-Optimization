from Python.Libraries.MappingStrategies.Crossproduct_Mapping import *
from Python.Libraries.MappingStrategies.Crossproduct_Mapping_Queue import *

import difflib
from collections import Counter

'''
Nutzung der Built-in Funktion aus Python für Score [0,1]
Ausserdem wird gezählt, wie oft die Terme in der gleichen Spalte einer Relation vorkommen
score = sim_score(0-1) + countPair(1-...)
'''

class SequenceMatcherPairOccurance(Crossproduct_Mapping_Queue):
    def __init__(self,paths):
        super().__init__(paths,"SequenceMatcher+PairOccurance")

    def similarity(self,term1,term2,term1_occ,term2_occ):
        # similarity was already calculated (just increase by one then)
        counter1 = Counter(term1_occ.keys())
        counter2 = Counter(term2_occ.keys())
        intersection = counter1 & counter2
        nr_inters = intersection.total()
        # based on the path to the first relation, determine path to second relation
        if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
            max_int = max(int(term1), int(term2))
            if max_int > 0:
                return nr_inters +  abs(int(term1) - int(term2)) / max_int
            else:
                return   nr_inters + 1
        else:
            return   nr_inters +  difflib.SequenceMatcher(None, term1, term2).ratio() + 1