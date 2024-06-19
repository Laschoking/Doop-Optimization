from enum import Enum
from pathlib import Path
from Python.Libraries.PathLib import *
from Python.Libraries import ShellLib
import csv


class Config:
    def __init__(self, class_name, db1_name, db2_name, pa_name):
        self.class_name = class_name
        self.base_output_path = base_out_path.joinpath(pa_name + "_" + db1_name + "_" + db2_name)
        self.db1_name = db1_name
        self.db2_name = db2_name
        self.db1_path = self.base_output_path.joinpath(db1_name)
        self.db2_path = self.base_output_path.joinpath(db2_name)
        self.pa_name = pa_name

class DB_Instance:
    def __init__(self,db_base_path, sub_dir):
        self.db_base_path = db_base_path
        self.name = db_base_path.stem + "-" + sub_dir
        self.path = db_base_path.joinpath(sub_dir)
        self.data_rows = dict()
        self.data_cols = dict()
        self.files = dict()

        # delete existing files in sub_dir
        ShellLib.clear_directory(self.path)


    def read_directory(self):
        for rel_path in self.path.glob("*"):
            file = rel_path.stem
            rows = []
            with open(rel_path, newline='') as db_file:
                tsv_file = csv.reader(db_file, delimiter='\t', quotechar='"')
                for row in tsv_file:
                    rows.append(tuple(row))
            self.insert_records(file, rows)

    def insert_records(self, file, rows):
        if file not in self.files:
            l_cols = len(rows[0]) if rows else 0
            self.files[file] = l_cols
            self.data_cols[file] = [set() for i in range(l_cols)]
            self.data_rows[file] = set()

        #create a list of sets (one for each column)
        for row in rows:
            self.data_rows[file].add(tuple(row))

            for ind in range(l_cols):
                self.data_cols[file][ind].add(row[ind])


    def write_data_to_file(self):
        for file in self.data_rows:
            with open(self.path.joinpath(file).with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for row in self.data_rows[file]:
                    tsv_writer.writerow(row)


class Bijection:
    def __init__(self, paths,name):
        self.name = name
        self.db2_merged_facts = DB_Instance(paths.db2_facts, name)
        self.db2_nemo_merged_results = DB_Instance(paths.db2_results, name)

        self.db1_inv_bij_results = DB_Instance(paths.db1_results, name)
        self.similarity_dict = dict()
        self.mapping = dict()

    def set_mapping(self, mapping):
        self.mapping = mapping

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

        self.bijections = []
    def add_bijection(self, bijection):
        self.bijections.append(bijection)
def print_merge_information(analysis):
    print("----------- META INFORMATION -----------")
    print("Compared databases: " + analysis.db1.name + " , " + analysis.db2.name)
    print("Program analysis: " + analysis.pa_config.pa_name + " Engine: " + analysis.engine.name)
    print("------------------------")
