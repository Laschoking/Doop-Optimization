from enum import Enum
from pathlib import Path
from Python.Libraries import PathLib
from Python.Libraries import ShellLib
from sortedcontainers import SortedList,SortedDict

import csv


class Config:
    def __init__(self, dir_name, db1_name, db2_name):
        self.dir_name = dir_name
        self.base_output_path = PathLib.base_out_path.joinpath(dir_name).joinpath(db1_name + "_" + db2_name)
        self.db1_name = db1_name
        self.db2_name = db2_name
        self.db1_path = self.base_output_path.joinpath(db1_name)
        self.db2_path = self.base_output_path.joinpath(db2_name)

class Term:
    def __init__(self, term_name):
        self.name = term_name
        self.occurrence = dict()
        self.type = "int" if term_name.lstrip("-").isdigit() else "string"
        self.degree = 0

    # one occurence has the following structure: file_name,col_nr,row_nr
    # the collection is of following structure {(file_name,col_nr) : [row_nr1,row_nr2, ...]}
    # this way, all row_nr are stored together, but with file_name,col_nr as keys
    # those keys can be used for later set-operations while mapping
    def add_occurence(self,file_name,col_nr,row_nr):
        key = (file_name,col_nr)
        if key in self.occurrence:
            self.occurrence[key].append(row_nr)
        else:
            self.occurrence[key] = [row_nr]
        self.degree += 1


class File:
    def __init__(self,file_name,col_size):
        self.name = file_name
        self.col_size = col_size
        self.records = []
        self.record_count = 0

    def incr_record_count(self):
        self.record_count += 1

class DB_Instance:
    def __init__(self,db_base_path, sub_dir):
        self.db_base_path = db_base_path
        self.name = db_base_path.stem + "-" + sub_dir
        self.path = db_base_path.joinpath(sub_dir)
        self.terms = dict()
        self.files = dict() # file : file_object
        # delete existing files in sub_dir
        ShellLib.clear_directory(self.path)


    def read_directory(self):
        for rel_path in self.path.glob("*"):
            file = rel_path.stem
            records = []
            with open(rel_path, newline='') as db_file:
                tsv_file = csv.reader(db_file, delimiter='\t', quotechar='"')
                for record in tsv_file:
                    records.append(record)
            self.insert_records(file, records)

    def insert_records(self, file_name, records):
        if file_name not in self.files:
            l_cols = len(records[0]) if len(records) > 0 else 0
            file_obj = File(file_name, l_cols)
            self.files[file_name] = file_obj
        else:
            file_obj = self.files[file_name]

        # nur für db1-facts & db2-facts benötigt
        #create a list of sets (one for each column)
        for record in records:
            file_obj.records.append(record)
            for col_nr in range(file_obj.col_size):
                if not record:
                    raise ValueError("empty record detected in mapped db: " + file_name)
                term_name = record[col_nr]

                if term_name in self.terms:
                    # retrieve object
                    term_obj = self.terms[term_name]
                else:
                    # create new entry for this term
                    term_obj = Term(term_name)
                    self.terms[term_name] = term_obj

                term_obj.add_occurence(file_name, col_nr, file_obj.record_count)

            file_obj.incr_record_count()
        return


    def write_data_to_file(self):
        for file_name,file_obj in self.files.items():
            with open(self.path.joinpath(file_name).with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for record in file_obj.records:
                    tsv_writer.writerow(record)
class BasePaths:
    def __init__(self,db1_base_path, db2_base_path):
        self.db1_facts = db1_base_path.joinpath("facts")
        self.db2_facts = db2_base_path.joinpath("facts")
        self.db1_results = db1_base_path.joinpath("results")
        self.db2_results = db2_base_path.joinpath("results")


class DataFrame:
    def __init__(self, db1_base_path, db2_base_path):
        self.paths = BasePaths(db1_base_path, db2_base_path)
        # origin of the facts for both databases

        self.db1_original_facts = DB_Instance(self.paths.db1_facts, "db1-original")
        self.db2_original_facts = DB_Instance(self.paths.db2_facts, "db2-original")

        # origin for separate Program Analysis without Bijection
        self.db1_original_results = DB_Instance(self.paths.db1_results, "db1-original")
        self.db2_original_results = DB_Instance(self.paths.db2_results, "db2-original")


        self.terms1 = dict()
        self.terms2 = dict()
        self.mappings = []

    def add_mapping(self, mapping):
        self.mappings.append(mapping)

