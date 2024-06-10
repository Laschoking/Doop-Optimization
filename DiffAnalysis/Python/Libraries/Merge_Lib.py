import os.path
import sys
import numpy as np
import csv
from prettytable import PrettyTable
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import Shell_Lib
from difflib import SequenceMatcher


def div_zero(n):
    return n if n != 0 else 10e9

def merge_baseline_facts(data):
    # merge atoms that are equal
    # TODO: ist doch super weird zeilenweise zu mergen, d.h. manchmal wird Term1 auf T2 abgebildet & manchmal nicht

    for file in data.db1_facts.files:
        rows = []
        rows1 = set(data.db1_facts.data_rows[file])
        rows2 = set(data.db2_facts.data_rows[file])
        inters = rows1.intersection(rows2)
        for row in inters:
            rows.append(row + ('0',))
        for row in rows1.difference(rows2):
            rows.append(row + ('1',))
        for row in rows2.difference(rows1):
            rows.append(row + ('10',))
        data.db2_merge_facts_base.insert_data(file,rows)
    data.db2_merge_facts_base.write_data_to_file()


'''
     - Assign the maximum value to each row_term if there are no conflicts 
     - a conflict (two row_terms have the same col_term target) is resolved by assigning the higher value (or if equal the first value)
     - iterating to resolve other conflict terms that did not get assigned yet
     - for each assignment (row_term, col_term) the corresponding column & row is masked 
'''
def calculate_pairwise_similarity(data):
    similarity_dict = {}
    # based on the path to the first relation, determine path to second relation
    for file in data.db1_facts.files:
        col_len = data.db1_facts.files[file]
        cols1 = data.db1_facts.data_cols[file]
        cols2 = data.db2_facts.data_cols[file]
        for col_nr in range(col_len):
            for term1 in cols1[col_nr]:
                for term2 in cols2[col_nr]:
                    if (term1, term2) not in similarity_dict:
                        # currently only accepts positive integers due to isdigit()
                        if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
                            max_int = max(int(term1), int(term2))
                            if max_int > 0:
                                sim = 1 - abs(int(term1) - int(term2)) / max_int
                            else:
                                # if both values are 0, have to set sim to 1
                                sim = 1
                        else:
                            sim = SequenceMatcher(None, term1, term2).ratio()

                        similarity_dict[(term1, term2)] = sim
    return similarity_dict
'''
set von columns statt liste von rows
vereinfacht berechnungen, da keine Dopplungen
'''
def calculate_occurance_similarity(data):
    similarity_dict = {}
    # based on the path to the first relation, determine path to second relation
    for file in data.db1_facts.files:
        nr_cols = data.db1_facts.files[file]
        cols1 = data.db1_facts.data_cols[file]
        cols2 = data.db2_facts.data_cols[file]
        for ind in range(nr_cols):
            for term1 in cols1[ind]:
                for term2 in cols2[ind]:
                    if (term1, term2) not in similarity_dict:
                        if term1.lstrip("-").isdigit() and term2.lstrip("-").isdigit():
                            max_int = max(int(term1), int(term2))
                            if max_int > 0:
                                sim = 1 - abs(int(term1) - int(term2)) / max_int
                            else:
                                sim = 1
                        else:
                            sim = SequenceMatcher(None, term1, term2).ratio()
                        similarity_dict[(term1, term2)] = sim + 1
                    else:
                        similarity_dict[(term1, term2)] += 1
    return similarity_dict





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


def find_best_bijection(ma_sim_matrix, row_terms, col_terms):
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


def apply_bijection(data):
    new_var_counter = 0
    for file in data.db1_facts.files:
        rows1 = data.db1_facts.data_rows[file]
        rows2 = data.db2_facts.data_rows[file]
        bijected_db = set()
        target_db = set()
        target_db.update([tuple(row) for row in rows2])
        for row1 in rows1:
            bijected_row = []
            for term in row1:
                if term in data.bijection:
                    bijected_row.append(data.bijection[term])
                else:
                    new_term = "new_var_" + str(new_var_counter)
                    data.bijection[term] = new_term  # introduce new variables
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
        data.db2_merge_facts_bij.insert_data(file, merged_rows)


def forward_bijection(data):
    # similar_files will swap the order of both directories, if db1 > db2
    # we want the smaller db to be at the y-axis (rows) and bigger db ath x-axis (columns)
    # because we biject fromt the smaller db to the bigger db
    #sim_dictionary = calculate_occurance_similarity(data)
    sim_dictionary = calculate_pairwise_similarity(data)
    ma_sim_matrix, term1_list, term2_list = create_sim_matrix(sim_dictionary)

    bijection = find_best_bijection(ma_sim_matrix, term1_list, term2_list)
    data.update_bijection(bijection)
    apply_bijection(data)
    return data


def reverse_bijection_on_pa(from_merged_db, to_bijected_db, bijection, from_identifier):
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
        to_bijected_db.insert_data(file, db1_bij_rows)
    # return to_bijected_db


