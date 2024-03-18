from Python.Classes import *
from Python.Merge_Lib import merge_directories, print_merge_stats,print_nemo_runtime
from Python import Shell_Lib


def create_facts(pa_config, fact_merge):
    Shell_Lib.clear_directory(fact_merge.merge_path)

    for fact_path, db_name in [fact_merge.db1_path, pa_config.db1_name], [fact_merge.db2_path, pa_config.db2_name]:
        Shell_Lib.clear_directory(fact_path)
        Shell_Lib.doop_create_facts(pa_config, db_name, fact_path)


# pa_config, facts1_path, result_path1, facts2_path, result_path2, merge_path, pa_config, engine
def run_separate_pa(pa_config, fact_merge, sep_pa_merge, engine1,engine2):
    runtime = []

    for fact_path, result_path,db_name,engine in [fact_merge.dir1.path, sep_pa_merge.db1_path,pa_config.db1_name,engine1], \
                                                 [fact_merge.dir2.path, sep_pa_merge.db2_path,pa_config.db2_name,engine2]:
        Shell_Lib.clear_directory(result_path)
        if engine == Engine.SOUFFLE:
            Shell_Lib.run_souffle_pa(fact_path, result_path, pa_config.souffle_sep_path)

        if engine == Engine.NEMO:
            runtime.append([db_name] + Shell_Lib.run_nemo_pa(fact_path, result_path, pa_config.nemo_sep_path))

    # (separate_pa_analysis, "PA",summary_writer, write_flag = True, split_flag = False)

    return runtime

def run_common_pa(pa_config, fact_path, result_path, engine):
    Shell_Lib.clear_directory(result_path)
    runtime = {}

    if engine == Engine.SOUFFLE:
        Shell_Lib.run_souffle_pa(fact_path, result_path, pa_config.souffle_merge_path)

    if engine == Engine.NEMO:
        runtime = Shell_Lib.run_nemo_pa(fact_path, result_path, pa_config.nemo_merge_path)
    return [[fact_path.parts[-2]] + runtime]

ConstantPropagation_Config = Config("Example","Example1","Example2", pa_name="ConstantPropagation",
                                souffle_sep_name="ConstantPropagation.dl", souffle_merge_name="",
                                nemo_sep_name="ConstantPropagation_separate.rls", nemo_merge_name="ConstantPropagation_merge.rls")

PointerAnalysis12_Config = Config("Pointer", "Pointer1", "Pointer2", pa_name="PointerAnalysis",
                                souffle_sep_name="pa-self-contained.dl", souffle_merge_name="",
                                nemo_sep_name="PointerAnalyse_separate.rls", nemo_merge_name="PointerAnalyse_merge.rls")

PointerAnalysis34_Config = Config("Pointer", "Pointer3", "Pointer4", pa_name="PointerAnalysis",
                                souffle_sep_name="pa-self-contained.dl", souffle_merge_name="",
                                nemo_sep_name="PointerAnalyse_separate.rls", nemo_merge_name="PointerAnalyse_merge.rls")

if __name__ == "__main__":
    pa_config = PointerAnalysis12_Config

    engine = Engine.NEMO
    python_merge_path = pa_config.base_output_path.joinpath("python-merge")

    # Fact Creation & Merge
    facts1_path = pa_config.db1_path.joinpath("facts")
    facts2_path = pa_config.db2_path.joinpath("facts")
    facts_merge_path = python_merge_path.joinpath("facts")
    summary_writer = open("summary.txt", "w")

    fact_merge = MergeClass(facts1_path, facts2_path, facts_merge_path, summary_writer)
    create_facts(pa_config, fact_merge)

    fact_merge = merge_directories(fact_merge, write_flag=True, split_flag=False)
    print_merge_stats(fact_merge,pa_config.db1_name, pa_config.db2_name, "FACT MERGE")

    # Separate Program Analysis Creation & Merge
    pa1_result_path = pa_config.db1_path.joinpath("results").joinpath(engine.name)
    pa2_result_path = pa_config.db2_path.joinpath("results").joinpath(engine.name)
    sep_pa_merge_path = python_merge_path.joinpath("results").joinpath(engine.name)
    #Shell_Lib.clear_directory(sep_pa_merge_path)
    sep_pa_merge = MergeClass(pa1_result_path, pa2_result_path, sep_pa_merge_path, summary_writer)
    sep_pa_runtime = run_separate_pa(pa_config, fact_merge, sep_pa_merge, engine,engine)
    sep_pa_merge = merge_directories(sep_pa_merge, write_flag=True, split_flag=False)
    print_merge_stats(sep_pa_merge, pa_config.db1_name, pa_config.db2_name,"Separate PA & Merge")
    print_nemo_runtime(sep_pa_runtime,pa_config.nemo_sep_name)

    # Common Program Analysis Creation & Merge
    common_result_path = pa_config.base_output_path.joinpath("common_pa")
    # here we run only 1 PA -> so just pass the paths directly
    common_pa_runtime = run_common_pa(pa_config, fact_merge.merge_dir.path, common_result_path, engine)
    common_pa_merge = MergeClass(sep_pa_merge.merge_dir.path, common_result_path, python_merge_path.joinpath("common_merge"), summary_writer)
    common_pa_merge = merge_directories(common_pa_merge, write_flag=True, split_flag=False)
    print_merge_stats(common_pa_merge,sep_pa_merge.merge_dir.path.parts[-3], common_result_path.parts[-1],"Comparison: Merged PA vs. separate PA")
    print_nemo_runtime(common_pa_runtime,pa_config.nemo_merge_name)
