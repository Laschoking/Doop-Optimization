import csv
import os
from pathlib import Path, PurePosixPath, PurePath
from Path_Lib import *
from Lib_Functions import merge_directories,divZero
import System_Setup
import glob


if __name__ == '__main__':
    analysis = Analysis(DB_Pointer,PA_PointerAnalysis,PA_TYPES.NEMO)
    match analysis.engine:
        case PA_TYPES.SOUFFLE_INT:
            System_Setup.SOUFFLE_INT(analysis)
        case PA_TYPES.SOUFFLE_EXT:
            System_Setup.Run_SOUFFLE_EXT_PA(analysis)
        case PA_TYPES.NEMO:
            System_Setup.Run_NEMO_PA(analysis)

    merge_directories(analysis.db1.pa_path, analysis.db2.pa_path, analysis.merge_pa_path, "PA")

