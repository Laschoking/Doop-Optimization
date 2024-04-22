import numpy as np
import csv
from prettytable import PrettyTable
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import Shell_Lib
from difflib import SequenceMatcher


def div_zero(n):
    return n if n != 0 else 10e9


def merge_relations(rel_class, write_flag, debug_flag):
    with open(rel_class.rel1.path, newline='') as f1, open(rel_class.rel2.path, newline='') as f2, open(rel_class.merge.path, 'w',
                                                                                newline='') as merge:

        merge_writer = csv.writer(merge, delimiter='\t',quoting=csv.QUOTE_NONE )# lineterminator='\n')
        nr_cols = 0
        f1_tsv = csv.reader(f1, delimiter='\t', quotechar='"')
        f2_tsv = csv.reader(f2, delimiter='\t', quotechar='"')
        r1 = set()
        r2 = set()
        for file,r in [f1_tsv,r1],[f2_tsv,r2]:
            for row in file:
                r.add(tuple(row))

        rel_class.rel1.rows = r1
        rel_class.rel2.rows = r2

        rel_class.common.rows = rel_class.rel1.rows.intersection(rel_class.rel2.rows)
        rel_class.common.nr_rows = len(rel_class.common.rows)

        for rel in [rel_class.rel1, rel_class.rel2]:
            rel.nr_rows = len(rel.rows)
            intersection = rel.rows.difference(rel_class.common.rows)
            # find relations, that are only in one file and add specific id
            if len(intersection) > 0 and debug_flag: print(rel.path)
            for diff_rel in intersection:
                rel.nr_chars += len(diff_rel)
                rel_class.merge.nr_chars += len(diff_rel) + len(
                    str(rel_class.common.id_nr))  # for additional lenght of id
                if debug_flag: print('\t'.join(diff_rel))
                diff_rel = diff_rel + tuple([rel.id_nr])
                rel_class.merge.nr_chars += len(diff_rel)
                if write_flag:
                    merge_writer.writerow(diff_rel)

            if nr_cols == 0 and rel.nr_rows > 0:
                test_row = rel.rows.pop()
                nr_cols = len(test_row)
                rel.rows.add(test_row)
            rel.nr_entries = rel.nr_rows * nr_cols
            rel.size = rel.path.stat().st_size

        # find facts, that are in both files & add with specific id
        for common_entries in rel_class.common.rows:
            rel_class.common.nr_chars += len(common_entries)
            rel_class.merge.nr_chars += len(common_entries) + len(
                str(rel_class.common.id_nr))  # for additional lenght of id
            common_entries = common_entries + tuple([rel_class.common.id_nr])
            if write_flag:
                merge_writer.writerow(common_entries)

        if nr_cols == 0 and rel_class.common.nr_rows > 0:
            test_row = rel_class.common.rows.pop()
            nr_cols = len(test_row)
            rel_class.common.rows.add(test_row)

        rel_class.rel1.nr_chars += rel_class.common.nr_chars
        rel_class.rel2.nr_chars += rel_class.common.nr_chars
        rel_class.common.nr_entries = rel_class.common.nr_rows * nr_cols
        rel_class.nr_cols = nr_cols
    rel_class.merge.nr_rows = rel_class.rel1.nr_rows + rel_class.rel2.nr_rows - rel_class.common.nr_rows
    rel_class.merge.nr_entries = rel_class.merge.nr_rows * (nr_cols + 1)

    # get file size after merge-file is closed
    rel_class.merge.size = rel_class.merge.path.stat().st_size


