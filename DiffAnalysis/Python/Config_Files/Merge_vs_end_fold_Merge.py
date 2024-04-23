from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import *
from Python.Config_Files.Analysis_Configs import *
# we want to evaluate the Merge-version that tries to fold relations immediately
# with the Merge-version, that folds at the end (thus creates more facts)

if __name__ == "__main__":
    pa_config = PointerAnalysis12_Config_merge_vs_end_fold_merge

    engine = Engine.NEMO
    python_merge_path = pa_config.base_output_path.joinpath("python-merge")

    # Fact Creation & Merge
    facts1_path = pa_config.db1_path.joinpath("facts")
    facts2_path = pa_config.db2_path.joinpath("facts")
    facts_merge_path = python_merge_path.joinpath("facts")
    summary_writer = open("../summary.txt", "w")

    fact_merge = MergeClass(facts1_path, facts2_path, facts_merge_path, summary_writer)
    create_facts(pa_config, fact_merge)

    fact_merge = forward_bijection(fact_merge, write_flag=True, debug_flag=False)
    print_merge_stats(fact_merge,pa_config.db1_name, pa_config.db2_name, "FACT MERGE")





    # Common Program Analysis Creation & Merge
    common_result_path = pa_config.base_output_path.joinpath("common_pa")
    # here we run only 1 PA -> so just pass the paths directly
    common_pa_runtime = run_single_pa(pa_config, fact_merge.merge_dir.path, common_result_path, engine)

    common_pa_merge = MergeClass(sep_pa_merge.merge_dir.path, common_result_path, python_merge_path.joinpath("common_merge"), summary_writer)
    common_pa_merge = forward_bijection(common_pa_merge, write_flag=True, debug_flag=True)
    print_merge_stats(common_pa_merge,sep_pa_merge.merge_dir.path.parts[-3], common_result_path.parts[-1],"Comparison: Merged PA vs. separate PA")
    print_nemo_runtime(common_pa_runtime,pa_config.nemo_merge_name)
