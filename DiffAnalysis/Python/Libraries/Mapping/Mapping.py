from Python.Libraries import Classes
import csv
from Python.Libraries import ShellLib
from bidict import bidict
# each Mapping has a Strategie and a similarity metric
class Mapping():
    def __init__(self, paths, exp_name,expansion_strategy,sim_name, similarity_metric):
        name = exp_name + "-" + sim_name
        self.name = name
        self.db1_inv_bij_facts = Classes.DB_Instance(paths.db1_facts,name)
        self.db2_merged_facts = Classes.DB_Instance(paths.db2_facts, name)
        self.db2_nemo_merged_results = Classes.DB_Instance(paths.db2_results, name)

        self.db1_inv_bij_results = Classes.DB_Instance(paths.db1_results, name)
        self.similarity_dict = dict()
        self.mapping = bidict()
        self.new_term_counter = 0
        self.expansion_strategy = expansion_strategy
        self.similarity_metric = similarity_metric

    def set_mapping(self, mapping):
        self.mapping = mapping

    def compute_mapping(self,db1,db2,pa_non_mapping_terms):
        self.expansion_strategy(self,db1,db2,pa_non_mapping_terms,self.similarity_metric)



    # output stuff
    def write_diagnostics(self, data_frame,base_dir):
        out_path = base_dir.joinpath("diagnostic").joinpath(self.name)
        ShellLib.clear_directory(out_path)
        # write mapping
        if self.mapping:
            with open(out_path.joinpath("Mapping").with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for to_term,from_term in self.mapping.items():
                    tsv_writer.writerow([to_term,from_term])

        # write db1 terms
        with open(out_path.joinpath("Terms1").with_suffix('.tsv'), 'w', newline='') as file_path:
            tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
            for to_term in data_frame.db1_original_facts.terms.keys():
                tsv_writer.writerow([to_term])
        # write db2 terms
        with open(out_path.joinpath("Terms2").with_suffix('.tsv'), 'w', newline='') as file_path:
            tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
            for from_term in data_frame.db2_original_facts.terms.keys():
                tsv_writer.writerow([from_term])

# can be implemented faster, just replace db
    def merge_dbs(self,db1,db2):
        for file_name in db1.files.keys():
            records1 = db1.files[file_name].records
            records2 = db2.files[file_name].records
            bijected_db = set()
            target_db = set()
            target_db.update([tuple(record) for record in records2])
            for record1 in records1:
                bijected_record = []
                for term in record1:
                    if term in self.mapping:
                        bijected_record.append(self.mapping[term])
                    else:
                        # TODO: this should better be implemented in the mapping step
                        new_term = "new_var_" + str(self.new_term_counter)
                        #print("add new var: " + new_term + " for " + term)
                        self.mapping[term] = new_term  # introduce new variables
                        self.new_term_counter += 1
                        bijected_record.append(new_term)
                bijected_db.add(tuple(bijected_record))
            merged_records = []
            # atom wird hinzugefügt
            common_records = bijected_db.intersection(target_db)
            target_db = target_db.difference(common_records)
            bijected_db = bijected_db.difference(common_records)
            for record in common_records:
                merged_records.append(list(record) + ['0'])
            for record in bijected_db:
                merged_records.append(list(record) + ['1'])
            for record in target_db:
                merged_records.append(list(record) + ['10'])
            self.db2_merged_facts.insert_records(file_name, merged_records)

# from_db & to_db are objects of self.mapping, so setting them will modify self.mapping (since its pointers)
    # from_DB is usually db2 & to_db is db1
    def revert_db_mapping(self,from_db,to_db, from_identifier):

        pa_additionally_terms = set()
        for file_name,from_file_obj in from_db.files.items():
            inverted_records = []
            for from_record in from_file_obj.records:
                inverted_record = []
                # only reverse records that have the common_identifier (0) or the from_identifier (1/2)
                if from_record[-1] == '0' or from_record[-1] == str(from_identifier):
                    for from_term in from_record[0:-1]:
                        if from_term in self.mapping.inverse:
                            inverted_record.append(self.mapping.inverse[from_term])
                        else:
                            # this case means, that the Datalog-rules created new terms, which are not part of db1 yet
                            pa_additionally_terms.add(from_term)
                            inverted_record.append(from_term)
                    inverted_records.append(inverted_record)

            to_db.insert_records(file_name,inverted_records)

        # insert reverted records into DB
        to_db.write_data_to_file()
        # TODO this should be printed only once (as summary / abnormalties)
        if pa_additionally_terms:
            print("terms that have been added by datalog rules: " + str(len(pa_additionally_terms)))
            print(pa_additionally_terms)
        return

