import csv


def compareRelations(relation1, relation2, merge_relation):
    results = {}
    with open(relation1) as f1, open(relation2) as f2, open(merge_relation, 'w', newline='') as merge:
        merge_writer = csv.writer(merge, delimiter=",")
        rel1 = set(map(str.rstrip, f1))
        rel2 = set(map(str.rstrip, f2))
        rel_merged = rel1.intersection(rel2)
        nr_rows_rel_merge = 0
        nr_chars_rel1 = 0
        nr_chars_rel2 = 0
        nr_chars_rel_common = 0

        # find relations, that are only in file 1 & add with number 1
        for diff_rel1 in rel1.difference(rel_merged):
            nr_chars_rel1 += len(diff_rel1)
            diff_rel1 = diff_rel1.split('\t')
            diff_rel1.append(1)
            nr_rows_rel_merge += 1
            merge_writer.writerow(diff_rel1)


        # find facts, that are only in file 2 & add with number 2
        for diff_rel2 in rel2.difference(rel_merged):
            nr_chars_rel2 += len(diff_rel2)
            diff_rel2 = diff_rel2.split('\t')
            diff_rel2.append(2)
            nr_rows_rel_merge += 1
            merge_writer.writerow(diff_rel2)

        # find facts, that are in both files & add with number 3
        for common_entries in rel_merged:
            nr_chars_rel_common += len(common_entries)
            common_entries = common_entries.split('\t')
            common_entries.append(3)
            nr_rows_rel_merge += 1
            merge_writer.writerow(common_entries)
        nr_rows_rel1 = len(rel1)
        nr_rows_rel2 = len(rel2)
        nr_common_rows = len(rel_merged)

        nr_cols_rel = 0
        if nr_rows_rel1 > 0:
            perc_common_rel1 = round(nr_common_rows / nr_rows_rel1, 3)
            nr_cols_rel = len(rel1.pop().split('\t'))
        else:
            perc_common_rel1 = 0
        if nr_rows_rel2 > 0:
            perc_common_rel2 = round(nr_common_rows / nr_rows_rel2, 3)
            nr_cols_rel  = len(rel2.pop().split('\t'))
        else:
            perc_common_rel2 = 0
        results["nr_chars_rel1"] = nr_chars_rel1 + nr_chars_rel_common
        results["nr_chars_rel2"] = nr_chars_rel2 + nr_chars_rel_common
        results["nr_chars_merge"] = nr_chars_rel1 + + nr_chars_rel2 + nr_chars_rel_common + nr_rows_rel_merge # da *1 fuer 1 zahl

        results["nr_cols_rel"] = nr_cols_rel
        results["nr_rows_rel1"] = nr_rows_rel1
        results["nr_rows_rel2"] = nr_rows_rel2
        results["nr_rows_rel_merge"] = nr_rows_rel_merge
        results["perc_common_rel1"] = perc_common_rel1
        results["perc_common_rel2"] = perc_common_rel2
        results["nr_common_rows"] = nr_common_rows
    return results
