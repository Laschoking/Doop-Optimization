from Python.Libraries import ShellLib
from Python.Libraries.MergeLib import *
from Python.Config_Files.Analysis_Configs import *
from Python.Libraries.DBEvaluation import DBMetaData
from Python.Libraries.LexicalBijections.StringEqualityBaseline import *
from Python.Libraries.StructuralBijections.SequenceMatcherPairOccurance import *
from Python.Libraries.LexicalBijections.SequenceMatcher import *


if __name__ == "__main__":

    # specify Java-files & Programm Analysis
    db_config = PointerAnalysis_Calc_old_new
    pa_sep = analyses["nemo_PA_sep"]
    pa_merge = analyses["nemo_PA_merge_end_fold"]

    # Fact Creation of Java-Files (or .Jar)
    data_frame = DataFrame(db_config.db1_path, db_config.db2_path)
    ShellLib.create_facts(db_config, data_frame.db1_original_facts.path, data_frame.db2_original_facts.path)


    # load facts into data-object
    data_frame.db1_original_facts.read_directory()
    data_frame.db2_original_facts.read_directory()

    '''print("db1: ")
    print(DBMetaData.order_node_by_count(data_frame.db1_facts))
    DBMetaData.calculate_pairwise_occurance_within_DB(data_frame.db1_facts)

    print("db2: ")
    print(DBMetaData.order_node_by_count(data_frame.db2_facts))
    DBMetaData.calculate_pairwise_occurance_within_DB(data_frame.db2_facts)
    '''
    pa_runtime = []
    eval_bijections = []

    # compute & evaluate equality base line
    pa_runtime.append(ShellLib.chase_nemo(pa_sep, data_frame.db1_original_facts.path, data_frame.db1_original_results.path))
    pa_runtime.append(ShellLib.chase_nemo(pa_sep, data_frame.db2_original_facts.path, data_frame.db2_original_results.path))

    data_frame.db1_original_results.read_directory()
    data_frame.db2_original_results.read_directory()

    # add bijections to data_frame
    data_frame.add_bijection(StringEqualityBaseline(data_frame.paths))
    data_frame.add_bijection(SequenceMatcher(data_frame.paths))
    data_frame.add_bijection(SequenceMatcherPairOccurance(data_frame.paths))

    # iterate through all selected bijection functions
    for bijection in data_frame.bijections:
        # calculate similarity_matrix & compute maximal mapping from db1 to db2
        bijection.compute_similarity(data_frame)
        ma_sim_matrix, term1_list, term2_list = create_sim_matrix(bijection.similarity_dict)
        mapping = compute_optimal_mapping(ma_sim_matrix, term1_list, term2_list)
        bijection.set_mapping(mapping)

        # execute best mapping and create merged database: merge(map(db1), db2) -> merge_db2
        apply_mapping_and_merge_dbs(data_frame,bijection)
        bijection.db2_merged_facts.write_data_to_file()

        # run Nemo-Rules on merged facts (merge_db2 )
        #pa_runtime.append(ShellLib.chase_nemo(pa_merge, bijection.db2_merge_facts_base.path, bijection.db2_merge_pa_base.path))
        pa_runtime.append(ShellLib.chase_nemo(pa_merge, bijection.db2_merged_facts.path, bijection.db2_nemo_merged_results.path))

        # Read PA-results
        bijection.db2_nemo_merged_results.read_directory()

        # Apply bijection to merged-result (from db2)
        inverse_bijection(bijection.db2_nemo_merged_results, bijection.db1_inv_bij_results, bijection.mapping, 1)
        bijection.db1_inv_bij_results.write_data_to_file()

        # check if bijected results correspond to correct results from base
        check_data_correctness(data_frame,bijection)

        # Evaluation function to analyse if the bijection reduces storage

    print(evaluate_bijection_overlap(data_frame))

# eine Tabelle mit allen PA

# data_frame.db2_merge_pa_base.read_directory()
