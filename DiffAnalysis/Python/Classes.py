from enum import Enum
from pathlib import Path

# This file defines all necessary paths for the comparison pipeline

# create path to doop base and its output dir
DOOP_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/"
DOOP_OUT_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/out/"
NEMO_ENGINE_PATH = "/home/kotname/Documents/Diplom/Code/nemo/nemo"

#

# this path will be the base for all of our file manipulation
base_diff_path = Path("/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis")
base_out_path = base_diff_path.joinpath("out")
java_source_dir = base_diff_path.joinpath("Java")

SOUFFLE_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_souffle/Analysis")
NEMO_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/Analysis")

Engine = Enum("Engine",["SOUFFLE", "NEMO"])


class Config:
    def __init__(self, class_name, db1_name, db2_name, pa_name, souffle_sep_name, souffle_merge_name, nemo_sep_name,
                 nemo_merge_name):
        self.class_name = class_name
        self.base_output_path = base_out_path.joinpath(pa_name + "_" + db1_name + "_" + db2_name)
        self.db1_name = db1_name
        self.db2_name = db2_name
        self.db1_path = self.base_output_path.joinpath(db1_name)
        self.db2_path = self.base_output_path.joinpath(db2_name)
        self.pa_name = pa_name

        self.souffle_sep_name = souffle_sep_name
        self.souffle_merge_name = souffle_merge_name
        self.souffle_sep_path = Path.joinpath(SOUFFLE_BASE, souffle_sep_name)
        self.souffle_merge_path = Path.joinpath(SOUFFLE_BASE, souffle_merge_name)

        self.nemo_sep_name = nemo_sep_name
        self.nemo_merge_name = nemo_merge_name
        self.nemo_sep_path = Path.joinpath(NEMO_BASE, nemo_sep_name)
        self.nemo_merge_path = Path.joinpath(NEMO_BASE, nemo_merge_name)


class Table:
    def __init__(self, nr):
        self.id_nr = nr
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0


class Relation:
    def __init__(self, path, nr):
        self.path = path
        self.id_nr = nr
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0
        self.rows = set()


class RelationClass:
    def __init__(self, merge_path, rel1, id_1, rel2, id_2, common_nr):
        self.rel1 = Relation(rel1, id_1)
        self.rel2 = Relation(rel2, id_2)
        self.merge = Relation(merge_path, -1)
        self.common = Table(common_nr)
        self.nr_cols = 0


class Directory:
    def __init__(self, dir_path):
        self.path = dir_path
        self.nr_filled_rel = 0
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0
        self.relation_list = []

    def update(self, rel):
        self.nr_rows += rel.nr_rows
        self.nr_entries += rel.nr_entries
        self.nr_chars += rel.nr_chars
        self.size += rel.size
        self.nr_filled_rel += 1 if rel.nr_rows > 0 else 0

    def add_relation(self, relation):
        self.relation_list.append(relation)


class MergeClass:
    def __init__(self, db1_path, db2_path, merge_path, summary_path):
        self.db1_path = db1_path
        self.db2_path = db2_path
        self.merge_path = merge_path
        self.summary_path = summary_path

        self.dir1 = Directory(db1_path)
        self.dir2 = Directory(db2_path)
        self.common_dir = Directory("")
        self.merge_dir = Directory(merge_path)
        self.nr_cols = 0

    def add_relation(self, rel_class):
        self.dir1.add_relation(rel_class.rel1)
        self.dir2.add_relation(rel_class.rel2)
        self.common_dir.add_relation(rel_class.common)


def print_merge_information(analysis):
    print("----------- META INFORMATION -----------")
    print("Compared databases: " + analysis.db1.name + " , " + analysis.db2.name)
    print("Program analysis: " + analysis.pa_config.pa_name + " Engine: " + analysis.engine.name)
    print("------------------------")
