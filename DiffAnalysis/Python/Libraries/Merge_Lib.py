import os.path

import numpy as np
import csv
from prettytable import PrettyTable
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import Shell_Lib
from difflib import SequenceMatcher


def div_zero(n):
    return n if n != 0 else 10e9

'''
     - Assign the maximum value to each row_term if there are no conflicts 
     - a conflict (two row_terms have the same col_term target) is resolved by assigning the higher value (or if equal the first value)
     - iterating to resolve other conflict terms that did not get assigned yet
     - for each assignment (row_term, col_term) the corresponding column & row is masked 
'''
def find_best_bijection(ma_sim_matrix,row_terms,col_terms):
    bijection = {}
    conflict_table = PrettyTable()
    conflict_table.field_names = ["target_term", "possible source terms","similarity with target", "chosen source term"]
    count_iter = 0
    while(ma_sim_matrix.mask.all() == False and count_iter < 5):
        # find maximum value & index for each row
        max_each_row = ma_sim_matrix.argmax(axis=1)
        max_val_each_row = ma_sim_matrix.max(axis=1)

        row_it = 0
        conflict_table.clear_rows()
        conflict_rows = set()
        for row_nr in range(len(max_each_row)):
            max_col = max_each_row[row_nr]
            if max_val_each_row[row_nr] > 0 and row_it not in conflict_rows: # masked entries will be evaluated to 0 by default
                find_conflict_rows = np.where(max_each_row == max_col)[0]
                if len(find_conflict_rows) > 1:                              # conflicting assignments
                    vals = [max_val_each_row[a] for a in find_conflict_rows]  # all row_terms whose maximum is col_term
                    for a in find_conflict_rows: conflict_rows.add(a)       # record conflict (to avoid duplicate entries)
                    row = find_conflict_rows[np.argmax(vals)]         # choose row_term to max similarity cell (possibly further in the list)
                    conflict_table.add_row([col_terms[max_col],[row_terms[a] for a in find_conflict_rows],vals, row_terms[row]])
                    for a in find_conflict_rows: conflict_rows.add(a)
                else:                   # no conflicts, use current row_term
                    row = row_it
                row_term = row_terms[row]
                col_term = col_terms[max_col]
                bijection[row_term] = col_term

                # mask corresponding column & row (preserves indices for look up of term name)
                ma_sim_matrix[row, :] = np.ma.masked
                ma_sim_matrix[:,max_col] = np.ma.masked
            row_it += 1
        print(conflict_table)
        count_iter += 1

        print("current length of bijection: " + str(len(bijection)))
    return bijection

def similar_files_in_2dirs(dir1,dir2,target):
    file_pairs = []
    s_db1 = 0
    s_db2 = 0
    for rel1_path in dir1.path.glob("*"):
        rel_name = rel1_path.name
        rel2_path = dir2.path.joinpath(rel_name)
        if not rel2_path.exists():
            new_suffix = '.csv' if rel1_path.suffix == ".tsv" else '.tsv'
            rel2_path = rel2_path.with_suffix(new_suffix)
            if not rel2_path.exists():
                print(FileNotFoundError("Skipped file: " + str(rel2_path.stem)))
                continue
        s_rel1 = os.path.getsize(rel1_path)
        s_rel2 = os.path.getsize(rel2_path)

        if s_rel1 > 0 or s_rel2 > 0:
            s_db1 += s_rel1
            s_db2 += s_rel2
            file_pairs.append((rel1_path,rel2_path,target.joinpath(rel_name),rel_name))
    if s_db1 < s_db2:
        return file_pairs
    else:
        print("changed order of db1 and db2!")
        return [(rel2_path,rel1_path,merge_path,rel_name) for rel1_path,rel2_path,merge_path,rel_name in file_pairs]


def apply_bijection(file_pairs,bijection):
    merge_table = PrettyTable()
    merge_table.field_names = ["relation name","single rows from_terms","single rows to_terms","rows in common","percentage of common"]
    for from_path,to_path,merge_path,rel_name in file_pairs:
        with open(from_path, newline='') as f1, open(to_path, newline='') as f2, open(merge_path, 'w',
                                                                                newline='') as merge:
            merge_writer = csv.writer(merge, delimiter='\t',quoting=csv.QUOTE_NONE )# lineterminator='\n')
            f1_tsv = csv.reader(f1, delimiter='\t', quotechar='"')
            f2_tsv = csv.reader(f2, delimiter='\t', quotechar='"') # maybe read as string directly?
            bijected_db = set()
            old_db = set()
            target_db = set()
            target_db.update([tuple(row) for row in f2_tsv])
            for row in f1_tsv:
                bijected_row = []
                for term in row:
                    if term in bijection:
                        bijected_row.append(bijection[term])
                    else:
                        print("error no bijection found: " + term )
                        bijected_row.append(term)
                bijected_db.add(tuple(bijected_row))
            common_rows = bijected_db.intersection(target_db)
            target_db = target_db.difference(common_rows)
            bijected_db = bijected_db.difference(common_rows)
            for common_row in common_rows: merge_writer.writerow(common_row + (0,))
            for bijected_row in bijected_db: merge_writer.writerow(bijected_row + (1,))
            for target_row in target_db: merge_writer.writerow(target_row + (2,))
            l_bij = len(bijected_db)
            l_tar = len(target_db)
            l_comm = len(common_row)
            merge_table.add_row([rel_name,l_bij,l_tar,l_comm,str(round(100*l_comm/(l_bij+l_tar+l_comm),1)) + "%"])
    print(merge_table)

def revert_bijection(pa_dir,bijection):
    return

