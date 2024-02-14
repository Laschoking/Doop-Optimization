import csv
import shutil

from Path_Lib import *
from prettytable import PrettyTable
class Table:
    def __init__(self,nr):
        self.id_nr = nr
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0

class Relation:
    def __init__(self,path,nr):
        self.path = path
        self.id_nr = nr
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0
        self.rows = set()

class RelationClass:
    def __init__(self,merge_path,rel1,id_1,rel2,id_2,common_nr):
        self.rel1 = Relation(rel1,id_1)
        self.rel2 = Relation(rel2,id_2)
        self.merge = Relation(merge_path,-1)
        self.common = Table(common_nr)
        self.nr_cols = 0

class Directory:
    def __init__(self,dir_path):
        self.path = dir_path
        self.nr_filled_rel = 0
        self.nr_rows = 0
        self.nr_entries = 0
        self.nr_chars = 0
        self.size = 0
        self.relation_list = []

    def update(self,rel) -> Relation:
        self.nr_rows += rel.nr_rows
        self.nr_entries += rel.nr_entries
        self.nr_chars += rel.nr_chars
        self.size += rel.size
        self.nr_filled_rel += 1 if rel.nr_rows > 0 else 0


    def add_relation(self, relation) -> Relation:
        self.relation_list.append(relation)


class DirectoryClass:
    def __init__(self,merge_dir,dir1, dir2, common_dir):
        self.merge_dir = merge_dir
        self.dir1 = dir1
        self.dir2 = dir2
        self.common_dir = common_dir
        self.nr_cols = 0


    def add_relation(self,rel_class) -> RelationClass:
        self.dir1.add_relation(rel_class.rel1)
        self.dir2.add_relation(rel_class.rel2)
        self.common_dir.add_relation(rel_class.common)


def divZero(n):
    return n if n != 0 else 10e9

def merge_relations(rel_class,write_flag,split_flag):
    with open(rel_class.rel1.path) as f1, open(rel_class.rel2.path) as f2, open(rel_class.merge.path, 'w', newline='') as merge:
        merge_writer = csv.writer(merge, delimiter= '\t', lineterminator='\n')
        nr_cols = 0
        r1 = set(map(str.rstrip, f1))
        r2 = set(map(str.rstrip, f2))

        # remove the last line of each entry -> allows to compare the results without the decuted side (0,1,10)
        if split_flag:
            for r,rel in [r1,rel_class.rel1] ,[r2,rel_class.rel2]:
                for row in r:
                    rel.rows.add("\t".join(row.split('\t')[:-1]))
        else:
            rel_class.rel1.rows = r1
            rel_class.rel2.rows = r2


        rel_class.common.rows = rel_class.rel1.rows.intersection(rel_class.rel2.rows)
        rel_class.common.nr_rows = len(rel_class.common.rows)

        for rel in [rel_class.rel1,rel_class.rel2]:
            rel.nr_rows = len(rel.rows)

            # find relations, that are only in one file and add specific id
            for diff_rel in rel.rows.difference(rel_class.common.rows):
                #if str(rel.path).__contains__("Method_ParamTypes"):
                #    print("t")
                rel.nr_chars += len(diff_rel)
                rel_class.merge.nr_chars += len(diff_rel) + len(str(rel_class.common.id_nr))  # for additional lenght of id
                #print(rel.path)
                #print(diff_rel)
                diff_rel = diff_rel.split('\t')
                diff_rel.append(rel.id_nr)
                rel_class.merge.nr_chars += len(diff_rel)
                if write_flag : merge_writer.writerow(diff_rel)

            if rel.nr_rows > 0:
                nr_cols = len(rel.rows.pop().split('\t'))
            rel.nr_entries = rel.nr_rows * nr_cols
            rel.size = rel.path.stat().st_size

        # find facts, that are in both files & add with specific id
        for common_entries in rel_class.common.rows:
            rel_class.common.nr_chars += len(common_entries)
            rel_class.merge.nr_chars += len(common_entries) + len(str(rel_class.common.id_nr)) # for additional lenght of id
            common_entries = common_entries.split('\t')
            common_entries.append(rel_class.common.id_nr)
            if write_flag : merge_writer.writerow(common_entries)
        if nr_cols == 0 and rel_class.common.nr_rows > 0:
            nr_cols = len(rel_class.common.rows.pop().split('\t'))

        rel_class.rel1.nr_chars += rel_class.common.nr_chars
        rel_class.rel2.nr_chars += rel_class.common.nr_chars
        rel_class.common.nr_entries = rel_class.common.nr_rows * nr_cols
        rel_class.nr_cols = nr_cols
    rel_class.merge.nr_rows = rel_class.rel1.nr_rows + rel_class.rel2.nr_rows - rel_class.common.nr_rows
    rel_class.merge.nr_entries = rel_class.merge.nr_rows * (nr_cols + 1)

    # get file size after merge-file is closed
    rel_class.merge.size = rel_class.merge.path.stat().st_size

