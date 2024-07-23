from Python.Libraries.EvaluateMappings import *
from Python.Config_Files.Analysis_Configs import *
from itertools import chain
from collections import Counter
import pandas as pd

from Python.Libraries.SimilarityMetric.ISUB_SequenceMatcher import *
from Python.Libraries.SimilarityMetric.SequenceMatcherPairOccurance import *
from Python.Libraries.SimilarityMetric.Term_Equality import *
from Python.Libraries.SimilarityMetric.Jaccard_Term_Overlap import *
from Python.Libraries.SimilarityMetric.Jaccard_Min import *
from Python.Libraries.SimilarityMetric.Jaccard_ISUB_Mix import *
from Python.Libraries.SimilarityMetric.Occurance_Multiplication import *


import time

if __name__ == "__main__":

    # specify Java-files & Programm Analysis
    db_config = Doop_Gocd_Websocket_Notifier_v1_v4
    program_config = Syn_Family_DL

    # TODO for synthetic DB - allow parameter for distribution of random values
    gen_new_facts = False  # if true, run doop again for new fact-gen, otherwise just copy from doop/out
    comp_new_mapping = True
    run_DL = False

    # Fact Creation of Java-Files (or .Jar)
    data_frame = DataFrame(db_config.db1_path, db_config.db2_path)

    if run_DL:
        ShellLib.create_input_facts(db_config, db_config.db1_dir_name, db_config.db1_file_name, data_frame.db1_original_facts.path)
        ShellLib.create_input_facts(db_config, db_config.db2_dir_name, db_config.db2_file_name, data_frame.db2_original_facts.path)

    # load facts into data-object
    data_frame.db1_original_facts.read_directory()
    data_frame.db2_original_facts.read_directory()


    pa_runtime = []
    eval_mappings = []

    # compute & evaluate equality base line
    if gen_new_facts:
        pa_runtime.append(ShellLib.chase_nemo(program_config.sep_dl, data_frame.db1_original_facts.path,
                                              data_frame.db1_original_results.path))
        pa_runtime.append(ShellLib.chase_nemo(program_config.sep_dl, data_frame.db2_original_facts.path,
                                          data_frame.db2_original_results.path))
    if run_DL:
        data_frame.db1_original_results.read_directory()
        data_frame.db2_original_results.read_directory()

    # add mappings to data_frame
    db1 = data_frame.db1_original_facts
    db2 = data_frame.db2_original_facts

    c_terms = 0
    for term in chain(db1.terms.values(),db2.terms.values()):
        c = Counter()
        for key,val in term.occurrence.items():
            for v in val:
                t = (key[0],v)
                c.update([t])
        l = c.most_common(1)[0]
        if l[1] > 1:
            #print(term.name,l)
            c_terms +=1
    print(c_terms)




    #data_frame.add_mapping(Mapping(data_frame.paths, "full_expansion", full_expansion_strategy, "term_equality", term_equality))
    #data_frame.add_mapping(Mapping(data_frame.paths, "full_expansion", full_expansion_strategy, "jaccard_min", jaccard_min))
    #data_frame.add_mapping(Mapping(data_frame.paths, "full_expansion", full_expansion_strategy, "isub", isub_sequence_matcher))
    #data_frame.add_mapping(Mapping(data_frame.paths, "full_expansion", full_expansion_strategy, "jaccard+isub",  jaccard_isub_mix))

    #data_frame.add_mapping(Mapping(data_frame.paths, "local_expansion", iterative_anchor_expansion, "term_equality", term_equality))
    data_frame.add_mapping(Mapping(data_frame.paths, "local_expansion", iterative_anchor_expansion, "jaccard_min", jaccard_term_overlap))
    #data_frame.add_mapping(Mapping(data_frame.paths, "local_expansion", iterative_anchor_expansion, "isub", isub_sequence_matcher))
    #data_frame.add_mapping(Mapping(data_frame.paths,"local_expansion",iterative_anchor_expansion,"jaccard+isub",jaccard_isub_mix))


    time_tab = PrettyTable()
    time_tab.field_names = ["Mapping", "#blocked Mappings", "# 1:1 Mappings", "#synthetic Terms", "# hub comp.", "uncertain mappings", "# comp. tuples", "comp. tuples in %", "run-time"]

    c_max_tuples = len(db1.terms) * len(db2.terms)
    # iterate through all selected mapping functions
    for mapping in data_frame.mappings:
        print("--------------------------")
        print(mapping.name)
        t0 = time.time()
        # calculate similarity_matrix & compute maximal mapping from db1 to db2
        if comp_new_mapping:
            (count_uncertain_mappings, count_hub_recomp, count_comp_tuples) = mapping.compute_mapping(db1, db2, program_config.blocked_terms)
        else:
            mapping.read_mapping(db_config.base_output_path)
        nr_1_1_mappings = len(mapping.mapping)
        # execute best mapping and create merged database: merge(map(db1), db2) -> merge_db2
        mapping.merge_dbs(db1, db2)
        mapping.write_diagnostics(data_frame, db_config.base_output_path)

        mapping.db2_merged_facts.write_data_to_file()
        check_data_correctness_facts(data_frame, mapping)

        if run_DL:
            # run Nemo-Rules on merged facts (merge_db2 )
            # pa_runtime.append(ShellLib.chase_nemo(pa_merge, mapping.db2_merge_facts_base.path, mapping.db2_merge_pa_base.path))
            pa_runtime.append(ShellLib.chase_nemo(program_config.merge_dl, mapping.db2_merged_facts.path,
                                                  mapping.db2_nemo_merged_results.path))

            # Read PA-results
            mapping.db2_nemo_merged_results.read_directory()

            # Apply mapping to merged-result (from db2)
            mapping.revert_db_mapping(mapping.db2_nemo_merged_results, mapping.db1_inv_bij_results, 1)

            # check if bijected results correspond to correct results from base
            check_data_correctness_results(data_frame, mapping)

        t1 = time.time()
        l_blocked_terms = len(program_config.blocked_terms)
        time_tab.add_row([mapping.name, l_blocked_terms, nr_1_1_mappings, mapping.new_term_counter, count_hub_recomp,count_uncertain_mappings,  count_comp_tuples,str(round(count_comp_tuples * 100 / c_max_tuples,2)) + "%", round(t1 - t0, 4)])

        # Evaluation function to analyse if the mapping reduces storage
    print(time_tab)
    print(evaluate_mapping_overlap_facts(data_frame))
    if run_DL:
        print(evaluate_mapping_overlap_results(data_frame))
    backup_path = ""

    if backup_path:
        mapping_view = pd.read_csv(backup_path.join("Mappings.tsv"))
        single_db_view = pd.read_csv(backup_path.join("SingleDatabase.tsv"))
        merge_db_view = pd.read_csv(backup_path.join("MergeDatabase.tsv"))
    else:

        single_db_view = pd.DataFrame(columns=["name","Term-count" "Atom-count", "last-modified"])
        merge_db_view = pd.DataFrame(columns=["Db1 name","DB2 name" ,"String Similarity","Mutual Termcount", "Mutual Atomcount"])
        mapping_backup = pd.DataFrame(columns=["Date","comit-hash","Database 1", "Database 2"])