def diff_two_dirs(db_inst1, db_inst2, rm_identifier='', print_flag=False):
    t = PrettyTable()
    t.field_names = ["file name", db_inst1.name, db_inst2.name, "common rows", "%"]
    t.sortby = "common rows"
    l_inters_files = 0
    l_rows1_files = 0
    l_rows2_files = 0
    for file in db_inst1.files:
        if file not in db_inst2.files:
            print("file was not compared: " + file)
            continue
        rows1 = set(db_inst1.data_rows[file])
        rows2 = set()
        # in case, one db still has identifiers appended (like ["a","b", 0], remove
        if rm_identifier != '':
            for x in db_inst2.data_rows[file]:
                # remove only common identifier & from correct side (dont consider rows that come from the other db)
                if x[-1] == str(rm_identifier) or x[-1] == '0':
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
            r = [file, l_rows1 + l_inters, l_rows2 + l_inters, l_inters, str(cov) + "%"]
            t.add_row(r)
    # t.add_row(['','','','','','',''],divider=True)
    t.add_row(["SUMMARY", l_rows1_files, l_rows2_files, l_inters_files,
               str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files))) + "%"])
    if (l_rows1_files > 0 or l_rows2_files > 0) and print_flag:
        print(t)
    # we return the nr. of rows for db1, db2, their intersection, and the overlap (inters/ (sum))
    return [l_rows1_files, l_rows2_files, l_inters_files,
            str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files), 1))]


def check_data_correctness(data):
    t = PrettyTable()
    # Color
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    t.field_names = ["1. DB", "rows of 1.", "2. DB", "rows of 2.", "common rows", "Similarity"]

    # Pointer2-facts == Pointer2_merge_facts_bij (split 10)
    diff = diff_two_dirs(data.db2_facts, data.db2_merge_facts_bij, rm_identifier=10, print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data.db2_facts.name, diff[0], data.db2_merge_facts_bij.name, diff[1], diff[2], diff[3] + "%" + N])

    # Pointer2-pa-base == Pointer2_merge_pa_bij (split 10)
    diff = diff_two_dirs(data.db2_pa_base, data.db2_merge_pa_bij, rm_identifier=10, print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data.db2_pa_base.name, diff[0], data.db2_merge_pa_bij.name, diff[1], diff[2], diff[3] + "%" + N])

    # Pointer2-pa-base == Pointer2_merge_pa_base (split 10)
    diff = diff_two_dirs(data.db2_pa_base, data.db2_merge_pa_base, rm_identifier=10, print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data.db2_pa_base.name, diff[0], data.db2_merge_pa_base.name, diff[1], diff[2], diff[3] + "%" + N])

    # Pointer1_pa_base == Pointer1_pa_inv_bij
    diff = diff_two_dirs(data.db1_pa_base, data.db1_pa_inv_bij, rm_identifier='', print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data.db1_pa_base.name, diff[0], data.db1_pa_inv_bij.name, diff[1], diff[2], diff[3] + "%" + N])

    # Pointer1-pa-base == Pointer2_merge_pa_base (split 1)
    diff = diff_two_dirs(data.db1_pa_base, data.db2_merge_pa_base, rm_identifier=1, print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data.db1_pa_base.name, diff[0], data.db2_merge_pa_base.name, diff[1], diff[2], diff[3] + "%" + N])
    if len(t.rows) > 0:
        print(t)


def db_overlap(db):
    split_db = {'1': 0, '10': 0, '0': 0}
    for file in db.files:
        for row in db.data_rows[file]:
            split_db[row[-1]] += 1
    return split_db, str(round(100 * split_db['0'] / (split_db['1'] + split_db['10'] + split_db['0']), 1))


def evaluate_bijection_overlap(data):
    t = PrettyTable()
    t.field_names = ["DB", "unique rows DB1", "unique rows DB2", "Common Rows", "Total Rows", "Similarity"]

    diff = diff_two_dirs(data.db1_facts, data.db2_facts, rm_identifier='', print_flag=False)
    t.add_row(["DB1/DB2 separate Facts ", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])

    # merged-facts-baseline
    split, sim = db_overlap(data.db2_merge_facts_base)
    t.add_row(["merged-facts-baseline", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
               sim + "%"])

    # merged-facts-bijected
    split, sim = db_overlap(data.db2_merge_facts_bij)
    t.add_row(["merged-facts-bijected", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
               sim + "%"], divider=True)
    #
    diff = diff_two_dirs(data.db1_pa_base, data.db2_pa_base, rm_identifier='', print_flag=False)
    t.add_row(["DB1/DB2 separate PA ", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])


    # in the PA we only fold the relevant relations VarPointsTo etc.
    # if we export all intermediate Relations, the overlap of merged-pa-baseline will be smaller than
    # DB1/DB2 separate PA because, not all relations are folded at the end
    # if we restrict output to the main relations, both overlaps are identical
    split, sim = db_overlap(data.db2_merge_pa_base)
    t.add_row(
        ["merged-pa-baseline", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'], sim + "%"])

    split, sim = db_overlap(data.db2_merge_pa_bij)
    t.add_row(
        ["merged-pa-bijected", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'], sim + "%"])

    # dont print unique rows from each DB
    print(t.get_string(fields=["DB", "Common Rows", "Total Rows", "Similarity"]))



