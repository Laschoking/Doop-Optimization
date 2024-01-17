import csv


def compareRelations(relation1, relation2, merge_relation):
    results = {}
    with open(relation1) as f1, open(relation2) as f2, open(merge_relation, 'w', newline='') as merge:
        merge_writer = csv.writer(merge, delimiter=",")
        rel1 = set(map(str.rstrip, f1))
        rel2 = set(map(str.rstrip, f2))
        rel_merged = rel1.intersection(rel2)

        # find relations, that are only in file 1 & add with number 1
        for diff_rel1 in rel1.difference(rel_merged):
            diff_rel1 = diff_rel1.split('\t')
            diff_rel1.append(1)
            merge_writer.writerow(diff_rel1)

        # find facts, that are only in file 2 & add with number 2
        for diff_rel2 in rel2.difference(rel_merged):
            diff_rel2 = diff_rel2.split('\t')
            diff_rel2.append(2)
            merge_writer.writerow(diff_rel2)

        # find facts, that are in both files & add with number 3
        for common_entries in rel_merged:
            common_entries = common_entries.split('\t')
            common_entries.append(3)
            merge_writer.writerow(common_entries)
        len_rel1 = len(rel1)
        len_rel2 = len(rel2)
        len_merge = len(rel_merged)
        cov1 = round(len_merge / len_rel1, 3) if len_rel1 > 0 else 0
        cov2 = round(len_merge / len_rel2, 3) if len_rel2 > 0 else 0
        results["len_rel1"] = len_rel1
        results["len_rel2"] = len_rel2
        results["len_merge"] = len_merge
        results["correlation1"] = cov1
        results["correlation2"] = cov2


    return results
