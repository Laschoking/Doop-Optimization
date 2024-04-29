from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import *
from Python.Config_Files.Analysis_Configs import *

if __name__ == "__main__":
    db_config = PointerAnalysis12_Config
    pa_sep = analyses["nemo_PA_sep"]

    # Fact Creation & read into data
    data = Data(db_config.db1_path,db_config.db2_path)
    create_facts(db_config,data.db1_facts.db_path, data.db2_facts.db_path)
    data.db1_facts.read_directory()
    data.db2_facts.read_directory()

    # calculate the bijection & write merged fact-files
    data = forward_bijection(data)
    data.db2_merge_facts.write_data_to_file()
    diff_two_dirs(data.db2_facts, data.db2_merge_facts)
    # Run Program Analysis on merged fact-files
    sep_pa_runtime = run_single_pa(pa_sep,data.db1_facts.db_path, data.db1_pa.db_path)
    sep_pa_runtime += run_single_pa(pa_sep,data.db2_facts.db_path, data.db2_pa.db_path)
    print_nemo_runtime(sep_pa_runtime,pa_sep["pa"])

    # Read separate PA-results
    data.db1_pa.read_directory()
    data.db2_pa.read_directory()

    # Apply bijection to merged-result (from db2)
    data = reverse_bijection_on_pa(data)
    data.db1_pa_bijected.write_data_to_file()
    # compare bijected results with correct results from pa1
    diff_two_dirs(data.db1_pa, data.db1_pa_bijected)

