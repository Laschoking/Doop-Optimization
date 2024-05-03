from enum import Enum
from pathlib import Path
from Python.Libraries.Path_Lib import *
from Python.Libraries import Shell_Lib
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
    def __init__(self,db_base_path,sub_dir):
        self.db_base_path = db_base_path
        self.name = db_base_path.stem + "-" + sub_dir
        self.path = db_base_path.joinpath(sub_dir)
        self.data = dict()
        Shell_Lib.clear_directory(self.path)


    def read_directory(self):
        for rel_path in self.path.glob("*"):
            file = rel_path.stem
            rows = []
            with open(rel_path, newline='') as db_file:
                tsv_file = csv.reader(db_file, delimiter='\t', quotechar='"')
                for row in tsv_file:
                    rows.append(tuple(row))
            self.insert_data(file, rows)

    def insert_data(self, file, rows):
        self.data[file] = [tuple(r) for r in rows]

    def write_data_to_file(self):
        for file in self.data:
            with open(self.path.joinpath(file).with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for row in self.data[file]:
                    tsv_writer.writerow(row)
class Data:
    def __init__(self, db1_base_path, db2_base_path):
        self.db1_facts =  DB_Instance(db1_base_path,"facts")
        self.db2_facts =  DB_Instance(db2_base_path,"facts")
        self.db1_pa_base = DB_Instance(db1_base_path, "pa_sep_base")
        self.db2_pa_base = DB_Instance(db2_base_path, "pa_sep_base")

        self.db2_merge_facts_bij = DB_Instance(db2_base_path, "merge_facts_bij")
        self.db2_merge_pa_bij = DB_Instance(db2_base_path, "merge_pa_bij")
        self.db2_merge_path_bij = db2_base_path.joinpath("merge_facts_bij")

        self.db1_pa_inv_bij = DB_Instance(db1_base_path, "bijected_pa_results")
        self.bijection = dict()
        #Base line case, that we only consider equal rows
        self.db2_merge_facts_base = DB_Instance(db2_base_path, "merge_facts_base")
        self.db2_merge_pa_base = DB_Instance(db2_base_path, "merge_pa_base")
        self.db2_merge_path_base = db2_base_path.joinpath("merge_facts_base")
    def update_bijection(self,bijection):
        self.bijection = bijection
def print_merge_information(analysis):
    print("----------- META INFORMATION -----------")
    print("Compared databases: " + analysis.db1.name + " , " + analysis.db2.name)
    print("Program analysis: " + analysis.pa_config.pa_name + " Engine: " + analysis.engine.name)
    print("------------------------")
