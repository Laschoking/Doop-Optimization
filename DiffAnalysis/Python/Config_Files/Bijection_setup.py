from Python.Libraries.EvaluateMappings import *
from Python.Config_Files.Analysis_Configs import *

from Python.Libraries.SimilarityMetric.ISUB_SequenceMatcher import *
from Python.Libraries.SimilarityMetric.SequenceMatcherPairOccurance import *
from Python.Libraries.SimilarityMetric.Term_Equality import *
from Python.Libraries.SimilarityMetric.Jaccard_Term_Overlap import *
from Python.Libraries.SimilarityMetric.Occurance_Multiplication import *


import time

if __name__ == "__main__":

    # specify Java-files & Programm Analysis
    db_config = Gocd_Websocket_Notifier_v1_v4
    pa_sep = analyses["nemo_PA_sep"]
    pa_merge = analyses["nemo_PA_merge_no_fold"]
    gen_new_facts = False # if true, run doop again for new fact-gen, otherwise just copy from doop/out

    # Fact Creation of Java-Files (or .Jar)
    data_frame = DataFrame(db_config.db1_path, db_config.db2_path)
    ShellLib.create_facts(db_config, data_frame.db1_original_facts.path, data_frame.db2_original_facts.path,gen_new_facts=gen_new_facts)


    # load facts into data-object
    data_frame.db1_original_facts.read_directory()
    data_frame.db2_original_facts.read_directory()

    #plot_degree_distribution(data_frame.db1_original_facts.terms)
    #plot_degree_distribution(data_frame.db2_original_facts.terms)


    pa_runtime = []
    eval_mappings = []

    # compute & evaluate equality base line
    pa_runtime.append(ShellLib.chase_nemo(pa_sep, data_frame.db1_original_facts.path, data_frame.db1_original_results.path))
    pa_runtime.append(ShellLib.chase_nemo(pa_sep, data_frame.db2_original_facts.path, data_frame.db2_original_results.path))

    data_frame.db1_original_results.read_directory()
    data_frame.db2_original_results.read_directory()

    # add mappings to data_frame
    db1 = data_frame.db1_original_facts
    db2 = data_frame.db2_original_facts

    #data_frame.add_mapping(StringEquality(data_frame.paths))
    #data_frame.add_mapping(SequenceMatcher(data_frame.paths))
    #data_frame.add_mapping(SequenceMatcherPairOccurance(data_frame.paths))
    #data_frame.add_mapping(ISUBSequenceMatcher_Crossproduct(data_frame.paths))
    #data_frame.add_mapping(ISUBSequenceMatcher_Iterative(data_frame.paths))
    #data_frame.add_mapping(ISUBSequenceMatcher_Iterative_Occ(data_frame.paths))
    #data_frame.add_mapping(TermOccuranceIterative(data_frame.paths))
    data_frame.add_mapping(Mapping(data_frame.paths,"iterative",iterative_anchor_expansion,"jaccard",jaccard_term_overlap))
    data_frame.add_mapping(Mapping(data_frame.paths,"iterative",iterative_anchor_expansion,"isub_sm",isub_sequence_matcher))
    #data_frame.add_mapping(Mapping(data_frame.paths,"iterative",iterative_anchor_expansion,"occ_multiplication",occurrence_multiplication))
    #data_frame.add_mapping(Mapping(data_frame.paths,"iterative",iterative_anchor_expansion,"term_equality",term_equality))


    time_tab = PrettyTable()
    time_tab.field_names = ["Mapping","#blocked Mappings", "# 1:1 Mappings","#synthetic Terms", "run-time"]

    # iterate through all selected mapping functions
    for mapping in data_frame.mappings:
        t0 = time.time()
        # calculate similarity_matrix & compute maximal mapping from db1 to db2
        mapping.compute_mapping(db1,db2,pa_merge["blocked_terms"])
        nr_1_1_mappings = len(mapping.mapping)
        # execute best mapping and create merged database: merge(map(db1), db2) -> merge_db2
        mapping.merge_dbs(db1,db2)
        mapping.write_diagnostics(data_frame,db_config.base_output_path)

        mapping.db2_merged_facts.write_data_to_file()



        # run Nemo-Rules on merged facts (merge_db2 )
        #pa_runtime.append(ShellLib.chase_nemo(pa_merge, mapping.db2_merge_facts_base.path, mapping.db2_merge_pa_base.path))
        pa_runtime.append(ShellLib.chase_nemo(pa_merge, mapping.db2_merged_facts.path, mapping.db2_nemo_merged_results.path))

        # Read PA-results
        mapping.db2_nemo_merged_results.read_directory()

        # Apply mapping to merged-result (from db2)
        mapping.revert_db_mapping(mapping.db2_nemo_merged_results,mapping.db1_inv_bij_results,1)


        # check if bijected results correspond to correct results from base
        check_data_correctness(data_frame,mapping)
        t1 = time.time()
        l_blocked_terms = len(pa_merge["blocked_terms"])
        time_tab.add_row([mapping.name,l_blocked_terms,nr_1_1_mappings,mapping.new_term_counter,round(t1 - t0,4)])

        # Evaluation function to analyse if the mapping reduces storage
    print(time_tab)
    print(evaluate_mapping_overlap(data_frame))

# eine Tabelle mit allen PA

# data_frame.db2_merge_pa_base.read_directory()

# TODO: Bessere Implementierung der Blocked numbers
# TODO: iterativ nachbarn einbeziehen
