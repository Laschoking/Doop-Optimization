import csv
import os
from Setup import *
from pathlib import Path, PurePosixPath
import glob

from Lib_Functions import compareRelations

# this script takes 2 Doop databases and compares the by table
# it output the number of common entries (per table & in total)
# and gives a coverage of how many percent of both tables are common
#  -> creates file "summarize_doop_merge.csv" under MergeLeftRight/summary/


if __name__ == '__main__':
    count_common = 0
    count_facts1 = 0
    count_facts2 = 0
    c_db1 = 0
    c_db2 = 0
    merge = Path(PA1_PATH)
    pa_results = merge.glob('*')

    # assume that both analysis have the same pa-results
    for relation1_path in pa_results:
        relation_name = PurePosixPath(relation1_path).name
        relation2_path = Path(PA2_PATH + relation_name)

        with open(MERGE_BASE_PATH + "Summary_" + PA_NAME + ".csv", 'w+') as summary_csv:
            summ = csv.writer(summary_csv, delimiter='\t', quotechar='|')
            summ.writerow(["Relation", "#Facts (1)", "#Facts (2)", "#commonLines", "Coverage(1)%", "Coverage(2)%"])
            merge_relation = MERGE_PA_PATH + relation_name

            stats = compareRelations(relation1_path, relation2_path,merge_relation, relation_name, summ)


    # print fact stats
    print("---FACT SUMMARY---")
    print("---database---")
    print("non-empty relations in db1: " + str(c_db1))
    print("non-empty relations in db2: " + str(c_db2))
    print("---merge stats---")
    print("total facts in db1: " + str(count_facts1) + "  |  common facts with db2: " + str(count_common) + " (" + str(round(count_common * 100 / count_facts1, 2) if count_facts1 > 0 else 0) + "%)")
    print("total facts in db2: " + str(count_facts2) + "  |  common facts with db1: " + str(count_common) + " (" + str(round(count_common * 100 / count_facts2, 2) if count_facts2 > 0 else 0) + "%)")
    print("total facts of merged db: " + str(count_facts1 + count_facts2 - count_common) + "  |  reduction of facts: " + str(round(count_common * 100 / (count_facts1 + count_facts2),2)) + "%")
    # print dir footprint
    print("---footprint---")
    print("db1: " + str(round(s_db1 >> 10, 2)) + "kB  | db2: " + str(round(s_db2 >> 10, 2)) + "kB  | merged db: " + str(
        round(s_merge >> 10, 2)) + "kB")
    print("saved memory: " + str(round(100 - s_merge * 100 / (s_db1 + s_db2), 2) if (s_db1 + s_db2 != 0) else 0) + "%")
'''