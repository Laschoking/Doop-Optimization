from Python.Libraries.Classes import *

analyses = {"nemo_CP_sep":{"pa": "ConstantPropagation_separate.rls","blocked_terms" : {}},
            "nemo_CP_merge": {"pa":"ConstantPropagation_merge.rls","blocked_terms" : {}},

            "nemo_PA_sep" : {"pa":"PointerAnalyse_separate.rls","blocked_terms" : {'',' ',"<clinit>", "void()","public","static","main","void(java.lang.String[])","java.io.Serializable","java.lang.Cloneable","java.lang.Object","abstract"}},
            "nemo_PA_merge_end_fold" : { "pa": "PointerAnalyse_merge_end_fold.rls","blocked_terms" : {'',' ',"<clinit>", "void()","public","static","main","void(java.lang.String[])","java.io.Serializable","java.lang.Cloneable","java.lang.Object","abstract"}},
            "nemo_PA_merge_no_fold": {"pa": "PointerAnalyse_merge_no_fold.rls", "blocked_terms" : {'',' ',"<clinit>", "void()","public","static","main","void(java.lang.String[])","java.io.Serializable","java.lang.Cloneable","java.lang.Object","abstract"}},

            "nemo_CFG_merge" : {"pa": "nemo-merged-cfg.rls", "blocked_terms" : {'',' ',"abstract","<sun.misc.ProxyGenerator: byte[] generateClassFile()>"}},
            "nemo_CFG_sep": {"pa": "nemo-separate-cfg.rls", "blocked_terms" : {'',' ',"abstract","<sun.misc.ProxyGenerator: byte[] generateClassFile()>"}}
            }


Constants = Config("Constants","v1","v2")

Simple_Pointer = Config("Simple_Pointer", "v1", "v2")

Simple_Java_Calculator = Config("Simple_Java_Calculator", "v3_0", "v3_1_1")

Gocd_Websocket_Notifier_v1_v4 = Config("Gocd_Websocket_Notifier", "v0_1", "v0_4_2")

Gocd_Websocket_Notifier_v3_v4 = Config("Gocd_Websocket_Notifier", "v0_3", "v0_4_2")