def calculate_pairwise_similarity(file_pairs):

    terms1 = set()
    terms2 = set()
    similarity_dict = {}
    # based on the path to the first relation, determine path to second relation
    for rel1_path,rel2_path,merge_path,rel_name in file_pairs:
        with open(rel1_path, newline='') as f1, open(rel2_path, newline='') as f2:
            f1_tsv = csv.reader(f1, delimiter='\t', quotechar='"')
            f2_tsv = csv.reader(f2, delimiter='\t', quotechar='"')
            f2_list = list(f2_tsv)
            for row1 in f1_tsv:
                for ind2 in range(len(f2_list)):
                    row2 = f2_list[ind2]
                    for i in range(len(row1)):
                        term1 = row1[i]
                        term2 = row2[i]
                        terms1.add(term1)
                        terms2.add(term2)
                        if (term1, term2) not in similarity_dict:
                            #currently only accepts positive integers due to isdigit()
                            if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
                                max_int = max(int(term1), int(term2))
                                if max_int > 0:
                                    sim = 1 - abs(int(term1) - int(term2)) / max_int
                                else:
                                    sim = 1
                            else:
                                sim = SequenceMatcher(None, term1, term2).ratio()

                            similarity_dict[(term1,term2)] = sim
    return similarity_dict

def create_sim_matrix(similarity_dict):
    # the lists are link the sim_matrix indices to the names of the terms
    term1_list = []
    term2_list = []
    for (term1,term2) in similarity_dict:
        if term1 not in term1_list: term1_list.append(term1)
        if term2 not in term2_list: term2_list.append(term2)


    sim_matrix = np.zeros(shape=(len(term1_list) ,len(term2_list)))
    for (term1,term2) in similarity_dict:
        term1_ind = term1_list.index(term1)
        term2_ind = term2_list.index(term2)
        sim_matrix[term1_ind][term2_ind] = similarity_dict[term1, term2]
    # mask all combinations that have not been calculated (they did never appear in the same column of an atom)
    ma_sim_matrix = np.ma.masked_equal(sim_matrix,0)
    return ma_sim_matrix,term1_list,term2_list



def forward_bijection(merge_class, write_flag, debug_flag):
    # create some variables for general db-stats
    dir1 = merge_class.dir1
    dir2 = merge_class.dir2
    # similar_files will swap the order of both directories, if db1 > db2
    # we want the smaller db to be at the y-axis (rows) and bigger db ath x-axis (columns)
    # because we biject fromt the smaller db to the bigger db
    file_pairs = similar_files_in_2dirs(dir1,dir2,merge_class.merge_dir.path)
    sim_dictionary = calculate_pairwise_similarity(file_pairs)
    ma_sim_matrix,term1_list,term2_list = create_sim_matrix(sim_dictionary)
    
    bijection = find_best_bijection(ma_sim_matrix, term1_list, term2_list)
    apply_bijection(file_pairs, bijection)

    return file_pairs,bijection



def print_nemo_runtime(runtime,PA_name):
    t = PrettyTable()
    t.field_names = ["Program Analysis","DB", "Total Reasoning", "Loading Input","Reasoning","Saving Output"]
    for r in runtime:
        t.add_row([PA_name] + r)
    print(t)


def print_merge_stats(merge_class,db1_name, db2_name, merge_type):
    dir1 = merge_class.dir1
    dir2 = merge_class.dir2
    common_dir = merge_class.common_dir
    merge_dir = merge_class.merge_dir
    sum_nr_rows = dir1.nr_rows + dir2.nr_rows
    sum_nr_chars = dir1.nr_chars + dir2.nr_chars
    sum_size = dir1.size + dir2.size
    avg_col_size = merge_class.nr_cols / max(dir1.nr_filled_rel, dir2.nr_filled_rel)
    t = PrettyTable()
    t.field_names = ["DB", "rows", "row save ", "chars in k", "char save", "size in kb", "size save"]
    t.add_row(["Common", common_dir.nr_rows, "",
               round(common_dir.nr_chars / 1000, 1), "", "", ""])

    t.add_row([db1_name, dir1.nr_rows, "", round(dir1.nr_chars / 1000, 1),
               "", round(dir1.size >> 10, 3), ""])
    t.add_row([db2_name, dir2.nr_rows, ""
                  , round(dir2.nr_chars / 1000, 1),
               "", round(dir2.size >> 10, 3), ""])

    t.add_row(["Sum(DB1,DB2)", sum_nr_rows, "",
               round(sum_nr_chars / 1000, 1),
               "", round(sum_size >> 10, 3), ""])

    t.add_row(["Merge", merge_dir.nr_rows, str(round(100 * merge_dir.nr_rows / sum_nr_rows - 100, 1)) + "%",
               round(merge_dir.nr_chars / 1000, 1),
               str(round(100 * merge_dir.nr_chars / sum_nr_chars - 100, 1)) + "%", round(merge_dir.size >> 10, 3),
               str(round(100 * merge_dir.size / sum_size - 100, 1)) + "%"])

    # print fact stats
    print("----------- " + merge_type + " -----------")
    print("dir1: " + str(dir1.path)[len(base_dir):])
    print("non-empty relations in DB1: " + str(dir1.nr_filled_rel))
    print("dir2: " + str(dir2.path)[len(base_dir):])
    print("non-empty relations in DB2: " + str(dir2.nr_filled_rel))
    print("compared relations:       " + str(len(dir2.relation_list)))
    print("average column size: " + str(round(avg_col_size, 2)))
    print("Database Similarity: " + str(round(100 * 2 * common_dir.nr_rows / (dir1.nr_rows + dir2.nr_rows), 1)) + "%")

    print(t)

