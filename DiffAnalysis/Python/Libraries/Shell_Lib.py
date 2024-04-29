import re
import glob
import os
from Python.Libraries.Classes import *
from pathlib import Path
import shutil
import subprocess

# Intermediate Functions
def create_facts(db_config,db1_path, db2_path):
    doop_create_facts(db_config, db_config.db1_name, db1_path)
    doop_create_facts(db_config, db_config.db2_name, db2_path)

def run_single_pa(pa_config, fact_path, result_path):
    #clear_directory(result_path)
    runtime = {}

    if pa_config["engine"] == Engine.SOUFFLE:
        run_souffle_pa(SOUFFLE_ANALYSIS_BASE.joinpath(pa_config["pa"]), fact_path, result_path)

    if pa_config["engine"] == Engine.NEMO:
        runtime = run_nemo_pa(NEMO_ANALYSIS_BASE.joinpath(pa_config["pa"]), fact_path, result_path)
    return [[fact_path.parts[-2]] + runtime]

# Shell commands
def clear_directory(directory):
    if directory.exists():
        shutil.rmtree(str(directory))
    os.system("mkdir -p " + str(directory))

def doop_create_facts(db_config, db_name, fact_path):
    os.chdir(DOOP_BASE)
    #clear_directory(fact_path)

    java_path = Path.joinpath(java_source_dir, db_name).joinpath(db_config.class_name + ".java")
    jar_path = Path.joinpath(java_source_dir, db_name).joinpath(db_config.class_name + ".jar")
    if os.path.isfile(java_path):
        os.system("bin/mkjar " + str(java_path)
                  + " 1.8 " + str(jar_path.parents[0]) )#+ ">/dev/null 2>&1")
    else:
        raise FileNotFoundError("The input file does not exist " + str(java_path))
    #os.system("./doop -a context-insensitive -i " + str(jar_path) + " --id " + str(db_name) + " --facts-only --Xfacts-subset APP --cache --generate-jimple")

    for file in DOOP_OUT.joinpath(db_name).joinpath("database").glob("*.facts"):
        shutil.copy(file, fact_path)

def run_souffle_pa(pa_path,fact_path, result_path):
    clear_directory(result_path)
    command= ["souffle", str(pa_path),"-F", str(fact_path),"-D",str(result_path),"-j4"]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

    os.chdir(result_path)
    os.system("rename 's/basic.//' *")

def run_nemo_pa(pa_path,fact_path, result_path):
    #os.chdir(NEMO_ENGINE)
    #clear_directory(result_path)
    command = [str(NEMO_ENGINE.joinpath("target/release/nmo")), str(pa_path), "-I", str(fact_path), "-D", str(result_path), "--overwrite-results", "-e", "keep"]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

    Dict = split_nemo_stdout(p.stdout)
    os.chdir(DOOP_BASE)
    return Dict

# parse Nemo output for runtimes
def split_nemo_stdout(stdout):
    stdout = stdout.decode("utf-8")
    stdout = stdout.split("\n")
    D = []
    D.append(re.search('[0-9m]*ms',stdout[0]).group(0))
    D.append(re.search('[0-9m]*ms',stdout[1]).group(0))
    D.append(re.search('[0-9m]*ms',stdout[2]).group(0))
    D.append(re.search('[0-9m]*ms',stdout[3]).group(0))
    return D