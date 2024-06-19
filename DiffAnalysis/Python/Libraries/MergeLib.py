import os.path
import sys
import numpy as np
import csv
from prettytable import PrettyTable
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import ShellLib

'''def merge_original_facts(data_frame):
    # merge atoms that are equal
    # TODO: ist doch super weird zeilenweise zu mergen, d.h. manchmal wird Term1 auf T2 abgebildet & manchmal nicht

    for file in data_frame.db1_facts.files:
        rows = []
        rows1 = set(data_frame.db1_facts.data_rows[file])
        rows2 = set(data_frame.db2_facts.data_rows[file])
        inters = rows1.intersection(rows2)
        for row in inters:
            rows.append(row + ('0',))
        for row in rows1.difference(rows2):
            rows.append(row + ('1',))
        for row in rows2.difference(rows1):
            rows.append(row + ('10',))
        data_frame.db2_merge_facts_base.insert_records(file, rows)
    data_frame.db2_merge_facts_base.write_data_to_file()
'''


def create_sim_matrix(similarity_dict):
    # the lists are link the sim_matrix indices to the names of the terms
    term1_list = []
    term2_list = []
    for (term1, term2) in similarity_dict:
        if term1 not in term1_list: term1_list.append(term1)
        if term2 not in term2_list: term2_list.append(term2)

    sim_matrix = np.zeros(shape=(len(term1_list), len(term2_list)))
    for (term1, term2) in similarity_dict:
        term1_ind = term1_list.index(term1)
        term2_ind = term2_list.index(term2)
        sim_matrix[term1_ind][term2_ind] = similarity_dict[term1, term2]
    # mask all combinations that have not been calculated (they did never appear in the same column of an atom)
    ma_sim_matrix = np.ma.masked_equal(sim_matrix, 0)
    if ma_sim_matrix.size == 0:
        e = ValueError("the Similarity Matrix is empty!")
        sys.exit(str(e))
    return ma_sim_matrix, term1_list, term2_list


def compute_optimal_mapping(ma_sim_matrix, row_terms, col_terms):
    bijection = {}
    conflict_table = PrettyTable()
    conflict_table.field_names = ["target_term", "possible source terms", "similarity with target",
                                  "chosen source term"]
    count_iter = 0
    while (ma_sim_matrix.mask.all() == False and count_iter < 5):
        # find maximum value & index for each row
        max_each_row = ma_sim_matrix.argmax(axis=1)
        max_val_each_row = ma_sim_matrix.max(axis=1)

        row_it = 0
        conflict_table.clear_rows()
        conflict_rows = set()
        for row_nr in range(len(max_each_row)):
            max_col = max_each_row[row_nr]
            if max_val_each_row[
                row_nr] > 0 and row_it not in conflict_rows:  # masked entries will be evaluated to 0 by default
                find_conflict_rows = np.where(max_each_row == max_col)[0]
                if len(find_conflict_rows) > 1:  # conflicting assignments
                    vals = [max_val_each_row[a] for a in find_conflict_rows]  # all row_terms whose maximum is col_term
                    for a in find_conflict_rows: conflict_rows.add(a)  # record conflict (to avoid duplicate entries)
                    row = find_conflict_rows[
                        np.argmax(vals)]  # choose row_term to max similarity cell (possibly further in the list)
                    conflict_table.add_row(
                        [col_terms[max_col], [row_terms[a] for a in find_conflict_rows], vals, row_terms[row]])
                    for a in find_conflict_rows: conflict_rows.add(a)
                else:  # no conflicts, use current row_term
                    row = row_it
                row_term = row_terms[row]
                col_term = col_terms[max_col]
                bijection[row_term] = col_term

                # mask corresponding column & row (preserves indices for look up of term name)
                ma_sim_matrix[row, :] = np.ma.masked
                ma_sim_matrix[:, max_col] = np.ma.masked
            row_it += 1
        # print(conflict_table)
        count_iter += 1

    return bijection


