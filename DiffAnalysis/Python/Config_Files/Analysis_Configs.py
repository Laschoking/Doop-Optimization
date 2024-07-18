from Python.Libraries.Classes import *

class DB_Config:
    def __init__(self, db_type, dir_name, db1_dir_name, db2_dir_name,db1_file_name=None, db2_file_name=None):
        self.db_type = db_type
        self.dir_name = dir_name
        self.base_output_path = PathLib.base_out_path.joinpath(db_type).joinpath(dir_name).joinpath(db1_dir_name + "_" + db2_dir_name)
        self.db1_dir_name = db1_dir_name
        self.db2_dir_name = db2_dir_name
        self.db1_path = self.base_output_path.joinpath(db1_dir_name)
        self.db2_path = self.base_output_path.joinpath(db2_dir_name)
        self.db1_file_name = db1_file_name if db1_file_name else dir_name
        self.db2_file_name = db2_file_name if db2_file_name else dir_name

class DatalogProgram():
    def __init__(self,program_type,class_name,sep_dl,merge_dl,blocked_terms=None):
        self.program_type = program_type
        self.class_name = class_name
        self.execution_path = PathLib.datalog_programs_path.joinpath(program_type).joinpath(class_name)
        self.sep_dl = self.execution_path.joinpath(sep_dl)
        self.merge_dl = self.execution_path.joinpath(merge_dl)
        if not blocked_terms:
            blocked_terms = {}
        self.blocked_terms = blocked_terms

DOOP_Unit_Test_Renamed_Literals = DB_Config("DoopProgramAnalysis","Unit-Tests", "Basic", "Literal-Renaming","BasicMethod" ,"BasicMethod")
DOOP_Unit_Test_Renamed_Method = DB_Config("DoopProgramAnalysis","Unit-Tests", "Basic", "Method-Renaming","BasicMethod" ,"Renamed")


Doop_Constants = DB_Config("DoopProgramAnalysis","Constants", "v1", "v2")
Doop_Simple_Pointer = DB_Config("DoopProgramAnalysis","Simple_Pointer", "v1", "v2")
Doop_Simple_Java_Calculator = DB_Config("DoopProgramAnalysis","Simple_Java_Calculator", "v3_0", "v3_1_1")
Doop_Gocd_Websocket_Notifier_v1_v4 = DB_Config("DoopProgramAnalysis","Gocd_Websocket_Notifier", "v0_1", "v0_4_2")
Doop_Gocd_Websocket_Notifier_v3_v4 = DB_Config("DoopProgramAnalysis","Gocd_Websocket_Notifier", "v0_3", "v0_4_2")

Doop_CFG = DatalogProgram("DoopProgramAnalysis","CFG","CFG_separate.rls","CFG_merge.rls", {'',' ',"abstract","<sun.misc.ProxyGenerator: byte[] generateClassFile()>"})
Doop_PointerAnalysis = DatalogProgram("DoopProgramAnalysis","PointerAnalysis","PointerAnalyse_separate.rls","PointerAnalyse_merge_no_fold.rls",{'',' ',"<clinit>", "void()","public","static","main","void(java.lang.String[])","java.io.Serializable","java.lang.Cloneable","java.lang.Object","abstract"})

Unit_Tests_Doublette = DB_Config("Strukturelle_Unit_Tests","Doublette_Paradox","v1","v2")
Unit_Tests_Jacc_Finsish = DB_Config("Strukturelle_Unit_Tests","Jaccard_Finish_Problem","v1","v2")



Syn_Family_Fold_DL = DatalogProgram("SouffleSynthetic","Family","Family_separate.rls","Family_merge_fold.rls", {})

Syn_Family_DL = DatalogProgram("SouffleSynthetic","Family","Family_separate.rls","Family_merge.rls", {})
Syn_Orbits_DL = DatalogProgram("SouffleSynthetic","Orbits","Orbits_separate.rls","Orbits_merge.rls",{})
Syn_Po1_DL = DatalogProgram("SouffleSynthetic","Po1","Po1_separate.rls","Po1_merge.rls",{})

Syn_Family_db = DB_Config("SouffleSynthetic","Family","v1","v2")
Syn_Orbits_db = DB_Config("SouffleSynthetic","Orbits","v1","v2")
Syn_Po1_db = DB_Config("SouffleSynthetic","Po1","v1","v2")

Family_db = DB_Config("SouffleSynthetic","Family","Unit","Example")
Family_Renaming_db = DB_Config("SouffleSynthetic","Family","Unit","Renaming")
