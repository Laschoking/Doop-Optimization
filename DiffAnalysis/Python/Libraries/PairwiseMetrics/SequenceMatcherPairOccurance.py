from Python.Libraries.MappingStrategies.Crossproduct_Mapping import *
import difflib

'''
Nutzung der Built-in Funktion aus Python für Score [0,1]
Ausserdem wird gezählt, wie oft die Terme in der gleichen Spalte einer Relation vorkommen
score = sim_score(0-1) + countPair(1-...)
'''

class SequenceMatcherPairOccurance(Crossproduct_Mapping):
    def __init__(self,paths):
        super().__init__(paths,"SequenceMatcher+PairOccurance")

    def similarity(self,term1,term2,sim):
        # similarity was already calculated (just increase by one then)
        if sim > 0:
            return sim + 1
        # based on the path to the first relation, determine path to second relation
        if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
            max_int = max(int(term1), int(term2))
            if max_int > 0:
                return 1 - abs(int(term1) - int(term2)) / max_int
            else:
                return 1
        else:
            return difflib.SequenceMatcher(None, term1, term2).ratio() + 1