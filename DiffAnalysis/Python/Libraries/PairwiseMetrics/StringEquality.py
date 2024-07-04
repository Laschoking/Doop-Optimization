from Python.Libraries.MappingStrategies.Crossproduct_Mapping_Queue import *
import difflib

class StringEquality(Crossproduct_Mapping_Queue):
    def __init__(self,paths):
        super().__init__(paths,"StringEquality")

    def similarity(self,term1,term2,occ1,occ2):
        if term1 == term2:
            return 1
        else:
            return 0