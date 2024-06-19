from Python.Libraries import Classes

class StringEqualityBaseline(Classes.Bijection):
    def __init__(self,paths):
        super().__init__(paths,"StringEqualityBaseline")

    def compute_similarity(self,data_frame):
        # based on the path to the first relation, determine path to second relation
        for file in data_frame.db1_original_facts.files:
            col_len = data_frame.db1_original_facts.files[file]
            cols1 = data_frame.db1_original_facts.data_cols[file]
            cols2 = data_frame.db2_original_facts.data_cols[file]
            for col_nr in range(col_len):
                for term1 in cols1[col_nr]:
                    for term2 in cols2[col_nr]:
                        if term1 == term2 and (term1, term2) not in self.similarity_dict:
                             self.similarity_dict[(term1, term2)] = 1