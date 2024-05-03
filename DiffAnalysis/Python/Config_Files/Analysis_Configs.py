from Python.Libraries.Classes import *

analyses = {"nemo_CP_sep":{"engine" : Engine.NEMO,"pa": "ConstantPropagation_separate.rls"},
            "nemo_CP_merge": {"engine" : Engine.NEMO,"pa":"ConstantPropagation_merge.rls"},
            "souffle_CP_sep":{"engine" : Engine.SOUFFLE, "pa":"ConstantPropagation_nemo_copy.dl"},
            "nemo_PA_sep" : {"engine" : Engine.NEMO, "pa":"PointerAnalyse_separate.rls"},
            "nemo_PA_sep_v4": {"engine": Engine.NEMO, "pa": "PointerAnalyse_separate_v4.rls"},
            "souffle_PA_sep": {"engine" : Engine.SOUFFLE, "pa":"PointerAnalysis_or_self_contained.dl"},
            "nemo_PA_merge": {"engine" : Engine.NEMO, "pa":"PointerAnalyse_merge.rls"},
            "nemo_PA_merge_end_fold" : {"engine" : Engine.NEMO, "pa": "PointerAnalyse_merge_end_fold.rls"},
            "nemo_PA_merge_no_fold": {"engine": Engine.NEMO, "pa": "PointerAnalyse_merge_no_fold.rls"}
            }


ConstantPropagation12_Config = Config("Constants","Constants1","Constants2", pa_name="ConstantPropagation")

ConstantPropagation_Config_NEMO_SOUFFLE = Config("Constants", "Constants1", "Constants1", pa_name="ConstantPropagation")

PointerAnalysis12_Config = Config("Pointer", "Pointer1", "Pointer2", pa_name="PointerAnalysis")

PointerAnalysis21_Config = Config("Pointer", "Pointer2", "Pointer1", pa_name="PointerAnalysis")


PointerAnalysis12_Config_merge_vs_end_fold_merge = Config("Pointer", "Pointer1", "Pointer2", pa_name="PointerAnalysis")



PointerAnalysis34_Config = Config("Pointer", "Pointer3", "Pointer4", pa_name="PointerAnalysis")


PointerAnalysis_Config_NEMO_SOUFFLE = Config("Pointer", "Pointer1", "Pointer1", pa_name="PointerAnalysis")
