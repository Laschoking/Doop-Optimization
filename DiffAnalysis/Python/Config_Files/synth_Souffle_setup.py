from Python.Libraries.EvaluateMappings import *
from Python.Config_Files.Analysis_Configs import *
from itertools import chain
from collections import Counter
import datetime
import pandas as pd
from Python.Libraries.Mapping import *
from Python.Libraries.SimilarityMetric.ISUB_SequenceMatcher import *
from Python.Libraries.SimilarityMetric.Term_Equality import *
from Python.Libraries.SimilarityMetric.Jaccard_Term_Overlap import *
from Python.Libraries.SimilarityMetric.Jaccard_Min import *
from Python.Libraries.SimilarityMetric.Jaccard_ISUB_Mix import *
from Python.Libraries.SimilarityMetric.Occurance_Multiplication import *
import git

import time

if __name__ == "__main__":

    # specify Java-files & Programm Analysis
    db_config = Doop_Simple_Pointer
    program_config = Doop_PointerAnalysis

    gen_new_facts = False  # if true, run doop again for new fact-gen, otherwise just copy from doop/out
    comp_new_mapping = True
    run_DL = True

  

    # Fact Creation of Java-Files (or .Jar)
    data = DataBag(db_config.base_output_path,db_config.db1_path, db_config.db2_path)

    # for collecting results
    global_log = ShellLib.GlobalLogger(data.paths.global_log)
    repo = git.Repo(search_parent_directories=True)
    commit = repo.head.object.hexsha
    date = datetime.datetime.now()


    if gen_new_facts:
        ShellLib.create_input_facts(db_config, db_config.db1_dir_name, db_config.db1_file_name, data.db1_original_facts.path)
        ShellLib.create_input_facts(db_config, db_config.db2_dir_name, db_config.db2_file_name, data.db2_original_facts.path)

    # load facts into data-object
    data.db1_original_facts.read_db_relations()
    data.read_terms_from_db(data.terms1, data.db1_original_facts)
    data.db2_original_facts.read_db_relations()
    data.read_terms_from_db(data.terms2, data.db2_original_facts)


    # compute & evaluate equality base line
    if run_DL:
        nemo_runtime = ShellLib.chase_nemo(program_config.sep_dl, data.db1_original_facts.path,
                                              data.db1_original_results.path)
        global_log.reasoning_df.loc[len(global_log.reasoning_df)] = [date, commit, db_config.dir_name + "-"+ db_config.db1_dir_name, None ,
                                               program_config.sep_dl.stem] + nemo_runtime

        nemo_runtime = ShellLib.chase_nemo(program_config.sep_dl, data.db2_original_facts.path,
                                          data.db2_original_results.path)
        global_log.reasoning_df.loc[len(global_log.reasoning_df)] = [date, commit,db_config.dir_name + "-"+ db_config.db2_dir_name, None,program_config.sep_dl.stem] + nemo_runtime


        data.db1_original_results.read_db_relations()
        data.db2_original_results.read_db_relations()

        reasoning_res = []

    db1_facts = data.db1_original_facts
    db2_facts = data.db2_original_facts

    # add mappings to data
    data.add_mapping(Mapping(data.paths, "local_expansion", iterative_anchor_expansion, "jaccard_min", jaccard_term_overlap))
    #data.add_mapping(Mapping(data.paths, "full_expansion", full_expansion_strategy, "term_equality", term_equality))
    #data.add_mapping(Mapping(data.paths, "full_expansion", full_expansion_strategy, "jaccard_min", jaccard_min))
    #data.add_mapping(Mapping(data.paths, "full_expansion", full_expansion_strategy, "isub", isub_sequence_matcher))
    #data.add_mapping(Mapping(data.paths, "full_expansion", full_expansion_strategy, "jaccard+isub",  jaccard_isub_mix))
    #data.add_mapping(Mapping(data.paths, "local_expansion", iterative_anchor_expansion, "term_equality", term_equality))
    #data.add_mapping(Mapping(data.paths, "local_expansion", iterative_anchor_expansion, "isub", isub_sequence_matcher))
    #data.add_mapping(Mapping(data.paths,"local_expansion",iterative_anchor_expansion,"jaccard+isub",jaccard_isub_mix))

    eval_tab = PrettyTable()
    eval_tab.field_names = ["Method", "data set", "unique rows DB1", "unique rows DB2", "Common Rows",
                            "overlap in %"]
    eval_tab.add_row(["No mapping","original facts"] + compute_overlap_dbs(data.db1_original_facts, data.db2_original_facts, print_flag=False))

    time_tab = PrettyTable()
    time_tab.field_names = ["Mapping", "#blocked Mappings", "# 1:1 Mappings", "#synthetic Terms", "# hub comp.", "uncertain mappings", "# comp. tuples", "comp. tuples in %", "run-time"]

    c_max_tuples = len(data.terms1) * len(data.terms2)
    # iterate through all selected mapping functions
    for mapping in data.mappings:
        print("--------------------------")
        print(mapping.name)
        # calculate similarity_matrix & compute maximal mapping from db1_facts to db2_facts
        if comp_new_mapping:
            t0 = time.time()
            mapping.compute_mapping(db1_facts,data.terms1, db2_facts, data.terms2, program_config.blocked_terms)
            t1 = time.time()
            mapping.db1_renamed_facts.log_db_relations()
            mapping_rt = round(t1 - t0, 4)
        else:
            mapping.read_mapping()
            mapping_rt = 0.0
        nr_1_1_mappings = len(mapping.mapping)
        # execute best mapping and create merged database: merge(map(db1_facts), db2_facts) -> merge_db2
        mapping.merge_dbs(mapping.db1_renamed_facts, db2_facts, mapping.db_merged_facts)

        mapping.log_mapping()
        mapping.db_merged_facts.log_db_relations()
        res = count_overlap_merge_db(mapping.db_merged_facts)
        if mapping == data.mappings[-1]:
            eval_tab.add_row([mapping.name, "merged facts"] + res ,divider=True)
        else:
            eval_tab.add_row([mapping.name, "merged facts"] + res, divider=False)



        l_blocked_terms = len(program_config.blocked_terms)

        time_tab.add_row(
            [mapping.name, l_blocked_terms, nr_1_1_mappings, mapping.new_term_counter, mapping.c_hub_recomp,
             mapping.c_uncertain_mappings, mapping.c_comp_tuples,
             str(round(mapping.c_comp_tuples * 100 / c_max_tuples, 2)) + "%", mapping_rt])
        if comp_new_mapping:
            global_log.mapping_df.loc[len(global_log.mapping_df)] = (
                    [date, commit, db_config.dir_name,mapping.name,mapping.expansion_strategy.__name__,mapping.similarity_metric.__name__,mapping.c_comp_tuples,str(round(mapping.c_comp_tuples * 100 / c_max_tuples,2)) + "%",nr_1_1_mappings, mapping.new_term_counter,mapping.c_hub_recomp, mapping.c_uncertain_mappings] + res + [mapping_rt])

        if run_DL:
            # run Nemo-Rules on merged facts (merge_db2 )
            nemo_runtime = ShellLib.chase_nemo(program_config.merge_dl, mapping.db_merged_facts.path,
                                               mapping.db_merged_results.path)

            # Read PA-results
            mapping.db_merged_results.read_db_relations()

            # Apply mapping to merged-result (from db2_facts)
            #mapping.map_df(mapping.db_merged_results, mapping.db1_unravelled_results)
            mapping.unravel_merge_dbs()
            mapping.db1_unravelled_results.log_db_relations()
            mapping.db2_unravelled_results.log_db_relations()

            # check if bijected results correspond to correct results from base
            verify_merge_results(data, mapping)
            overlap = count_overlap_merge_db(mapping.db_merged_results)
            reasoning_res.append([mapping.name, "merged results"] + overlap)
            # global_log nemo-runtime
            global_log.reasoning_df.loc[len(global_log.reasoning_df)] = [date,commit,db_config.full_name, mapping.name, program_config.merge_dl.stem] + nemo_runtime
            #"Date","SHA","MergeDB","Mapping","Expansion","Metric", "Unique Records DB1","Unique Records DB2","Mutual Records","Overlap in %"
            global_log.merge_db_df.loc[len(global_log.merge_db_df)] = [date,commit,db_config.full_name, mapping.name,mapping.expansion_strategy.__name__,
                                                                 mapping.similarity_metric.__name__] + overlap

    # Evaluation function to analyse if the mapping reduces storage
    print(time_tab)
    if run_DL:
        eval_tab.add_row(["No mapping", "original results"] + compute_overlap_dbs(data.db1_original_results,data.db2_original_results))
        # unfortunately we cant evalute this during the mapping bc. eval_tab should be separated by fact-eval & DL-eval
        eval_tab.add_rows(reasoning_res)

    print(eval_tab)

    data.log_terms()
    global_log.saveResults()
