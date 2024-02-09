import csv
import os
from pathlib import Path, PurePosixPath, PurePath
from Path_Lib import *
from Lib_Functions import compareRelations,divZero
import System_Setup
import glob

# this script takes 2 Doop databases and compares the by table
# it output the number of common entries (per table & in total)
# and gives a coverage of how many percent of both tables are common
#  -> creates file "summarize_doop_merge.csv" under MergeLeftRight/summary/


if __name__ == '__main__':
    analysis = Analysis(DB_Pointer,PA_PointerAnalysis,PA_TYPES.NEMO)
    System_Setup.Create_Dirs(analysis)
    System_Setup.DOOP_Create_Facts(analysis)
    '''match analysis.engine:
        case PA_TYPES.SOUFFLE_INT:
            System_Setup.SOUFFLE_INT(analysis)
        case PA_TYPES.SOUFFLE_EXT:
            System_Setup.Run_SOUFFLE_EXT_PA(analysis)
        case PA_TYPES.NEMO:
            System_Setup.Run_NEMO_PA(analysis)
    '''
    # create some variables for general db-stats
    nr_rows_db1 = 0
    nr_rows_db2 = 0
    nr_rows_merge = 0
    nr_common_rows_db = 0
    nr_entries_db1 = 0
    nr_entries_db2 = 0
    nr_entries_merge = 0
    nr_filled_rel_db1 = 0
    nr_filled_rel_db2 = 0
    nr_rel = 0
    nr_chars_db1 = 0
    nr_chars_db2 = 0
    nr_chars_db_merge = 0
    avg_col_size = 0

    # Open summary file
    with open(analysis.summary_pa_path, 'w+') as summary_csv:
        summary = csv.writer(summary_csv, delimiter='\t', quotechar='|')
        summary.writerow(["Relation", "#Facts (1)", "#Facts (2)", "#commonLines", "Coverage(1)%", "Coverage(2)%"])

        # based on the path to the first relation, determine path to second relation
        for rel1_path in analysis.db1.facts_path.glob("*"):
            rel_name = Path(rel1_path).name
            rel2_path = Path.joinpath(analysis.db2.facts_path,rel_name)
            merge_rel_path = Path.joinpath(analysis.merge_facts_path, rel_name)

            stats = compareRelations(rel1_path, rel2_path, merge_rel_path)
            nr_rows_rel1 = stats["nr_rows_rel1"]
            nr_rows_rel2 = stats["nr_rows_rel2"]
            nr_cols = stats["nr_cols_rel"]
            nr_rows_rel_merge = stats["nr_rows_rel_merge"]
            perc_common_rel1 = stats["perc_common_rel1"]
            perc_common_rel2 = stats["perc_common_rel2"]
            nr_common_rows_db += stats["nr_common_rows"]
            nr_chars_db1 += stats["nr_chars_rel1"]
            nr_chars_db2 += stats["nr_chars_rel2"]
            nr_chars_db_merge += stats["nr_chars_merge"]


            if nr_rows_rel1 + nr_rows_rel2 > 0:
                summary.writerow([rel_name, nr_rows_rel1, nr_rows_rel2, nr_rows_rel_merge, perc_common_rel1, perc_common_rel2])
                avg_col_size += nr_cols
            nr_filled_rel_db1 = nr_filled_rel_db1 + 1 if nr_rows_rel1 > 0 else nr_filled_rel_db1
            nr_filled_rel_db2 = nr_filled_rel_db2 + 1 if nr_rows_rel2 > 0 else nr_filled_rel_db2
            nr_rel = nr_rel + 1
            nr_rows_merge += nr_rows_rel_merge
            nr_rows_db1 += nr_rows_rel1
            nr_rows_db2 += nr_rows_rel2
            nr_entries_db1 += nr_rows_rel1 * nr_cols
            nr_entries_db2 += nr_rows_rel2 * nr_cols
            nr_entries_merge += nr_rows_rel_merge * (nr_cols + 1)

        # determine paths for memory consumption
        # conversion in Path object is necessary to get memory consumption
        max_db_count = max(nr_filled_rel_db1, nr_filled_rel_db2)
        avg_col_size = avg_col_size / max_db_count if max_db_count > 0 else 1
        size_db1 = sum(f.stat().st_size for f in analysis.db1.facts_path.glob('*') if f.is_file())
        size_db2 = sum(f.stat().st_size for f in analysis.db2.facts_path.glob('*') if f.is_file())
        size_merge = sum(f.stat().st_size for f in analysis.merge_facts_path.glob('*') if f.is_file())

        # print memory consumption

                # print fact stats
        print("----------- FACTS SUMMARY-----------")
        print("---database---")
        print("relations in each DB:       " + str(nr_rel))
        print("non-empty relations in DB1: " + str(nr_filled_rel_db1))
        print("non-empty relations in DB2: " + str(nr_filled_rel_db2))
        print("sum of rows in DB1 & DB2: " + str(nr_rows_db1 + nr_rows_db2))
        print("common rows in DB1 & DB2: " + str(nr_common_rows_db) + "     -> DB-Similarity (" + str(round(2 * nr_common_rows_db * 100 / divZero(nr_rows_db1 + nr_rows_db2),1)) + "%)")
        print("average column size: " + str(round(avg_col_size,1)))

        print("\n---merge stats---")

        print("DB1   - rows: " + str(nr_rows_db1) + "           entries: " + str(nr_entries_db1) + "            chars: " + str(round(nr_chars_db1 /1000,1)) + "k             size: " +
        str(round(size_db1 >> 10, 3)) + "kB")
        #common rows: " + str(nr_common_rows_db) + " (" + str(round(nr_common_rows_db * 100 / nr_rows_db1, 2) if nr_rows_db1 > 0 else 0) + "%)")

        print("DB2   - rows: " + str(nr_rows_db2) + "           entries: " + str(nr_entries_db2) + "            chars: " + str(round(nr_chars_db2/1000,1)) + "k             size: " +
              str(round(size_db2 >> 10, 3)) + "kB")
        #common rows: " + str(
            #nr_common_rows_db) + " (" + str(round(nr_common_rows_db * 100 / nr_rows_db2, 2) if nr_rows_db2 > 0 else 0) + "%)")

        print("Merge - rows: " + str(nr_rows_merge) + " (" + str(
            round(nr_rows_merge * 100 / divZero(nr_rows_db1 + nr_rows_db2) - 100, 1)) + "%)" +
            "  entries: " + str(nr_entries_merge) + " (" + str(round(nr_entries_merge * 100 / divZero(nr_entries_db1 + nr_entries_db2) - 100, 1) ) + "%)"
            + "   chars: " + str(round(nr_chars_db_merge/1000,1)) + "k (" + str(round(nr_chars_db_merge * 100 / divZero(nr_chars_db1 + nr_chars_db2) - 100, 1)) + "%)    size: "
            + str(round(size_merge >> 10, 3)) + " kB (" + str(round(size_merge * 100 / divZero(size_db1 + size_db2) - 100, 1)) + ")%\n")


# TODO: Reduktion des Fakten-Merging auf PA-Grösse  bzw. Separierung
# Das ist schwer, wenn die Analyse durch souffle direkt in DOOP ausgeführt wird, weil dann nicht erkennbar ist, welche Fakten-relationen genutzt werden
# bei Nemo/ souffle extern waeren das einfach alle importierten Dateien
# TODO: Reduzierung der PA-Merging auf Manuell gewählte Ergebnisse (die Aussagekräftig sind)