def merge_directories(dir1_path, dir2_path, merge_dir_path, merge_type,summary_file,write_flag,split_flag):
    # create some variables for general db-stats
    dir1 = Directory(dir1_path)
    dir2 = Directory(dir2_path)
    common_dir = Directory("")
    merge_dir = Directory(merge_dir_path)

    dir_class = DirectoryClass(merge_dir, dir1, dir2,common_dir)

    # based on the path to the first relation, determine path to second relation
    for rel1_path in dir1.path.glob("*"):
        rel_name = Path(rel1_path).name
        if rel_name == "Method_Descriptor.tsv" or rel_name == "MainClass.tsv":
            continue
        rel2_path = Path.joinpath(dir2.path, rel_name)
        merge_rel_path = Path.joinpath(merge_dir.path, rel_name)

        rel_class = RelationClass(merge_rel_path, rel1_path, 1, rel2_path, 10, 0)
        dir_class.add_relation(rel_class)
        merge_relations(rel_class,write_flag,split_flag)
        dir1.update(rel_class.rel1)
        dir2.update(rel_class.rel2)
        common_dir.update(rel_class.common)
        merge_dir.update(rel_class.merge)
        dir_class.nr_cols += rel_class.nr_cols

    sum_nr_rows = dir1.nr_rows + dir2.nr_rows
    sum_nr_chars = dir1.nr_chars + dir2.nr_chars
    sum_size = dir1.size + dir2.size
    avg_col_size = dir_class.nr_cols / max(dir1.nr_filled_rel, dir2.nr_filled_rel)


    t = PrettyTable()
    t.field_names = ["DB","rows","row save ", "chars in k", "char save", "size in kb","size save"]
    t.add_row(["Common", common_dir.nr_rows,"",
               round(common_dir.nr_chars/1000,1),"","",""])

    t.add_row(["Db1", dir1.nr_rows,"", round((dir1.nr_chars)/1000,1),
               "",round(dir1.size >> 10, 3),""])
# str(round(100 * common_dir.nr_rows/dir2.nr_rows, 1)) + ")%"
    t.add_row(["Db2", dir2.nr_rows,""
               , round((dir2.nr_chars)/1000,1),
               "",round(dir2.size >> 10, 3),""])

    t.add_row(["Sum(DB1,DB2)",sum_nr_rows,"",
               round(sum_nr_chars /1000,1),
               "",round(sum_size >> 10, 3),""])

    t.add_row(["Merge",merge_dir.nr_rows,  str(round(100 * merge_dir.nr_rows/sum_nr_rows -100,1)) + "%",
               round(merge_dir.nr_chars/1000,1),
               str(round(100 * merge_dir.nr_chars / sum_nr_chars -100,1))+ "%", round(merge_dir.size >> 10,3),  str(round( 100 * merge_dir.size/sum_size - 100, 1)) + "%"])

    # print fact stats
    print("----------- " + merge_type + " SUMMARY-----------")
    print("---database---")
    print("dir1: " + str(dir1.path))
    print("relations in each DB:       " + str(len(dir1.relation_list)))
    print("non-empty relations in DB1: " + str(dir1.nr_filled_rel))
    print("dir2: " + str(dir2.path))
    print("non-empty relations in DB2: " + str(dir2.nr_filled_rel))
    print("average column size: " + str(round(avg_col_size,2)))
    print("Database Similarity: " + str(round(100 * 2 * common_dir.nr_rows / (dir1.nr_rows + dir2.nr_rows),1)) + "%")
    print("--- ---")

    print(t)

