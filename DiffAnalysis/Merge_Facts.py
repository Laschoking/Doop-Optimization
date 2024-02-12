import csv
import os
from pathlib import Path, PurePosixPath, PurePath
from Path_Lib import *
from Lib_Functions import merge_directories,divZero
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
    #summary_writer = open(Analysis.summary_facts_path, "w")
    merge_directories(analysis.db1.facts_path, analysis.db2.facts_path, analysis.merge_facts_path, "FACTS")

    if analysis.engine == PA_TYPES.SOUFFLE_INT:
        System_Setup.SOUFFLE_INT(analysis)

    if analysis.engine == PA_TYPES.SOUFFLE_EXT:
        System_Setup.Run_SOUFFLE_EXT_PA(analysis)

    if analysis.engine == PA_TYPES.NEMO:
        System_Setup.Run_NEMO_PA(analysis)

    merge_directories(analysis.db1.pa_path, analysis.db2.pa_path, analysis.merge_pa_path, "PA")
