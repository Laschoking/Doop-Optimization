from prettytable import PrettyTable
import numpy as np
import sys
from Python.Libraries.Mapping.Mapping import *

class Crossproduct_Mapping(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)
        self.mapping = dict()

# TODO: rewrite this without data_cols
    def compute_similarity(self,db1,db2):
        # based on the path to the first relation, determine path to second relation
        similarity_dict = dict()
        for file in db1.files:
            nr_cols = db1.files[file]
            cols1 = db1.data_cols[file]
            cols2 = db2.data_cols[file]
            for ind in range(nr_cols):
                for term1 in cols1[ind]:
                    for term2 in cols2[ind]:
                        if (term1, term2) not in similarity_dict:
                            sim = self.similarity(term1, term2,0)
                            similarity_dict[(term1, term2)] = sim
                        else:
                            sim = self.similarity(term1, term2, similarity_dict[(term1, term2)])
                            similarity_dict[(term1, term2)] = sim
        return similarity_dict

    def create_sim_matrix(self, similarity_dict):
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

    def compute_mapping(self,db1,db2,pa_non_terms):
        similarity_dict = self.compute_similarity(db1,db2)
        ma_sim_matrix, row_terms, col_terms = self.create_sim_matrix(similarity_dict)

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
                    self.mapping[row_term] = col_term

                    # mask corresponding column & row (preserves indices for look up of term name)
                    ma_sim_matrix[row, :] = np.ma.masked
                    ma_sim_matrix[:, max_col] = np.ma.masked
                row_it += 1
            # print(conflict_table)
            count_iter += 1

    def similarity(self,t1,t2,sim):
        return 0