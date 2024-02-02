from enum import Enum
# This file defines all necessary paths for the comparation pipeline

PA_TYPES = Enum('PA_TYPE', ["SOUFFLE_INT","SOUFFLE_EXT","NEMO"])


# The two input sources that will be compared
# ------------------------------------------------ #
# -------- variables to adapt -------------------- #
CLASS_NAME = "Example"
DB1_NAME = "Example1"
DB2_NAME = "Example2"

# define the type of analysis you want to run
PA_TYPE = PA_TYPES.SOUFFLE_EXT

# general PA-Name
PA_NAME = "ConstantPropagation"

PA_NAME_SOUFFLE_INT = "context-insensitive"
# SOUFFLE_EXT:
PA_NAME_SOUFFLE_EXT = "Liveness.dl"
# Nemo:
PA_NAME_NEMO = "ConstantPropagation.rls"
PA_PATH_SOUFFLE_EXT = "/home/kotname/Documents/Diplom/Code/ex_souffle/Analysis/Liveness/" + PA_NAME_SOUFFLE_EXT
PA_PATH_NEMO = "/home/kotname/Documents/Diplom/Code/ex_nemo/Analysis/ClassicDoopAnalysis/" + PA_NAME_NEMO

PA_RELEVANT_FACT_FILES = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/RelevantFilesPA/" + PA_TYPE.name + "/relevant_facts.csv"
PA_RELEVANT_RESULT_FILES = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/RelevantFilesPA/" + PA_TYPE.name + "/relevant_results.csv"


# -------- variables to adapt -------------------- #
# ------------------------------------------------ #

# create path to doop base and its output dir
DOOP_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/"
DOOP_OUT_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/out/"

NEMO_ENGINE_PATH = "/home/kotname/Documents/Diplom/Code/nemo/nemo"


# This list holds the names of all 133 relations which doop outputs as fact-relations
FACT_LIST = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/facts.txt"

# this path will be the base for all of our file manipulation
BASE_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/out/Diff_" + DB1_NAME + "_" + DB2_NAME + "/"

# create path for input source code (either .java or .jar) for doop
# note: javac compiles only if class name equals file name
# doop takes the class & method name for each statement, so to compare 2 db they need to have same signature
# -> thats why we need extra folders to separate /DiffAnalysis/Java/Example1/Example.java & /DiffAnalysis/Java/Example2/Example.java
JAVA1_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/Java/" + DB1_NAME + "/" + CLASS_NAME + ".java"
JAR1_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/Java/" + DB1_NAME + "/" + CLASS_NAME + ".jar"

JAVA2_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/Java/" + DB2_NAME + "/" + CLASS_NAME + ".java"
JAR2_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/Java/" + DB2_NAME + "/" + CLASS_NAME + ".jar"

# create paths to the facts of DOOP & the results of the analysis
FACTS1_PATH = BASE_PATH + DB1_NAME + "/facts/"
JIMPLE1_PATH = BASE_PATH + DB1_NAME + "/jimple/"
PA1_PATH = BASE_PATH + DB1_NAME + "/results/" + PA_TYPE.name + "/" + PA_NAME + "/"

FACTS2_PATH = BASE_PATH + DB2_NAME + "/facts/"
JIMPLE2_PATH = BASE_PATH + DB2_NAME + "/jimple/"
PA2_PATH = BASE_PATH + DB2_NAME + "/results/" + PA_TYPE.name + "/" + PA_NAME + "/"

# create path for the merge database (both for merged facts & merged PA-Results)
MERGE_BASE_PATH = BASE_PATH + "merge/"
MERGE_FACTS_PATH = MERGE_BASE_PATH + "facts/"
MERGE_PA_PATH = MERGE_BASE_PATH + "results/" + PA_TYPE.name + "/" + PA_NAME + "/"
