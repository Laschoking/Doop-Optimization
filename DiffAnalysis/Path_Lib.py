from enum import Enum
from pathlib import Path
# This file defines all necessary paths for the comparison pipeline

# create path to doop base and its output dir
DOOP_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/"
DOOP_OUT_PATH = "/home/kotname/Documents/Diplom/Code/doop/master/out/"
NEMO_ENGINE_PATH = "/home/kotname/Documents/Diplom/Code/nemo/nemo"

#
java_source_dir = Path("/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/Java")

# this path will be the base for all of our file manipulation
BASE_PATH = Path("/home/kotname/Documents/Diplom/Code/doop/master/DiffAnalysis/out")

SOUFFLE_EXT_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_souffle/Analysis")
NEMO_BASE = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/Analysis")

PA_TYPES = Enum('PA_TYPE', ["SOUFFLE_INT","SOUFFLE_EXT","NEMO"])

class DB_Config:
    def __init__(self,class_name,db1_name,db2_name):
        self.class_name = class_name
        self.db1_name = db1_name
        self.db2_name = db2_name
class PA_Config:
    def __init__(self,pa_name, souffle_int_name, souffle_ext_name, nemo_name):
        self.pa_name = pa_name
        self.souffle_int_name = souffle_int_name
        self.souffle_ext_name = souffle_ext_name
        self.nemo_name = nemo_name
        self.souffle_ext_pa_path = Path.joinpath(SOUFFLE_EXT_BASE, souffle_ext_name)
        self.nemo_pa_path = Path.joinpath(NEMO_BASE, nemo_name)

DB_Pointer = DB_Config("Pointer", "Pointer1", "Pointer2")
DB_Example = DB_Config("Example", "Example1", "Example2")

PA_PointerAnalysis = PA_Config("PointerAnalysis", "context-insensitive", "pa-self-contained.dl", "PointerAnalyse.rls")
PA_Common_Facts_PointerAnalysis = PA_Config("CommonPointerAnalysis", "", "", "PointerAnalyse_merged.rls")
PA_ConstantPropAnalysis = PA_Config("ConstantPropagation", "", "", "")

class DB:
    def __init__(self, class_name, name, base_path,pa_name,engine):
        self.name = name
        # note: to compare the two dbs their names need to be the same (s.t. doop facts are similar)
        self.java_path = Path.joinpath(java_source_dir,name).joinpath(class_name + ".java")
        self.jar_path = Path.joinpath(java_source_dir,name).joinpath(class_name + ".jar")
        self.base_path = base_path.joinpath(name)
        # create paths to the facts of DOOP & the results of the analysis
        self.facts_path = self.base_path.joinpath("facts")
        self.jimple_path = self.base_path.joinpath("jimple")
        self.pa_path = self.base_path.joinpath("results").joinpath(engine.name).joinpath(pa_name)

class Analysis:
    def __init__(self,db_config, pa_config, engine):
        self.db_config = db_config
        self.pa_config = pa_config
        self.engine = engine
        appendix = db_config.db1_name + "_" + db_config.db2_name
        self.base_path = Path.joinpath(BASE_PATH, "Diff_" + appendix)

        self.db1 = DB(db_config.class_name, db_config.db1_name, self.base_path, pa_config.pa_name, self.engine)
        self.db2 = DB(db_config.class_name, db_config.db2_name, self.base_path, pa_config.pa_name, self.engine)

        # create path for the merge database (both for merged facts & merged PA-Results)
        merge_base_path = self.base_path.joinpath("merge")
        self.merge_facts_path = merge_base_path.joinpath("facts")
        self.merge_pa_path = merge_base_path.joinpath("results").joinpath(self.engine.name).joinpath(pa_config.pa_name)


        self.summary_facts_path = merge_base_path.joinpath("Summary_Facts.csv")
        self.summary_pa_path = self.merge_pa_path.joinpath("Summary_" + pa_config.pa_name + ".csv")

def printMetaInformation(analysis) -> Analysis:
    print("----------- META INFORMATION -----------")
    print("Compared databases: " + analysis.db1.name + " , " + analysis.db2.name )
    print("Program analysis: " + analysis.pa_config.pa_name + " Engine: " + analysis.engine.name)
    print("------------------------")