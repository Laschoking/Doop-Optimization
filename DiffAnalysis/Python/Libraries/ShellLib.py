import re
import glob
import os
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import PathLib
import shutil
import subprocess
from prettytable import PrettyTable

# Shell commands
def clear_directory(directory):
    if directory.exists():
        shutil.rmtree(str(directory))
    os.system("mkdir -p " + str(directory))

# Intermediate Functions
def create_facts(db_config,db1_path, db2_path):
    doop_create_facts(db_config, db_config.db1_name, db1_path)
    doop_create_facts(db_config, db_config.db2_name, db2_path)
def doop_create_facts(db_config, db_name, fact_path):
    os.chdir(PathLib.DOOP_BASE)
    #clear_directory(fact_path)

    java_path = Path.joinpath(PathLib.java_source_dir, db_config.dir_name).joinpath(db_name).joinpath(db_config.dir_name + ".java")
    jar_path = Path.joinpath(PathLib.java_source_dir, db_config.dir_name).joinpath(db_name).joinpath(db_config.dir_name + ".jar")
    if os.path.isfile(java_path):
        os.system("bin/mkjar " + str(java_path)
                  + " 1.8 " + str(jar_path.parents[0]))#+ ">/dev/null 2>&1")
    else:
        print("No Java-file found, use .jar ")
    if not os.path.isfile(jar_path):
        raise FileNotFoundError("Java & Jar File do not exist: " + str(java_path) + str(jar_path))
    os.system("./doop -a context-insensitive -i " + str(jar_path) + " --id " + str(db_name) + " --facts-only --Xfacts-subset APP --cache --generate-jimple")

    for file in PathLib.DOOP_OUT.joinpath(db_name).joinpath("database").glob("*.facts"):
        new_file_name = file.with_suffix('.tsv').name
        target_file = fact_path.joinpath(new_file_name)
        shutil.copy(file, target_file)



'''def run_souffle_pa(pa_path,fact_path, result_path):
    clear_directory(result_path)
    command= ["souffle", str(pa_path),"-F", str(fact_path),"-D",str(result_path),"-j4"]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

    os.chdir(result_path)
    os.system("rename 's/basic.//' *")
'''

def chase_nemo(pa_config, fact_path, result_path):
    pa_path = PathLib.NEMO_ANALYSIS_BASE.joinpath(pa_config["pa"])
    command = [str(PathLib.NEMO_ENGINE.joinpath("target/release/nmo")), str(pa_path), "-I", str(fact_path), "-D", str(result_path), "--overwrite-results", "-e", "keep"]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

    Dict = split_nemo_stdout(p.stdout)
    os.chdir(PathLib.DOOP_BASE)
    return [pa_config["pa"]] + [fact_path.parts[-2:]] + Dict

# parse Nemo output for runtimes
def split_nemo_stdout(stdout):
    stdout = stdout.decode("utf-8")
    stdout = stdout.split("\n")
    D = [re.search('[0-9m]*ms', stdout[0]).group(0), re.search('[0-9m]*ms', stdout[1]).group(0),
         re.search('[0-9m]*ms', stdout[2]).group(0), re.search('[0-9m]*ms', stdout[3]).group(0)]
    return D


def print_nemo_runtime(runtime):
    t = PrettyTable()
    t.field_names = ["Program Analysis","DB", "Total Reasoning", "Loading Input","Reasoning","Saving Output"]
    t.add_rows(runtime)
    print(t)