def find_best_bijection(sim_matrix_ma,from_terms,to_terms):
    shape = sim_matrix_ma.shape
    from_side = 0
    to_side = 1
    bijection = {}
    it = 0
    while(sim_matrix_ma.mask.all() == False and it < 5):
        max_ind_to_side = sim_matrix_ma.argmax(axis=to_side) # list comprehension along the axis (col = 0)
        max_val_to_side = sim_matrix_ma.max(axis=to_side)
        remove_from_side = set()
        remove_to_side = set()
        from_iterator = 0
        for to_range in range(len(max_ind_to_side)):
            to_index = max_ind_to_side[to_range]
            if max_val_to_side[to_range] > 0:
                to_index_list = np.where(max_ind_to_side == to_index)[0]
                if len(to_index_list) > 1:
                    vals = [max_val_to_side[a] for a in to_index_list]
                    from_index = to_index_list[np.argmax(vals)] # change index to max similarity cell (possibly further in the list)
                    print(from_index)
                    print(to_index_list)
                    print(vals)
                else:
                    from_index = from_iterator
                from_term = from_terms[from_index]
                to_term = to_terms[to_index]
                #print(from_term,to_term)
                bijection[from_term] = to_term
                remove_from_side.add(from_index)
                remove_to_side.add(to_index)
            from_iterator += 1

        it += 1
        # instead of deleting rows and columns we set them to 0, thus we dont have changing indices
        for i in remove_from_side : sim_matrix_ma[i,:] = np.ma.masked
        for i in remove_to_side : sim_matrix_ma[:,i] = np.ma.masked


        print("current length of bijection: " + str(len(bijection)))
    #print(bijection)

        #rm entries
            # handle multiple


def find_bijection(merge_class):
    dir1 = merge_class.dir1
    dir2 = merge_class.dir2
    common_dir = merge_class.common_dir
    merge_dir = merge_class.merge_dir
    Shell_Lib.clear_directory(merge_dir.path)
    terms1 = set()
    terms2 = set()

    similarity_dict = {}
    # based on the path to the first relation, determine path to second relation
    for rel1_path in dir1.path.glob("*"):
        rel_name = rel1_path.name
        rel2_path = dir2.path.joinpath(rel_name)
        if not rel2_path.exists():
            new_suffix = '.csv' if rel1_path.suffix == ".tsv" else '.tsv'
            rel2_path = rel2_path.with_suffix(new_suffix)
            if not rel2_path.exists():
                print(FileNotFoundError("Skipped file: " + str(rel2_path.stem)))
                continue
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
                        sim = 0
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
    term1_list = []
    term2_list = []
    for (term1,term2) in similarity_dict:
        if term1 not in term1_list: term1_list.append(term1)
        if term2 not in term2_list: term2_list.append(term2)

    # the smaller from_db will be projected to the to_bigger one ->
    # make sure, that smalled from_db is y-axis (rows) & bigger to_db is x-axis
    sim_matrix = np.zeros(shape=(len(term1_list) ,len(term2_list)))
    for (term1,term2) in similarity_dict:
        term1_ind = term1_list.index(term1)
        term2_ind = term2_list.index(term2)
        sim_matrix[term1_ind][term2_ind] = similarity_dict[term1, term2]
    if len(term1_list) > len(term2_list):
        sim_matrix = sim_matrix.transpose()
        tmp = term1_list
        term1_list = term2_list
        term2_list = tmp
    sim_matrix_ma = np.ma.masked_equal(sim_matrix,0)
    bijection = find_best_bijection(sim_matrix_ma,term1_list,term2_list)






def merge_directories(merge_class, write_flag, debug_flag):
    # create some variables for general db-stats
    dir1 = merge_class.dir1
    dir2 = merge_class.dir2
    common_dir = merge_class.common_dir
    find_bijection(merge_class)
    '''
    merge_dir = merge_class.merge_dir
    Shell_Lib.clear_directory(merge_dir.path)

    # based on the path to the first relation, determine path to second relation
    for rel1_path in dir1.path.glob("*"):
        rel_name = rel1_path.name
        rel2_path = dir2.path.joinpath(rel_name)
        if not rel2_path.exists():
            new_suffix = '.csv' if rel1_path.suffix == ".tsv" else '.tsv'
            rel2_path = rel2_path.with_suffix(new_suffix)
            if not rel2_path.exists():
                print(FileNotFoundError("Skipped file: " + str(rel2_path.stem)))
                continue
        merge_rel_path = Path.joinpath(merge_dir.path, rel_name)

        rel_class = RelationClass(merge_rel_path, rel1_path, rel2_path, NR_LEFT, NR_RIGHT, NR_TARGET)
        merge_class.add_relation(rel_class)
        merge_relations(rel_class, write_flag, debug_flag)
        dir1.update(rel_class.rel1)
        dir2.update(rel_class.rel2)
        common_dir.update(rel_class.common)
        merge_dir.update(rel_class.merge)
        merge_class.nr_cols += rel_class.nr_cols
    '''
    return merge_class

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