def apply_mapping_and_merge_dbs(data_frame,bijection):
    new_var_counter = 0
    for file in data_frame.db1_original_facts.files:
        rows1 = data_frame.db1_original_facts.data_rows[file]
        rows2 = data_frame.db2_original_facts.data_rows[file]
        bijected_db = set()
        target_db = set()
        target_db.update([tuple(row) for row in rows2])
        for row1 in rows1:
            bijected_row = []
            for term in row1:
                if term in bijection.mapping:
                    bijected_row.append(bijection.mapping[term])
                else:
                    new_term = "new_var_" + str(new_var_counter)
                    bijection.mapping[term] = new_term  # introduce new variables
                    new_var_counter += 1
                    bijected_row.append(new_term)
            bijected_db.add(tuple(bijected_row))
        merged_rows = []
        common_rows = bijected_db.intersection(target_db)
        target_db = target_db.difference(common_rows)
        bijected_db = bijected_db.difference(common_rows)
        for row in common_rows:
            merged_rows.append(row + ('0',))
        for row in bijected_db:
            merged_rows.append(row + ('1',))
        for row in target_db:
            merged_rows.append(row + ('10',))
        bijection.db2_merged_facts.insert_records(file, merged_rows)


def inverse_bijection(from_merged_db, to_bijected_db, bijection, from_identifier):
    inv_bijection = dict((term2, term1) for term1, term2 in bijection.items())
    for file in from_merged_db.files:
        db1_bij_rows = []
        for row2 in from_merged_db.data_rows[file]:
            # only reverse rows that have the common_identifier (0) or the from_identifier (1/2)
            if row2[-1] == '0' or row2[-1] == str(from_identifier):
                db1_bij_row = []
                for term2 in row2[0:-1]:
                    if term2 in inv_bijection:
                        db1_bij_row.append(inv_bijection[term2])
                        # neuen eintrag
                    else:
                        # since there is no matching, but the term belongs to db1 its value was copied directly
                        # this happens if constants have been introduced in the PA
                        # print("no inverse bijection found for this term: " + term2 )
                        db1_bij_row.append(term2)
                db1_bij_rows.append(db1_bij_row)
        to_bijected_db.insert_records(file, db1_bij_rows)
    # return to_bijected_db


def diff_two_dirs(db_inst1, db_inst2, rm_identifier='', print_flag=True):
    t = PrettyTable()
    #if db_inst1.name == db_inst2.name:
    #    print(db_inst1.name)
    #    return
    t.field_names = ["file name", db_inst1.name, db_inst2.name, "common rows", "overlap in %"]
    t.sortby = "common rows"
    l_inters_files = 0
    l_rows1_files = 0
    l_rows2_files = 0
    file_count = len(db_inst1.files)
    div = False
    for file in db_inst1.files:
        file_count -= 1
        if file not in db_inst2.files:
            print("file was not compared: " + file)
            continue
        rows1 = set(db_inst1.data_rows[file])
        rows2 = set()
        # in case, one db still has identifiers appended (like ["a","b", 0], remove
        if rm_identifier != '':
            for x in db_inst2.data_rows[file]:
                # remove only common identifier & from correct side (dont consider rows that come from the other db)
                if x[-1] == rm_identifier or x[-1] == '0':
                    rows2.add(x[:-1])
        else:
            rows2 = set(db_inst2.data_rows[file])

        inters = rows1.intersection(rows2)
        unique_rows1 = rows1.difference(rows2)
        unique_rows2 = rows2.difference(rows1)
        l_inters = len(inters)
        l_rows1 = len(unique_rows1)
        l_rows2 = len(unique_rows2)
        if l_rows1 + l_rows2 + l_inters == 0: continue
        l_rows1_files += l_rows1
        l_rows2_files += l_rows2
        l_inters_files += l_inters
        cov = round(100 * l_inters / (l_rows1 + l_rows2 + l_inters))
        if cov != 100:
            r = [file, l_rows1, l_rows2, l_inters, str(cov) + "%"]
            t.add_row(r,divider=div)
    #t.add_row(['','','','',''],divider=True)
    t.add_row(["SUMMARY", l_rows1_files , l_rows2_files , l_inters_files,
               str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files))) + "%"])
    if (l_rows1_files > 0 or l_rows2_files > 0) and print_flag:
        print(t)
    # we return the nr. of rows for db1, db2, their intersection, and the overlap (inters/ (sum))
    return [l_rows1_files, l_rows2_files, l_inters_files,
            str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files), 1))]


