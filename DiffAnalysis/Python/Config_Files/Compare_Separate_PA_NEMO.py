from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import *
from Python.Config_Files.Analysis_Configs import *

if __name__ == "__main__":
    db_config = PointerAnalysis12_Config
    python_merge_path = db_config.base_output_path.joinpath("python-merge")

    # Fact Creation & Merge
    facts1_path = db_config.db1_path.joinpath("facts")
    facts2_path = db_config.db2_path.joinpath("facts")
    facts_merge_path = python_merge_path.joinpath("facts")
    summary_writer = open("../summary.txt", "w")

    fact_merge = MergeClass(facts1_path, facts2_path, facts_merge_path, summary_writer)
    create_facts(db_config, fact_merge)

    file_pairs,bijection = forward_bijection(fact_merge, write_flag=True, debug_flag=False)
    #print_merge_stats(fact_merge,db_config.db1_name, db_config.db2_name, "FACT MERGE")

    # Separate Program Analysis
    pa_sep = analyses["nemo_PA_sep"]
    pa1_result_path = db_config.db1_path.joinpath("results").joinpath(pa_sep["engine"].name)
    pa2_result_path = db_config.db2_path.joinpath("results").joinpath(pa_sep["engine"].name)
    sep_pa_merge_path = python_merge_path.joinpath("results").joinpath(pa_sep["engine"].name)

    sep_pa_merge = MergeClass(pa1_result_path, pa2_result_path, sep_pa_merge_path, summary_writer)


    sep_pa_runtime = run_single_pa(pa_sep,fact_merge.dir1.path, sep_pa_merge.db1_path)
    sep_pa_runtime += run_single_pa(pa_sep,fact_merge.dir2.path, sep_pa_merge.db2_path)
    print_nemo_runtime(sep_pa_runtime,pa_sep["pa"])

    rev_pa_db = reverse_bijection_on_pa(file_pairs, bijection)
    #evaluation = evaluate_bijection()




