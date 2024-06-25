from prettytable import PrettyTable

def diff_two_dirs(db1, db2, rm_identifier='', print_flag=True):
    t = PrettyTable()
    t.field_names = ["file name", db1.name, db2.name, "common rows", "overlap in %"]
    t.sortby = "common rows"
    unique_rows_db1 = set()
    unique_rows_db2 = set()
    inters_db1_db2 = set()

    file_count = len(db1.files)
    div = False
    for file in db1.files:
        file_count -= 1
        if file not in db2.files:
            print("faulty database: " + db2.name)
            print("file was not compared: " + file)
            continue
        rows1 = set(tuple(row) for row in db1.data_rows[file])
        rows2 = set()
        # in case, one db still has identifiers appended (like ["a","b", 0], remove
        if rm_identifier != '':
            for x in db2.data_rows[file]:
                # remove only common identifier & from correct side (dont consider rows that come from the other db)
                if x[-1] == rm_identifier or x[-1] == '0':
                    rows2.add(tuple(x[:-1]))
        else:
            rows2 = set(tuple(row) for row in db2.data_rows[file])

        inters = rows1.intersection(rows2)
        unique_rows1 = rows1.difference(rows2)
        unique_rows2 = rows2.difference(rows1)

        l_inters = len(inters)
        l_rows1 = len(unique_rows1)
        if l_rows1 > 0 and print_flag:
            print(file)
            print(unique_rows1)
        l_rows2 = len(unique_rows2)
        inters_db1_db2 = inters_db1_db2 | inters
        unique_rows_db1 =  unique_rows_db1 | unique_rows1
        unique_rows_db2 = unique_rows_db2 | unique_rows2
        if l_rows1 + l_rows2 + l_inters == 0: continue

        cov = round(100 * l_inters / (l_rows1 + l_rows2 + l_inters))
        if cov != 100:
            r = [file, l_rows1, l_rows2, l_inters, str(cov) + "%"]
            t.add_row(r,divider=div)


    l_rows1_files = len(unique_rows_db1)
    l_rows2_files = len(unique_rows_db2)
    l_inters_files = len(inters_db1_db2)
    #t.add_row(['','','','',''],divider=True)
    t.add_row(["SUMMARY", l_rows1_files , l_rows2_files , l_inters_files,
               str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files))) + "%"])
    if (l_rows1_files > 0 or l_rows2_files > 0) and print_flag:
        print(t)
    # we return the nr. of rows for db1, db2, their intersection, and the overlap (inters/ (sum))
    return ([l_rows1_files, l_rows2_files, l_inters_files,
            str(round(100 * l_inters_files / (l_rows1_files + l_rows2_files + l_inters_files), 1))], unique_rows_db1, unique_rows_db2, inters_db1_db2)


def check_data_correctness(data_frame, mapping):
    t = PrettyTable()
    # Color
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    t.field_names = ["1. DB", "rows of 1.", "2. DB", "rows of 2.", "common rows", "overlap in %"]
    # DB1-original-facts == DB2_merged_facts (split 1 & inverse bijection)

    # TODO: identifier in db speichern
    # this is only to verify that the original facts db can be produced from merging
    mapping.revert_db_mapping(mapping.db2_merged_facts, mapping.db1_inv_bij_facts, 1)
    diff,unique_rows_db1,unique_rows_db2, inters_db1_db2 = diff_two_dirs(data_frame.db1_original_facts, mapping.db1_inv_bij_facts, rm_identifier='', print_flag=False)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data_frame.db2_original_facts.name, diff[0], mapping.db2_merged_facts.name, diff[1], diff[2], diff[3] + "%" + N])


    # DB2-original-facts == DB2_merged_facts (split 10)
    diff = diff_two_dirs(data_frame.db2_original_facts, mapping.db2_merged_facts, rm_identifier='10', print_flag=False)[0]
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row(
            [R + data_frame.db2_original_facts.name, diff[0], mapping.db2_merged_facts.name, diff[1], diff[2], diff[3] + "%" + N])

    # DB2-separate-results == DB2_merged_results (split 10)
    diff = diff_two_dirs(data_frame.db2_original_results, mapping.db2_nemo_merged_results, rm_identifier='10', print_flag=False)[0]
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data_frame.db2_original_results.name, diff[0], mapping.db2_nemo_merged_results.name, diff[1], diff[2], diff[3] + "%" + N])

    # DB1-separate-results == DB1-inverse-mapping-results
    diff,unique_rows_db1,unique_rows_db2, inters_db1_db2 = diff_two_dirs(data_frame.db1_original_results, mapping.db1_inv_bij_results, rm_identifier='', print_flag=True)
    if (diff[0] > 0 or diff[1] > 0):
        t.add_row([R + data_frame.db1_original_results.name, diff[0], mapping.db1_inv_bij_results.name, diff[1], diff[2], diff[3] + "%" + N])

        # find out why atoms were not mapped correctly
        wrong_mapped = PrettyTable()
        wrong_mapped.field_names = ["terms db2 ","mapping to"]
        inv_bijection = dict((term2, term1) for term1, term2 in mapping.mapping.items())

        for rows1 in unique_rows_db1:
            for term1 in rows1:
                if term1 in inv_bijection:
                    wrong_mapped.add_row([term1,inv_bijection[term1]])
                else:
                    wrong_mapped.add_row([term1,''])

        #print(wrong_mapped)

    if len(t.rows) > 0:
        print(t)


def db_overlap(db):
    split_db = {'1': 0, '10': 0, '0': 0}
    for file in db.files:
        for row in db.data_rows[file]:
            split_db[row[-1]] += 1
        #print(file + ": " +  str(split_db['1']) + "  " + str(split_db['10']) + "  " + str(split_db['0']))
    return split_db, str(round(100 * split_db['0'] / (split_db['1'] + split_db['10'] + split_db['0']), 1))


def evaluate_mapping_overlap(data_frame):
    t = PrettyTable()
    t.field_names = ["Method", "data set", "unique rows DB1", "unique rows DB2", "Common Rows", "Total Rows", "overlap in %"]


    diff = diff_two_dirs(data_frame.db1_original_facts, data_frame.db2_original_facts, rm_identifier='', print_flag=False)[0]
    t.add_row(["No mapping","original facts", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])

    l_b = data_frame.mappings[-1]
    for mapping in data_frame.mappings:
        div = False
        split, sim = db_overlap(mapping.db2_merged_facts)
        if mapping == l_b:
            div = True
        t.add_row([mapping.name, "merged facts", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
                   sim + "%"], divider=div)
    # merged-facts-baseline
    #split, sim = db_overlap(data_frame.db2_merge_facts_base)
    #t.add_row(["merged-facts-baseline", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'],
    #           sim + "%"])

    diff = diff_two_dirs(data_frame.db1_original_results, data_frame.db2_original_results, rm_identifier='',
                         print_flag=False)[0]
    t.add_row(["No mapping", "original results", diff[0], diff[1], diff[2], diff[0] + diff[1] + diff[2], diff[3] + "%"])

    for mapping in data_frame.mappings:
        split, sim = db_overlap(mapping.db2_nemo_merged_results)
        t.add_row(
            [mapping.name, "merged results", split['1'], split['10'], split['0'], split['0'] + split['1'] + split['10'], sim + "%"])

    return t.get_string(fields=["Method", "data set", "Common Rows", "Total Rows", "overlap in %"])