def check_data_correctness(data_frame, bijection):
    t = PrettyTable()
    # Color
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    t.field_names = ["1. DB", "rows of 1.", "2. DB", "rows of 2.", "common rows", "overlap in %"]

    # DB2-original-facts == DB2_merged_facts (split 10)
    diff = diff_two_dirs(data_frame.db2_original_facts, bijection.db2_merged_facts, rm_identifier='10', print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data_frame.db2_original_facts.name, diff[0], bijection.db2_merged_facts.name, diff[1], diff[2], diff[3] + "%" + N])

    # DB2-separate-results == DB2_merged_results (split 10)
    diff = diff_two_dirs(data_frame.db2_original_results, bijection.db2_nemo_merged_results, rm_identifier='10', print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data_frame.db2_original_results.name, diff[0], bijection.db2_nemo_merged_results.name, diff[1], diff[2], diff[3] + "%" + N])

    # DB1-separate-results == DB1-inverse-bijection-results
    diff = diff_two_dirs(data_frame.db1_original_results, bijection.db1_inv_bij_results, rm_identifier='', print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data_frame.db1_original_results.name, diff[0], bijection.db1_inv_bij_results.name, diff[1], diff[2], diff[3] + "%" + N])

    if len(t.rows) > 0:
        print(t)


def db_overlap(db):
    split_db = {'1': 0, '10': 0, '0': 0}
    for file in db.files:
        for row in db.data_rows[file]:
            split_db[row[-1]] += 1
    return split_db, str(round(100 * split_db['0'] / (split_db['1'] + split_db['10'] + split_db['0']), 1))


def evaluate_bijection_overlap(data_frame):
    t = PrettyTable()
    t.field_names = ["Method", "data set", "unique rows DB1", "unique rows DB2", "Common Rows", "Total Rows", "overlap in %"]


    diff = diff_two_dirs(data_frame.db1_original_facts, data_frame.db2_original_facts, rm_identifier='', print_flag=True)
    t.add_row(["No Bijection","original facts", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])

    l_b = data_frame.bijections[-1]
    for bijection in data_frame.bijections:
        div = False
        split, sim = db_overlap(bijection.db2_merged_facts)
        if bijection == l_b:
            div = True
        t.add_row([bijection.name, "merged facts", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
                   sim + "%"], divider=div)
    # merged-facts-baseline
    #split, sim = db_overlap(data_frame.db2_merge_facts_base)
    #t.add_row(["merged-facts-baseline", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
    #           sim + "%"])

    diff = diff_two_dirs(data_frame.db1_original_results, data_frame.db2_original_results, rm_identifier='',
                         print_flag=True)
    t.add_row(["No Bijection", "original results", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])

    for bijection in data_frame.bijections:
        split, sim = db_overlap(bijection.db2_nemo_merged_results)
        t.add_row(
            [bijection.name, "merged results", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'], sim + "%"])


        # in the PA we only fold the relevant relations VarPointsTo etc.
        # if we export all intermediate Relations, the overlap of merged-pa-baseline will be smaller than
        # DB1/DB2 separate PA because, not all relations are folded at the end
        # if we restrict output to the main relations, both overlaps are identical
        #split, sim = db_overlap(data_frame.db2_merge_pa_base)
        #t.add_row(
        #    ["merged-pa-baseline", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'], sim + "%"])


    # dont print unique rows from each DB
    return t #.get_string(fields=["DB", "Common Rows", "Total Rows", "Similarity"])



