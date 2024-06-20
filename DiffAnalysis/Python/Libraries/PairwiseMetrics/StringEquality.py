from Python.Libraries.MappingStrategies.Crossproduct_Mapping import *
import difflib
class StringEquality(Crossproduct_Mapping):
    def __init__(self,paths):
        super().__init__(paths,"StringEquality")

    def similarity(self,term1,term2,sim):
        if term1 == term2:
            return 1
        else:
            return 0