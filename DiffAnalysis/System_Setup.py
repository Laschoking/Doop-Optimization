import glob
import os
from Path_Lib import *
from pathlib import Path
import shutil
from Lib_Functions import printMetaInformation

# depending on the PA, a big amount of Facts may not be relevant to the PA
# Thus we want to find the subset of fact-relations that is relevant to the current PA

#def reduceFacts():
def Create_Dirs(analysis) -> Analysis:
    os.system("mkdir -p " + str(analysis.merge_facts_path))
    os.system("mkdir -p " + str(analysis.merge_pa_path))
    for db in [analysis.db1, analysis.db2]:
        os.system("mkdir -p " + str(db.facts_path))
        os.system("mkdir -p " + str(db.pa_path))
        os.system("mkdir -p " + str(db.jimple_path))


def DOOP_Create_Facts(analysis) -> Analysis:
    os.chdir(DOOP_PATH)

    for db in [analysis.db1, analysis.db2]:
        #if not os.path.isfile(db.jar_path):
        if os.path.isfile(db.java_path):
            os.system("bin/mkjar " + str(db.java_path)
                      + " 1.8 " + str(db.jar_path.parents[0]))
        else:
            raise FileNotFoundError("The input file does not exist " + str(db.java_path))
        if analysis.engine != PA_TYPES.SOUFFLE_INT:
            #os.system("./doop -a  " + str(analysis.pa_config.souffle_int_name) + " -i " + str(db.jar_path) + " --id " + str(db.name) + " --facts-only --Xfacts-subset APP --cache --generate-jimple")

            for file in glob.glob(DOOP_OUT_PATH + db.name + "/database/*.facts"):
                shutil.copy(file, db.facts_path)

            for file in glob.glob(DOOP_OUT_PATH + db.name + "/database/jimple/*"):
                shutil.copy(file, db.jimple_path)
    printMetaInformation(analysis)

def Run_SOUFFLE_INT_PA(analysis) -> Analysis:
    for db in [analysis.db1, analysis.db2]:
        os.system("./doop -a  " + str(analysis.pa_config.souffle_int_name) + " -i " + str(db.jar_path) + " --id " + str(db.name) + " --Xfacts-subset APP --cache --generate-jimple")

        # move PA-Resuls to target directory ( only necessary for souffle_int)
        for file in glob.glob(DOOP_OUT_PATH + db.name + "/database/*.csv"):
            shutil.copy(file, analysis.pa_path)

        for file in glob.glob(DOOP_OUT_PATH + db.name + "/database/*.facts"):
            shutil.copy(file, db.facts_path)

        for file in glob.glob(DOOP_OUT_PATH + db.name + "/database/jimple/*"):
            shutil.copy(file, db.jimple_path)

def Run_SOUFFLE_EXT_PA(analysis) -> Analysis:
    for db in [analysis.db1, analysis.db2]:
        # once DOOP generated facts, run souffle 2.1 externally on given PA
        os.system("souffle " + str(SOUFFLE_EXT_BASE.joinpath(analysis.pa_config.souffle_ext_name)) + " -F " + str(db.facts_path) + " -D " + str(db.pa_path) + " -j4")
        if analysis.pa_config.pa_name == "PointerAnalysis":
            # copy 2 files from souffle pa to facts, so NEMO can use them
            method_descriptor = db.pa_path.joinpath("Method_Descriptor.csv")
            main_class = db.pa_path.joinpath("MainClass.csv")
            #if (method_descriptor.is_file() and main_class.is_file()):
            #    shutil.copy(str(method_descriptor), str(db.facts_path))
            #    shutil.copy(str(main_class), str(db.facts_path))


def Run_NEMO_SINGLE_PA(nemo_pa_path,facts_path,pa_path):

    os.chdir(NEMO_ENGINE_PATH)
    os.system("target/debug/nmo " + str(nemo_pa_path) + " -I " + str(facts_path) + " -D " + str(
        pa_path) + " --save-results --overwrite-results -q --write-all-idb-predicates ")  # >/dev/null 2>&1")
    os.chdir(DOOP_PATH)


def Run_NEMO_PA(analysis) -> Analysis:
    for db in [analysis.db1, analysis.db2]:
        os.chdir(NEMO_ENGINE_PATH)
        os.system("target/debug/nmo " + str(analysis.pa_config.nemo_pa_path) + " -I " + str(db.facts_path) + " -D " + str(db.pa_path) + " --save-results --overwrite-results -q ") #>/dev/null 2>&1")
        os.chdir(DOOP_PATH)
