# This file defines all necessary paths for the comparison pipeline
from pathlib import Path
from enum import Enum

# create path to doop base and its output dir
DOOP_BASE = Path("/home/kotname/Documents/Diplom/Code/doop/master/")
DOOP_OUT = Path("/home/kotname/Documents/Diplom/Code/doop/master/out/")
NEMO_ENGINE = Path("/home/kotname/Documents/Diplom/Code/nemo/nemo")

#

# this path will be the base for all of our file manipulation
base_diff_path = Path("/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis")
base_out_path = base_diff_path.joinpath("out")
java_source_dir = base_diff_path.joinpath("Java")

SOUFFLE_ANALYSIS_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_souffle/Analysis")
NEMO_ANALYSIS_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/Analysis")
base_dir = "/out/"

Engine = Enum("Engine",["SOUFFLE", "NEMO"])
NR_LEFT = 1
NR_RIGHT = 10
NR_TARGET = 0
