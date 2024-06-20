from Python.Libraries import Classes

# each Mapping has a Strategie and a similarity metric
class Mapping():
    def __init__(self, paths, name):
        self.name = name
        self.db2_merged_facts = Classes.DB_Instance(paths.db2_facts, name)
        self.db2_nemo_merged_results = Classes.DB_Instance(paths.db2_results, name)

        self.db1_inv_bij_results = Classes.DB_Instance(paths.db1_results, name)
        self.similarity_dict = dict()
        self.mapping = dict()

    def set_mapping(self, mapping):
        self.mapping = mapping
    def compute_mapping(self,db1,db2):
        pass

    def similarity(self):
        pass


    def merge_dbs(self,db1,db2):
        new_var_counter = 0
        for file in db1.files:
            rows1 = db1.data_rows[file]
            rows2 = db2.data_rows[file]
            bijected_db = set()
            target_db = set()
            target_db.update([tuple(row) for row in rows2])
            for row1 in rows1:
                bijected_row = []
                for term in row1:
                    if term in self.mapping:
                        bijected_row.append(self.mapping[term])
                    else:
                        new_term = "new_var_" + str(new_var_counter)
                        self.mapping[term] = new_term  # introduce new variables
                        new_var_counter += 1
                        bijected_row.append(new_term)
                bijected_db.add(tuple(bijected_row))
            merged_rows = []
            common_rows = bijected_db.intersection(target_db)
            target_db = target_db.difference(common_rows)
            bijected_db = bijected_db.difference(common_rows)
            for row in common_rows:
                merged_rows.append(list(row) + ['0'])
            for row in bijected_db:
                merged_rows.append(list(row) + ['1'])
            for row in target_db:
                merged_rows.append(list(row) + ['10'])
            self.db2_merged_facts.insert_records(file, merged_rows)

    def inverse_mapping(self, from_identifier):
        inv_bijection = dict((term2, term1) for term1, term2 in self.mapping.items())
        for file in self.db2_nemo_merged_results.files:
            db1_bij_rows = []
            for row2 in self.db2_nemo_merged_results.data_rows[file]:
                # only reverse rows that have the common_identifier (0) or the from_identifier (1/2)
                if row2[-1] == '0' or row2[-1] == str(from_identifier):
                    db1_bij_row = []
                    for term2 in row2[0:-1]:
                        if term2 in inv_bijection:
                            db1_bij_row.append(inv_bijection[term2])
                            # neuen eintrag
                        else:
                            # since there is no matching, but the term belongs to db1 its value was copied directly
                            # this happens if constants have been introduced in the PA
                            # print("no inverse bijection found for this term: " + term2 )
                            db1_bij_row.append(term2)
                    db1_bij_rows.append(db1_bij_row)
            self.db1_inv_bij_results.insert_records(file, db1_bij_rows)
        self.db1_inv_bij_results.write_data_to_file()
        # return self.db1_inv_bij_results
