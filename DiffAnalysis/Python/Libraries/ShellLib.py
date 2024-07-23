import re
import glob
import os
from Python.Libraries.Classes import *
from pathlib import Path
from Python.Libraries import PathLib
import shutil
import subprocess
from prettytable import PrettyTable
import pandas as pd

# Shell commands
def clear_directory(directory):
    if directory.exists():
        shutil.rmtree(str(directory))
    os.system("mkdir -p " + str(directory))

def init_synth_souffle_database(db_config, db_name, fact_path):
    gen_facts_path = PathLib.datalog_programs_path.joinpath(db_config.db_type).joinpath(db_config.dir_name)
    os.chdir(gen_facts_path)
    command = ["./gen_facts.sh","small",str(fact_path)]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

def create_input_facts(db_config, db_dir_name, db_file_name, fact_path):
    if db_config.db_type == "DoopProgramAnalysis":
        create_doop_facts(db_config, db_dir_name,db_file_name, fact_path)
    elif db_config.db_type == "SouffleSynthetic":
        init_synth_souffle_database(db_config, db_dir_name,fact_path)
    print("initialized database: " + db_dir_name)

def create_doop_facts(db_config, db_name, db_file_name,fact_path):
    os.chdir(PathLib.DOOP_BASE)
    clear_directory(fact_path)

    java_path = Path.joinpath(PathLib.java_source_dir, db_config.dir_name).joinpath(db_name).joinpath(db_file_name + ".java")
    jar_path = Path.joinpath(PathLib.java_source_dir, db_config.dir_name).joinpath(db_name).joinpath(db_file_name + ".jar")
    if os.path.isfile(java_path):
        os.system("bin/mkjar " + str(java_path)
                  + " 1.8 " + str(jar_path.parents[0]))#+ ">/dev/null 2>&1")
    else:
        print("No Java-file found, use .jar ")
    if not os.path.isfile(jar_path):
        raise FileNotFoundError("Java & Jar File do not exist: " + str(java_path) + str(jar_path))
    # cannot name the java or jar files appart bc. javac would complain that Class name & file-name differ
    doop_out_name = db_config.dir_name + "_" + db_name

    os.system("./doop -a context-insensitive -i " + str(jar_path) + " --id " + str(doop_out_name) + " --facts-only --Xfacts-subset APP --cache --generate-jimple")

    for file in PathLib.DOOP_OUT.joinpath(doop_out_name).joinpath("database").glob("*.facts"):
        new_file_name = file.with_suffix('.tsv').name
        target_file = fact_path.joinpath(new_file_name)
        shutil.copy(file, target_file)

def chase_nemo(dl_rule_path, fact_path, result_path):
    if not dl_rule_path:
        return
    command = [str(PathLib.NEMO_ENGINE.joinpath("target/release/nmo")), str(dl_rule_path), "-I", str(fact_path), "-D", str(result_path), "--overwrite-results", "-e", "keep"]
    p = subprocess.run(command,capture_output=True)
    if p.returncode != 0:
        raise ChildProcessError(p.stderr.decode("utf-8"))

    nemo_runtime = split_nemo_stdout(p.stdout)
    os.chdir(PathLib.DOOP_BASE)
    return nemo_runtime

# parse Nemo output for runtimes
def split_nemo_stdout(stdout):
    stdout = stdout.decode("utf-8")
    stdout = stdout.split("\n")
    nemo_runtime = [re.search('[0-9m]*ms', stdout[0]).group(0), re.search('[0-9m]*ms', stdout[1]).group(0),
         re.search('[0-9m]*ms', stdout[2]).group(0), re.search('[0-9m]*ms', stdout[3]).group(0)]
    return nemo_runtime


def print_nemo_runtime(runtime):
    t = PrettyTable()
    t.field_names = ["Program Analysis","DB", "Total Reasoning", "Loading Input","Reasoning","Saving Output"]
    t.add_rows(runtime)
    print(t)


class GlobalLogger:
    def __init__(self):
        result_path = PathLib.base_out_path.joinpath("Results")
        self.path_single_db = result_path.joinpath("SingleDatabase.tsv")
        self.path_merge_db_df = result_path.joinpath("MergeDatabase.tsv")
        self.path_mapping_df = result_path.joinpath("Mappings.tsv")
        self.path_reasoning_df = result_path.joinpath("Reasoning.tsv")
    
    
        if self.path_single_db.exists():
            self.single_db_df = pd.read_csv(self.path_single_db, sep='\t', index_col=0, header=0)
        else:
            self.single_db_df = pd.DataFrame(columns=["name","Term-count" "Atom-count", "last-modified"])
    
        if self.path_merge_db_df.exists():
            self.merge_db_df = pd.read_csv(self.path_merge_db_df, sep='\t', index_col=0,header=0)
        else:
            self.merge_db_df = pd.DataFrame(columns=["MergeDB", "Db1 name", "DB2 name", "Mutual Termcount", "Mutual Atomcount"])
    
        if self.path_merge_db_df.exists():
            self.mapping_df = pd.read_csv(self.path_mapping_df, sep='\t', index_col=0,header=0)
        else:
            self.mapping_df = pd.DataFrame(columns=["MappingID","Date","SHA","MergeDB","Expansion","Metric","Expanded Tuples","% to crossproduct",
                                               "1-1 Mappings","Synthetic Mappings","Hub Re-Computation","Uncertain Mappings","Runtime"])
    
        if self.path_reasoning_df.exists():
            self.reasoning_df = pd.read_csv(self.path_reasoning_df, sep='\t',index_col=0, header=0)
        else:
            self.reasoning_df = pd.DataFrame(columns=["MappingID","Database","Date","SHA", "DL-Rules", "Total Time",  "Loading Time","Reasoning Time","Saving Time"])


    def saveResults(self):
        self.single_db_df.to_csv(self.path_single_db,sep='\t')
        self.merge_db_df.to_csv(self.path_merge_db_df,sep='\t')
        self.mapping_df.to_csv(self.path_mapping_df,sep='\t')
        self.reasoning_df.to_csv(self.path_reasoning_df,sep='\t')