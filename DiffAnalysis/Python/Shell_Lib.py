import glob
import os
from Python.Classes import *
from pathlib import Path
import shutil


# depending on the PA, a big amount of Facts may not be relevant to the PA
# Thus we want to find the subset of fact-relations that is relevant to the current PA

# def reduceFacts():


def doop_create_facts(db_config, db_name, fact_path):
    os.chdir(DOOP_PATH)

    java_path = Path.joinpath(java_source_dir, db_name).joinpath(db_config.class_name + ".java")
    jar_path = Path.joinpath(java_source_dir, db_name).joinpath(db_config.class_name + ".jar")
    if os.path.isfile(java_path):
        os.system("bin/mkjar " + str(java_path)
                  + " 1.8 " + str(jar_path.parents[0]))
    else:
        raise FileNotFoundError("The input file does not exist " + str(java_path))
    #os.system("./doop -a context-insensitive -i " + str(jar_path) + " --id " + str(db_name) + " --facts-only --Xfacts-subset APP --cache --generate-jimple")

    for file in glob.glob(DOOP_OUT_PATH + db_name + "/database/*.facts"):
        shutil.copy(file, fact_path)


def run_souffle_pa(fact_path, result_path, souffle_ext_pa_path):
    clear_directory(result_path)
    os.system("souffle " + str(souffle_ext_pa_path) + " -F " + str(fact_path) + " -D " + str(result_path) + " -j4")


def run_nemo_pa(fact_path, result_path, nemo_pa_path):
    os.chdir(NEMO_ENGINE_PATH)
    clear_directory(result_path)
    os.system("target/debug/nmo " + str(nemo_pa_path) + " -I " + str(fact_path) + " -D " + str(
        result_path) + " --save-results --overwrite-results -q  --write-all-idb-predicates")  # >/dev/null 2>&1")
    os.chdir(DOOP_PATH)


def clear_directory(directory):
    # for file in list(dir.glob('*')):
    if directory.exists():
        shutil.rmtree(str(directory))
    os.system("mkdir -p " + str(directory))
