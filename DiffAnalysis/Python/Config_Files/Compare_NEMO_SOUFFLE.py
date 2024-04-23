from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import forward_bijection, print_merge_stats, print_nemo_runtime
from Analysis_Configs import *


if __name__ == "__main__":
    pa_config = ConstantPropagation_Config_NEMO_SOUFFLE

    engine1 = Engine.NEMO
    engine2 = Engine.SOUFFLE
    python_merge_path = pa_config.base_output_path.joinpath("python-merge")

    # Fact Creation & Merge
    facts1_path = pa_config.db1_path.joinpath("facts")
    facts2_path = pa_config.db2_path.joinpath("facts")
    facts_merge_path = python_merge_path.joinpath("facts")
    summary_writer = open("../summary.txt", "w")

    fact_merge = MergeClass(facts1_path, facts2_path, facts_merge_path, summary_writer)
    create_facts(pa_config, fact_merge)

    fact_merge = forward_bijection(fact_merge, write_flag=True, split_flag=False)
    print_merge_stats(fact_merge,pa_config.db1_name, pa_config.db2_name, "FACT MERGE")

    # Separate Program Analysis Creation & Merge
    pa1_result_path = pa_config.db1_path.joinpath("results").joinpath(engine1.name)
    pa2_result_path = pa_config.db2_path.joinpath("results").joinpath(engine2.name)
    sep_pa_merge_path = python_merge_path.joinpath("results").joinpath("NEMO_Souffle")
    #Shell_Lib.clear_directory(sep_pa_merge_path)
    sep_pa_merge = MergeClass(pa1_result_path, pa2_result_path, sep_pa_merge_path, summary_writer)
    sep_pa_runtime = run_separate_pa(pa_config, fact_merge, sep_pa_merge, engine1,engine2)
    sep_pa_merge = forward_bijection(sep_pa_merge, write_flag=True, split_flag=False)
    print_merge_stats(sep_pa_merge, engine1.name, engine2.name,"Pointer1 NEMO vs. Souffle")
    print_nemo_runtime(sep_pa_runtime,pa_config.nemo_sep_name)
