import csv
import os
from pathlib import Path
from Setup import *
from Lib_Functions import compareRelations
import glob

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
    with open(FACT_LIST) as f:
        database = f.readlines()
    with open(BASE_PATH + "Summary_Facts.csv", 'w+') as summary_csv:
        summary = csv.writer(summary_csv, delimiter='\t', quotechar='|')
        summary.writerow(["Relation", "#Facts (1)", "#Facts (2)", "#commonLines", "Coverage(1)%", "Coverage(2)%"])
        for relation in database:
            relation = relation.split()[0]
            relation1 = FACTS1_PATH + relation
            relation2 = FACTS2_PATH + relation
            merge_relation = MERGE_FACTS_PATH + relation
            
            stats = compareRelations(relation1,relation2,merge_relation, relation, summary)
            l1 = stats["len_rel1"]
            l2 = stats["len_rel2"]
            l_merge = stats["len_merge"]
            cov1 = stats["correlation1"]
            cov2 = stats["correlation2"]


            c_db1 = c_db1 + 1 if l1 > 0 else c_db1
            c_db2 = c_db2 + 1 if l1 > 0 else c_db2

            count_common += l_merge
            count_facts1 += l1
            count_facts2 += l2
    

    # print fact stats
    print("---FACT SUMMARY---")
    print("---database---")
    print("non-empty relations in DB1_NAME: " + str(c_db1))
    print("non-empty relations in DB2_NAME: " + str(c_db2))
    print("---merge stats---")
    print("total facts in DB1_NAME: " + str(count_facts1) + "  |  common facts with DB2_NAME: " + str(count_common) + " (" + str(round(count_common * 100 / count_facts1, 2) if count_facts1 > 0 else 0) + "%)")
    print("total facts in DB2_NAME: " + str(count_facts2) + "  |  common facts with DB1_NAME: " + str(count_common) + " (" + str(round(count_common * 100 / count_facts2, 2) if count_facts2 > 0 else 0) + "%)")
    print("total facts of merged db: " + str(count_facts1 + count_facts2 - count_common) + "  |  reduction of facts: " + str(round(count_common * 100 / (count_facts1 + count_facts2),2)) + "%")


    # determine paths for memory consumption
    # conversion in Path object is necessary to get memory consumption
    facts1 = Path(FACTS1_PATH)
    facts2 = Path(FACTS2_PATH)
    merge = Path(MERGE_FACTS_PATH)
    s_db1 = sum(f.stat().st_size for f in facts1.glob('*') if f.is_file())
    s_db2 = sum(f.stat().st_size for f in facts2.glob('*') if f.is_file())
    s_merge = sum(f.stat().st_size for f in merge.glob('**/*') if f.is_file())

    # print memory consumption
    print("---footprint---")
    print("DB1_NAME: " + str(round(s_db1 >> 10, 3)) + "kB  | DB2_NAME: " + str(round(s_db2 >> 10, 3)) + "kB  | merged db: " + str(
        round(s_merge >> 10, 3)) + "kB")
    print("saved memory: " + str(round(100 - s_merge * 100 / (s_db1 + s_db2), 2) if (s_db1 + s_db2 != 0) else 0) + "%")
