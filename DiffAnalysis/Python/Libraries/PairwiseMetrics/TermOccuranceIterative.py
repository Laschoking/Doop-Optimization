from collections import Counter
from Python.Libraries import Classes
from Python.Libraries.MappingStrategies.Iterative_Anchor_Mapping import *


class TermOccuranceIterative(Iterative_Anchor_Mapping):
    def __init__(self,paths):
        super().__init__(paths,"TermOccuranceIterative")


    def similarity(self,term1,term1_occ,term2,term2_occ):
        counter1 = Counter(term1_occ.keys())
        counter2 = Counter(term2_occ.keys())
        intersection = counter1 & counter2
        structural_sim = -2 * intersection.total() / (counter1.total() + counter2.total())
        # eventually integrate lexical similarity
        # TODO: currently priority queue works with minimal value first
        # file, t1_row, t2_row
        join_atoms = []
        for overlap in intersection:
            join_atoms.append(overlap + (term1_occ[overlap],term2_occ[overlap]))
        return structural_sim,join_atoms