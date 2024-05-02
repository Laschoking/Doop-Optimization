from Python.Libraries.Shell_Lib import *
from Python.Libraries.Merge_Lib import *
from Python.Config_Files.Analysis_Configs import *

if __name__ == "__main__":
    db_config = ConstantPropagation12_Config
    pa_sep = analyses["nemo_CP_sep"]
    pa_merge = analyses["nemo_CP_merge"]
    # Fact Creation & read into data
    data = Data(db_config.db1_path,db_config.db2_path)
    create_facts(db_config, data.db1_facts.path, data.db2_facts.path)
    data.db1_facts.read_directory()
    data.db2_facts.read_directory()

    # calculate the bijection & write merged fact-files
    data = forward_bijection(data)
    data.db2_merge_facts.write_data_to_file()
    diff_two_dirs(data.db2_facts, data.db2_merge_facts,rm_identifier=10)
    # Run Program Analysis on merged fact-files
    sep_pa_runtime = run_single_pa(pa_sep, data.db1_facts.path, data.db1_pa.path)
    sep_pa_runtime += run_single_pa(pa_sep, data.db2_facts.path, data.db2_pa.path)
    print_nemo_runtime(sep_pa_runtime,pa_sep["pa"])

    merge_pa_runtime = run_single_pa(pa_merge,data.db2_merge_facts.path, data.db2_merge_pa.path)

    # reverse common PA???

    # Read separate PA-results
    data.db1_pa.read_directory()
    data.db2_pa.read_directory()
    data.db2_merge_pa.read_directory()

    # Apply bijection to merged-result (from db2)
    to_bijected_db = reverse_bijection_on_pa(data.db2_merge_pa, data.db1_bijected_pa,data.bijection,1)
    data.db1_bijected_pa = to_bijected_db

    data.db1_bijected_pa.write_data_to_file()
    print(data.bijection)
    print(data.db1_bijected_pa.data)
    print(data.db1_pa.data)

    # compare bijected results with correct results from pa1
    diff_two_dirs(data.db1_pa, data.db1_bijected_pa)
    diff_two_dirs(data.db2_pa, data.db2_merge_pa,rm_identifier=10)

