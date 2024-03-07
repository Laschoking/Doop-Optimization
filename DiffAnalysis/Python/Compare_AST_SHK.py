from Python.Classes import *
from Python.Merge_Lib import merge_directories, print_merge_stats
from Python import Shell_Lib


def create_facts(pa_config, fact_merge):
    Shell_Lib.clear_directory(fact_merge.merge_path)

    for fact_path, db_name in [fact_merge.db1_path, pa_config.db1_name], [
        fact_merge.db2_path, pa_config.db2_name]:
        Shell_Lib.clear_directory(fact_path)
        Shell_Lib.doop_create_facts(pa_config, db_name, fact_path)


# pa_config, facts1_path, result_path1, facts2_path, result_path2, merge_path, pa_config, engine
def run_separate_pa(pa_config, fact_merge, sep_pa_merge, engine):
    for fact_path, result_path in [fact_merge.dir1.path, sep_pa_merge.db1_path], [fact_merge.dir2.path, sep_pa_merge.db2_path]:
        Shell_Lib.clear_directory(result_path)
        if engine == Engine.SOUFFLE:
            Shell_Lib.run_souffle_pa(fact_path, result_path, pa_config.souffle_sep_path)

        if engine == Engine.NEMO:
            Shell_Lib.run_nemo_pa(fact_path, result_path, pa_config.nemo_sep_path)

    # (separate_pa_analysis, "PA",summary_writer, write_flag = True, split_flag = False)


def run_common_pa(pa_config, fact_path, result_path, engine):
    Shell_Lib.clear_directory(result_path)

    if engine == Engine.SOUFFLE:
        Shell_Lib.run_souffle_pa(fact_path, result_path, pa_config.souffle_merge_path)

    if engine == Engine.NEMO:
        Shell_Lib.run_nemo_pa(fact_path, result_path, pa_config.nemo_merge_path)


PointerAnalysis_Config = Config("Pointer", "Pointer1", "Pointer2", pa_name="PointerAnalysis",
                                souffle_sep_name="pa-self-contained.dl", souffle_merge_name="",
                                nemo_sep_name="PointerAnalyse.rls", nemo_merge_name="PointerAnalyse_merge.rls")

if __name__ == "__main__":
    # compare CFG results from AST tree (merged before computation vs merged after separate computation)
    pa1_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/sep")
    pa2_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/merge")
    compare_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/compare_res")
    summary_writer = ""
    compare_sep_merge_AST = MergeClass(pa1_result_path, pa2_result_path, compare_path, summary_writer)

    compare_sep_merge_AST = merge_directories(compare_sep_merge_AST, write_flag=False, split_flag=False)
    print_merge_stats(compare_sep_merge_AST, "AST: separate computation vs merged computation")


    # compare AST Reaching Definition Results (1 is separated computed & then merged, vs merged computation)

    pa1_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/data/ReDef/Schwarz/")
    pa2_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/data/ReDef/Schwarz_split/")
    compare_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/compare_res")
    summary_writer = ""
    compare_sep_merge_AST = MergeClass(pa1_result_path, pa2_result_path, compare_path, summary_writer)

    compare_sep_merge_AST = merge_directories(compare_sep_merge_AST, write_flag=False, split_flag=False)
    print_merge_stats(compare_sep_merge_AST, "AST: separate computation vs merged computation")
