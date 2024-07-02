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
        self.terms = dict()
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
                    rows.append(row)
            self.insert_records(file, rows)

    def insert_records(self, file, rows):
        if file not in self.files:
            l_cols = len(rows[0]) if len(rows) > 0 else 0
            self.files[file] = l_cols
            self.data_rows[file] = []
        row_nr = len(self.data_rows[file])

        # nur für db1-facts & db2-facts benötigt
        #create a list of sets (one for each column)
        for row in rows:
            self.data_rows[file].append(row)
            for col_nr in range(l_cols):
                if not row:
                    raise ValueError("empty row detected in mapped db: " + str(file))
                term = row[col_nr]
                if term in self.terms:
                    self.terms[term][(file,col_nr)] = row_nr
                else:
                    self.terms[term] = {(file, col_nr) :  row_nr }
            row_nr += 1
        return


    def write_data_to_file(self):
        for file in self.data_rows:
            with open(self.path.joinpath(file).with_suffix('.tsv'), 'w', newline='') as file_path:
                tsv_writer = csv.writer(file_path, delimiter='\t', lineterminator='\n')
                for row in self.data_rows[file]:
                    tsv_writer.writerow(row)
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

