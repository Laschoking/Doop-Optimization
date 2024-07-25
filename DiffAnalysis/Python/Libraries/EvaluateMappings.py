from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def compute_overlap_dbs(db1, db2, print_flag=False):

    t = PrettyTable()
    t.field_names = ["file name", db1.name, db2.name, "common rows", "overlap in %"]
    t.sortby = "common rows"

    l_records_db1 = 0
    l_records_db2 = 0
    l_records_db_merge = 0
    div = False
    for file_name,df1 in db1.files.items():
        if file_name not in db2.files:
            raise FileNotFoundError("df does not exist in db2: " + db2.name + " file: " + file_name)

        df2 = db2.files[file_name]
        if df1.empty or df2.empty:
            # create dummy merge-df
            df1_only = df1
            df2_only = df2
            df_both = pd.DataFrame()
        else:
            df = pd.merge(df1, df2, how='outer',indicator=True)
            df1_only = df[df['_merge'] == 'left_only']
            df2_only = df[df['_merge'] == 'right_only']
            df_both = df[df['_merge'] == 'both']

        l_df1_only = df1_only.shape[0]
        l_df2_only = df2_only.shape[0]
        l_df_both = df_both.shape[0]

        l_records_db1 += l_df1_only
        l_records_db2 += l_df2_only
        l_records_db_merge += l_df_both

        if l_df1_only > 0 and print_flag:
            print(file_name)
            print("db1 unique-rows: ")
            print(df1_only)
        if l_df2_only > 0 and print_flag:
            print("db2 unique-rows: ")
            print(df2_only)

        if l_df1_only + l_df2_only + l_df_both == 0: continue

        cov = round(100 * l_df_both / (l_df1_only + l_df2_only + l_df_both))
        if cov != 100:
            r = [file_name, l_df1_only, l_df2_only, l_df_both, str(cov) + "%"]
            t.add_row(r,divider=div)

            # atoms appearing in more than 1 relation are only counted once

    #t.add_row(['','','','',''],divider=True)
    total_rows = l_records_db1 + l_records_db2 + l_records_db_merge
    t.add_row(["SUMMARY", l_records_db1 , l_records_db2 , l_records_db_merge,
               str(round(100 * l_records_db_merge / (total_rows),2)) + "%"])
    if (l_records_db1 > 0 or l_records_db2 > 0) and print_flag:
        print(t)
    # we return the nr. of rows for db1, db2, their intersection, and the overlap (inters/ (sum))
    return [l_records_db1, l_records_db2, l_records_db_merge, str(round(100 * l_records_db_merge / total_rows, 2)) + "%"]


def verify_merge_results(data, mapping):
    t = PrettyTable()
    # Color
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    t.field_names = ["1. DB","2. DB", "rows of 1.", "rows of 2.", "common rows", "overlap in %"]

    # DB1-separate-results == db1_unravelled_results
    diff = compute_overlap_dbs(data.db1_original_results, mapping.db1_unravelled_results,print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        l = [R + data.db1_original_results.name,mapping.db1_unravelled_results.name] + diff[:-1] + [diff[-1] + N]
        t.add_row(l)

    # DB2-separate-results == db2_unravelled_results
    diff = compute_overlap_dbs(data.db2_original_results, mapping.db2_unravelled_results,print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        l = [R + data.db2_original_results.name,mapping.db2_unravelled_results.name] + diff[:-1] + [diff[-1] + N]
        t.add_row(l)


    if len(t.rows) > 0:
        print(t)

def count_overlap_merge_db(merge_db):
    c_left = 0
    c_right = 0
    c_both = 0

    for df in merge_db.files.values():
        if df.empty:
            continue
        # access last column that holds identifier for each record
        val_count = df.iloc[:,-1].value_counts()
        ind = val_count.index
        if '1' in ind:
            c_left += val_count.at['1']
        if '10' in ind:
            c_right += val_count.at['10']
        if '0' in ind:
            c_both += val_count.at['0']

    total_records = c_left + c_right + c_both
    if total_records > 0:
        overlap = round(100 * c_both / total_records,2)
    else:
        overlap = 0.0
    return [c_left, c_right,c_both,str(overlap) + "%"]


