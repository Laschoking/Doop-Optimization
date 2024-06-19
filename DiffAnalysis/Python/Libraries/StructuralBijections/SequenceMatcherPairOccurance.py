from difflib import SequenceMatcher
from Python.Libraries import Classes

'''
Nutzung der Built-in Funktion aus Python für Score [0,1]
Ausserdem wird gezählt, wie oft die Terme in der gleichen Spalte einer Relation vorkommen
score = sim_score(0-1) + countPair(1-...)
'''

class SequenceMatcherPairOccurance(Classes.Bijection):
    def __init__(self,paths):
        super().__init__(paths,"SequenceMatcher+PairOccurance")

    def compute_similarity(self,data_frame):
        # based on the path to the first relation, determine path to second relation
        for file in data_frame.db1_original_facts.files:
            nr_cols = data_frame.db1_original_facts.files[file]
            cols1 = data_frame.db1_original_facts.data_cols[file]
            cols2 = data_frame.db2_original_facts.data_cols[file]
            for ind in range(nr_cols):
                for term1 in cols1[ind]:
                    for term2 in cols2[ind]:
                        if (term1, term2) not in self.similarity_dict:
                            if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
                                max_int = max(int(term1), int(term2))
                                if max_int > 0:
                                    sim = 1 - abs(int(term1) - int(term2)) / max_int
                                else:
                                    sim = 1
                            else:
                                sim = SequenceMatcher(None, term1, term2).ratio()
                            self.similarity_dict[(term1, term2)] = sim + 1
                        else:
                            self.similarity_dict[(term1, term2)] += 1
        return
