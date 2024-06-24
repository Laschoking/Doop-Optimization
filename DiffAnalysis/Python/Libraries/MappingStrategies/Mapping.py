from Python.Libraries import Classes
import csv
# each Mapping has a Strategie and a similarity metric
class Mapping():
    def __init__(self, paths, name):
        self.name = name
        self.db1_inv_bij_facts = Classes.DB_Instance(paths.db1_facts,name)
        self.db2_merged_facts = Classes.DB_Instance(paths.db2_facts, name)
        self.db2_nemo_merged_results = Classes.DB_Instance(paths.db2_results, name)

        self.db1_inv_bij_results = Classes.DB_Instance(paths.db1_results, name)
        self.similarity_dict = dict()
        self.mapping = dict()
        self.inverse_mapping = dict()

    def set_mapping(self, mapping):
        self.mapping = mapping
    def compute_mapping(self,db1,db2):
        pass

    def similarity(self):
        pass

    def write_mapping_to_file(self,file):
        if self.mapping:
            with open(file.with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for term1,term2 in self.mapping.items():
                    tsv_writer.writerow([term1,term2])



# can be implemented faster, just replace db
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
                        # TODO: this should better be implemented in the mapping step
                        new_term = "new_var_" + str(new_var_counter)
                        #print("add new var: " + new_term + " for " + term)
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

# bisschen unschlau programmiert, dass db mitgegeben wird aktuell
    def revert_db_mapping(self,from_db,to_db, from_identifier):
        if not self.inverse_mapping:
            self.inverse_mapping = dict((term2, term1) for term1, term2 in self.mapping.items())
        pa_added_terms = set()
        for file in from_db.files:
            inverted_rows = []
            for row2 in from_db.data_rows[file]:
                inverted_row = []
                # only reverse rows that have the common_identifier (0) or the from_identifier (1/2)
                if row2[-1] == '0' or row2[-1] == str(from_identifier):
                    for term2 in row2[0:-1]:
                        if term2 in self.inverse_mapping:
                            inverted_row.append(self.inverse_mapping[term2])
                        else:
                            # this case means, that the Datalog-rules created new terms, which are not part of db1 yet
                            pa_added_terms.add(term2)
                            inverted_row.append(term2)
                    inverted_rows.append(inverted_row)
            # does this actually alter the mapping?
            to_db.insert_records(file,inverted_rows)

        # insert reverted rows into DB
        to_db.write_data_to_file()
        print("terms that have been added by datalog rules: " + str(len(pa_added_terms)))
        print(pa_added_terms)
        return

        # return self.db1_inv_bij_results

