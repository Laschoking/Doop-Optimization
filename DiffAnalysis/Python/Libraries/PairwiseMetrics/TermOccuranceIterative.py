from collections import Counter
from Python.Libraries import Classes
from Python.Libraries.MappingStrategies.Iterative_Anchor_Mapping import *


class TermOccuranceIterative(Iterative_Anchor_Mapping):
    def __init__(self,paths):
        super().__init__(paths,"TermOccuranceIterative")


    def similarity(self,term_name1,term_obj1,term_name2,term_obj2):
        # compress the term-occurances
        counter1 = Counter({key : len(val) for key,val in term_obj1.occurrence.items()})
        counter2 = Counter({key : len(val) for key,val in term_obj2.occurrence.items()})
        intersection = counter1 & counter2
        structural_sim = intersection.total() **2 / (counter1.total() + counter2.total())
        # eventually integrate lexical similarity
        join_atoms = []
        # maybe it would be smarter to calculate this only after mapping has been accepted
        # on the other hand: when including the neighbour sim we need this info here
        # overlap consists of file, col_nr
        for overlap in intersection:
            join_atoms.append((overlap + (term_obj1.occurrence[overlap],term_obj2.occurrence[overlap])))
        return structural_sim, join_atoms