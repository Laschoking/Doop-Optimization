
from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import *


if __name__ == "__main__":
    # compare CFG results from AST tree (merged before computation vs merged after separate computation)
    pa1_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/sep")
    pa2_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/merge")
    compare_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/compare_res")
    summary_writer = ""
    compare_sep_merge_AST = MergeClass(pa1_result_path, pa2_result_path, compare_path, summary_writer)

    compare_sep_merge_AST = forward_bijection(compare_sep_merge_AST, write_flag=False, debug_flag=False)
    print_merge_stats(compare_sep_merge_AST, "AST: separate computation vs merged computation")


    # compare AST Reaching Definition Results (1 is separated computed & then merged, vs merged computation)

    pa1_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/data/ReDef/Schwarz/")
    pa2_result_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/data/ReDef/Schwarz_split/")
    compare_path = Path("/home/kotname/Documents/Diplom/Code/ex_nemo/cpec/AST-Diffing/comp_sep_merge/compare_res")
    summary_writer = ""
    compare_sep_merge_AST = MergeClass(pa1_result_path, pa2_result_path, compare_path, summary_writer)

    compare_sep_merge_AST = forward_bijection(compare_sep_merge_AST, write_flag=False, debug_flag=False)
    print_merge_stats(compare_sep_merge_AST, "AST: separate computation vs merged computation")
