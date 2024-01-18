# This file defines all necessary paths for the comparation pipeline

# The two input sources that will be compared
# Only those 2 lines need to be changed
CLASS_NAME = "Example"
DB1_NAME = "Example1"
DB2_NAME = "Example2"
PA_NAME = "context-insensitive"

# create path to doop base and its output dir
DOOP_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/"
DOOP_OUT_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/out/"

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
PA1_PATH = BASE_PATH + DB1_NAME + "/results/" + PA_NAME + "/"

FACTS2_PATH = BASE_PATH + DB2_NAME + "/facts/"
JIMPLE2_PATH = BASE_PATH + DB2_NAME + "/jimple/"
PA2_PATH = BASE_PATH + DB2_NAME + "/results/" + PA_NAME + "/"

# create path for the merge database (both for merged facts & merged PA-Results)
MERGE_BASE_PATH = BASE_PATH + "merge/"
MERGE_FACTS_PATH = MERGE_BASE_PATH + "facts/"
MERGE_PA_PATH = MERGE_BASE_PATH + "results/" + PA_NAME + "/"
