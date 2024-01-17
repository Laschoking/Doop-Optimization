import csv
import os
from pathlib import Path, PurePosixPath, PurePath
from Setup import *
from Lib_Functions import compareRelations
import glob

# this script takes 2 Doop databases and compares the by table
# it output the number of common entries (per table & in total)
# and gives a coverage of how many percent of both tables are common
#  -> creates file "summarize_doop_merge.csv" under MergeLeftRight/summary/


if __name__ == '__main__':

    summary_facts_path = BASE_PATH + "Summary_Facts.csv"
    summary_pa_path = BASE_PATH + "Summary_" + PA_NAME + ".csv"

    facts1_dir = Path(FACTS1_PATH)
    facts2_dir = Path(FACTS2_PATH)
    merge_facts_path = Path(MERGE_FACTS_PATH)
    merge_pa_path = Path(MERGE_PA_PATH)
    pa1_dir = Path(PA1_PATH)
    pa2_dir = Path(PA2_PATH)
    
    fact_setup = (facts1_dir, facts2_dir, merge_facts_path, summary_facts_path, "Facts")
    pa_setup = (pa1_dir, pa2_dir, merge_pa_path, summary_pa_path, str.upper(PA_NAME))
    
    # initialize variables for Facts (1. run) & PA (2. run)
    for (relation1_dir, relation2_dir, merge_relation_dir, summary_path, TYPE) in [fact_setup, pa_setup]:
        # create some variables for general db-stats
        count_common = 0
        db1_nr_entries = 0
        db2_nr_entries = 0
        c_db1 = 0
        c_db2 = 0

        # Open summary file
        with open(summary_path, 'w+') as summary_csv:
            summary = csv.writer(summary_csv, delimiter='\t', quotechar='|')
            summary.writerow(["Relation", "#Facts (1)", "#Facts (2)", "#commonLines", "Coverage(1)%", "Coverage(2)%"])

            # based on the path to the first relation, determine path to second relation
            for relation1_path in relation1_dir.glob("*"):
                relation_name = PurePosixPath(relation1_path).name
                relation2_path = PurePath.joinpath(relation2_dir,relation_name)
                merge_relation_path = PurePath.joinpath(merge_relation_dir, relation_name)

                stats = compareRelations(relation1_path, relation2_path, merge_relation_path)
                l1 = stats["len_rel1"]
                l2 = stats["len_rel2"]
                l_merge = stats["len_merge"]
                cov1 = stats["correlation1"]
                cov2 = stats["correlation2"]

                if (l1 + l2 > 0):
                    summary.writerow([relation_name, l1, l2, l_merge, cov1, cov2])
                c_db1 = c_db1 + 1 if l1 > 0 else c_db1
                c_db2 = c_db2 + 1 if l1 > 0 else c_db2

                count_common += l_merge
                db1_nr_entries += l1
                db2_nr_entries += l2

        # print fact stats
        print("-----------" + TYPE + " SUMMARY-----------")
        print("---database---")
        print("non-empty relations in DB1: " + str(c_db1))
        print("non-empty relations in DB2: " + str(c_db2))
        print("---merge stats---")
        print("total facts in DB1: " + str(db1_nr_entries) + "  |  common facts with DB2: " + str(
            count_common) + " (" + str(round(count_common * 100 / db1_nr_entries, 2) if db1_nr_entries > 0 else 0) + "%)")
        print("total facts in DB2: " + str(db2_nr_entries) + "  |  common facts with DB1: " + str(
            count_common) + " (" + str(round(count_common * 100 / db2_nr_entries, 2) if db2_nr_entries > 0 else 0) + "%)")
        print("total facts of merged db: " + str(
            db1_nr_entries + db2_nr_entries - count_common) + "  |  reduction of facts: " + str(
            round(count_common * 100 / (db1_nr_entries + db2_nr_entries), 2)) + "%")

        # determine paths for memory consumption
        # conversion in Path object is necessary to get memory consumption

        s_db1 = sum(f.stat().st_size for f in relation1_dir.glob('*') if f.is_file())
        s_db2 = sum(f.stat().st_size for f in relation2_dir.glob('*') if f.is_file())
        s_merge = sum(f.stat().st_size for f in merge_relation_dir.glob('*') if f.is_file())

        # print memory consumption
        print("---footprint---")
        print("DB1: " + str(round(s_db1 >> 10, 3)) + "kB  | DB2: " + str(
            round(s_db2 >> 10, 3)) + "kB  | merged db: " + str(
            round(s_merge >> 10, 3)) + "kB")
        print("saved memory: " + str(
            round(100 - s_merge * 100 / (s_db1 + s_db2), 2) if (s_db1 + s_db2 != 0) else 0) + "%\n")
