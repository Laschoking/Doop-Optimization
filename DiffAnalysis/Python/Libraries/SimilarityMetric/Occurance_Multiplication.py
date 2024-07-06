from collections import Counter
from Python.Libraries import Classes
from Python.Libraries.ExpansionStrategies.Iterative_Anchor_Expansion import *


def occurrence_multiplication(term_name1,term_name2,term_obj1,term_obj2,occ_overlap):
    sum = 0
    for common in occ_overlap:
        sum += term_obj1.occurrence_c[common] * term_obj2.occurrence_c[common]
    return sum