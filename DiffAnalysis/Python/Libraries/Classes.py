from enum import Enum
from pathlib import Path

import pandas as pd

from Python.Libraries import PathLib
from Python.Libraries import ShellLib
from sortedcontainers import SortedList,SortedDict

import csv
from collections import Counter
import os

class Term:
    def __init__(self, term_name, file_name,col_ind,row_ind):
        self.name = term_name
        self.occurrence = dict()
        self.occurrence_c = Counter()
        self.type = "int" if type(term_name) is int else "string"
        self.degree = 0

        self.update(file_name,col_ind,row_ind)

    # one occurence has the following structure: file_name,col_nr,row_nr
    # the collection is of following structure {(file_name,col_nr) : [row_nr1,row_nr2, ...]}
    # this way, all row_nr are stored together, but with file_name,col_nr as keys
    # those keys can be used for later set-operations while mapping
    def update(self,file_name,col_nr,row_nr):
        key = (file_name,col_nr)
        self.occurrence_c.update([key])
        if key in self.occurrence:
            self.occurrence[key].append(row_nr)
        else:
            self.occurrence[key] = [row_nr]
        self.degree += 1


class DB_Instance:
    def __init__(self,db_base_path, sub_dir):
        self.db_base_path = db_base_path
        self.name = db_base_path.stem + "-" + sub_dir
        self.path = db_base_path.joinpath(sub_dir)
        self.files = dict()

        #ShellLib.clear_directory(self.path)


    def read_db_relations(self):
        if not self.path.is_dir():
            raise FileNotFoundError("Directory does not exist: " + str(self.path))
        for rel_path in self.path.glob("*"):
            file_name = rel_path.stem
            if os.stat(rel_path).st_size == 0:
                df = pd.DataFrame()
            else:
                df = pd.read_csv(rel_path,sep='\t', keep_default_na=False,dtype='string',header=None,on_bad_lines='warn')
            self.insert_df(file_name,df)



    def insert_df(self, file_name, df):
        self.files[file_name] = df



    def log_db_relations(self):
        ShellLib.clear_directory(self.path)
        for file_name,df in self.files.items():
            df.to_csv(self.path.joinpath(file_name).with_suffix('.tsv'),sep="\t",index=False,header=False)

class BasePaths:
    def __init__(self,base_output_path,db1_base_path, db2_base_path):
        self.db1_facts = db1_base_path.joinpath("facts")
        self.db2_facts = db2_base_path.joinpath("facts")
        self.db1_results = db1_base_path.joinpath("results")
        self.db2_results = db2_base_path.joinpath("results")
        self.merge_facts = base_output_path.joinpath("merge_db").joinpath("facts")
        self.merge_results = base_output_path.joinpath("merge_db").joinpath("results")
        self.mapping_results = base_output_path.joinpath("mappings")
        self.terms1 = base_output_path.joinpath("Terms1.tsv")
        self.terms2 = base_output_path.joinpath("Terms2.tsv")
        self.global_log = PathLib.base_out_path.joinpath("Results")

class DataBag:
    def __init__(self, base_output_path, db1_base_path, db2_base_path):
        self.paths = BasePaths(base_output_path,db1_base_path, db2_base_path)
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

    def read_terms_from_db(self,terms, db_instance):
        for file_name, df in db_instance.files.items():
            for row_ind, row in df.iterrows():
                for col_ind, term in row.items():
                    if term in terms:
                        terms[term].update(file_name, col_ind,row_ind)
                    else:
                        terms[term] = Term(term, file_name,col_ind,row_ind)
        return terms

    def log_terms(self):
        terms1_df = pd.Series(self.terms1.keys())
        if not self.paths.terms1.exists():
            terms1_df.to_csv(self.paths.terms1,sep='\t',index=False,header=False)

        terms2_df = pd.Series(self.terms2.keys())
        if not self.paths.terms2.exists():
            terms2_df.to_csv(self.paths.terms2,sep='\t',index=False,header=False)




