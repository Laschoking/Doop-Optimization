from collections import deque
import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sortedcontainers import SortedList, SortedDict
import itertools
import Python.Config_Files.Setup as setup
debug = True

# blocked terms only if DL-computation
def iterative_anchor_expansion(mapping_obj, db1, terms1, db2, terms2, blocked_terms, similarity_metric):
    prio_dict = SortedDict()
    # those lists hold all terms, that are still mappable
    for term in terms1.keys():
        if type(term) is not str:
            print(term)
    free_term_names1 = SortedList(terms1.keys())
    free_term_names2 = SortedList(terms2.keys())

    # those Dicts are a mirror version of prio_dict. for each term t, the tuple objects are saved, where t is involved
    # holds {term_name : [(tuple1,sim1),(tuple2,sim2) ...]}
    terms1_pq_mirror = SortedDict()
    terms2_pq_mirror = SortedDict()
    mapping_dict = []

    tuples_loc_sim = SortedDict()
    processed_mapping_tuples = set()

    # block certain terms, that cannot be changed without computing wrong results
    for blocked_term in blocked_terms:
        if blocked_term in terms1:
            # map term to itself
            mapping_dict.append((blocked_term,blocked_term))
            free_term_names1.discard(blocked_term)
            # if in terms2 then delete occurrence there
            if blocked_term in free_term_names2:
                free_term_names2.discard(blocked_term)
            else:
                # for counting, how many terms are mapped to synthetic values (that do not exist in db2)
                mapping_obj.new_term_counter += 1
    # counts len, after mapping pop, del obsolete tuples & adding new tuples from neighbourhoods
    watch_prio_len = []
    watch_exp_sim = []
    accepted_sim = []
    uncertain_mapping_tuples = 0
    local_approval = setup.hub_recompute

    count_hub_recomp = 0
    new_hubs_flag = True
    last_sim = 0
    # TODO auch eine Möglichkeit wäre es, alle Mappings eines Bags abzuarbeiten (falls viele sehr gut sind)

    while 1:
        if prio_dict and not new_hubs_flag:  # pop last item = with the highest similarity
            sim, tuples = prio_dict.peekitem(index=-1)
            #if debug: print(prio_dict)

            # data could be empty because of deletion of obsolete term-tuples
            if not tuples:
                prio_dict.popitem(-1)
                continue

            # removes first data-item ( tuples appended later i.e. by hub recomputation are at the end)
            term_name_tuple = tuples.pop(0)
            term_name1, term_name2 = term_name_tuple
            term_obj1, term_obj2 = terms1[term_name1], terms2[term_name2]

            # last tuple in similarity bin -> delete empty bin

            if term_name1 not in free_term_names1 or term_name2 not in free_term_names2:
                ValueError("Term should not be vacant anymore: " + term_name1 + " " +  term_name2)
            # if value is too bad - find new Hubs

            if setup.hub_recompute and accepted_sim and local_approval:
                q1 = np.percentile(accepted_sim,25)
                q3 = np.percentile(accepted_sim,75)
                IQR = q3 - q1
                low_outlier = q1 - 1.5 * IQR
                if sim < low_outlier:
                    # trigger new hub detection
                    new_hubs_flag = True
                    # insert sim & tuple back to dictionary
                    prio_dict[sim].append(term_name_tuple)
                    print("denied: " + str(sim))
                    # mark as false so at least 1 new mapping has to be added before we can trigger recomputation again
                    local_approval = False
                    continue
                

            sim, common_occ = tuples_loc_sim[term_name_tuple]

            # add new mapping
            mapping_dict.append((term_name1,term_name2))
            if debug: print(term_name1 + " -> " + term_name2)

            # make terms "blocked"
            free_term_names1.discard(term_name1)
            free_term_names2.discard(term_name2)

            # remove tuple from mirror so that we have no key error
            terms1_pq_mirror[term_name1].remove((sim, term_name_tuple))
            terms2_pq_mirror[term_name2].remove((sim, term_name_tuple))

            # delete all tuples from priority queue, that contain term_obj1 or term_obj2

            uncertain_mapping_flag = delete_from_prio_dict(terms1_pq_mirror[term_name1], prio_dict, sim)
            uncertain_mapping_flag += delete_from_prio_dict(terms2_pq_mirror[term_name2], prio_dict, sim)
            l = sum(len(val) for val in prio_dict.values())
            if debug:
                print("reduced length: " + str(l))
            watch_prio_len.append(l)

            if uncertain_mapping_flag:
                uncertain_mapping_tuples += 1
            # remove term entry from mirror
            del terms1_pq_mirror[term_name1]
            del terms2_pq_mirror[term_name2]

            accepted_sim.append(sim)

            # expansion strategy:
            # current state: consider only terms, that occur in same colum of merged records
            new_mapping_tuples = set()
            for file_name, map_term_col in common_occ.keys():

                db1_row_ids, db2_row_ids = term_obj1.occurrence[(file_name, map_term_col)], term_obj2.occurrence[
                        (file_name, map_term_col)]
                df1 = db1.files[file_name]
                df2 = db2.files[file_name]
                cols = unpack_multi_columns(map_term_col)
                #if debug: print(file_name,col)

                # the mapped tuple (term_obj1, term_obj2) has the same key =  "file_name" & position "col"
                # this could have been multiple times (db1_row_ids & db2_row_ids) for the same key
                # i.e. term_obj1 "a" appears in several rows at the same spot  1:[a,b,c], 2:[a,d,f], so db1_row_ids hold all record-ids [1,2]
                # -> iterate through all columns and retrieve possible mapping pairs (aka. neighbours of term1 & term2)
                for col_ind in set(range(len(df1.columns))) - set(cols):
                    # iterate through all records of db1: "filename", where term1 was at place "col"

                    # retrieve Term-objects that are neigbours of previously mapped terms
                    new_term_names1 = set(df1.at[rec_ind,col_ind] for rec_ind in db1_row_ids if
                                         df1.at[rec_ind,col_ind] in free_term_names1)
                    new_term_names2 = set(df2.at[rec_ind,col_ind] for rec_ind in db2_row_ids if
                                         df2.at[rec_ind,col_ind] in free_term_names2)

                    # insert crossproduct of poss. new mappings into set
                    new_mapping_tuples |= find_crossproduct_mappings(new_term_names1, new_term_names2)

            # remove pairs, that are in prio_dict
            if setup.update_terms:       
                update_tuples = processed_mapping_tuples & new_mapping_tuples
                update_existing_mappings(update_tuples, prio_dict,tuples_loc_sim,terms1_pq_mirror, terms2_pq_mirror)

            new_mapping_tuples -= processed_mapping_tuples

            add_mappings_to_pq(terms1, terms2, new_mapping_tuples, tuples_loc_sim, terms1_pq_mirror, terms2_pq_mirror, prio_dict,
                               processed_mapping_tuples, watch_exp_sim, similarity_metric)


            if not prio_dict:
                new_hubs_flag = True
            # allow new hub-recomputation
            if not local_approval:
                local_approval = True
                print("now accepted: " + str(sim))

            l = sum(len(val) for val in prio_dict.values())
            if debug:
                print("new length: " + str(l))
            watch_prio_len.append(l)

        # add new hubs, if prio_dict is empty
        elif len(free_term_names1) > 0 and len(free_term_names2) > 0 and new_hubs_flag:
            new_hubs_flag = False  # idea is to only find new hubs if in last iteration at least 1 mapping was added
            count_hub_recomp += 1

            # detect new hubs (term-objects) based on all free-terms for each Database
            hubs1 = find_hubs_quantile(free_term_names1, terms1)
            hubs2 = find_hubs_quantile(free_term_names2, terms2)

            new_mapping_tuples = find_crossproduct_mappings(hubs1, hubs2)
            add_mappings_to_pq(terms1,terms2,new_mapping_tuples, tuples_loc_sim, terms1_pq_mirror, terms2_pq_mirror, prio_dict,
                               processed_mapping_tuples, watch_exp_sim, similarity_metric)
            l = sum(len(val) for val in prio_dict.values())
            if debug:
                print("new length hubs: " + str(l))
            watch_prio_len.append(l)

        else:
            # Exit Strategy
            # map the remaining terms to dummies
            for term_name1 in free_term_names1:
                new_term = "new_var_" + str(mapping_obj.new_term_counter)
                # print("add new var: " + new_term + " for " + term)
                mapping_dict.append((term_name1,new_term))
                mapping_obj.new_term_counter += 1
            if len(mapping_dict) != len(terms1):
                s1 = set([x for (x,y) in mapping_dict])
                s2 = set(terms1.keys())
                print(s1 - s2)
                print(s2 - s1)
                raise ValueError("not same nr of mappings than terms: " + str(len(mapping_dict)) + " " + str(len(terms1)) )

            break
    mapping_obj.mapping = pd.DataFrame.from_records(mapping_dict,columns=None)

    fig, ax = plt.subplots(4,1)
    fig.suptitle("iterativeExpansion + " + similarity_metric.__name__)
    ax[0].scatter(range(len(watch_prio_len)),watch_prio_len,s=1, label='Queue Size')
    ax[0].set_title("Queue Size")
    ax[1].scatter(range(len(watch_exp_sim)),np.array(watch_exp_sim),s=1,label='Expanded Similarities')
    ax[1].set_title("Computed Similarities")
    ax[2].scatter(range(len(accepted_sim)), np.array(accepted_sim), s=0.5, label='Accepted Similarities')
    ax[2].set_title("Mapped Similarities")
    ax[3].hist(accepted_sim,100,label='Accepted Mapping Distribution')
    ax[3].set_title("Distribution of Similarities")
    fig.tight_layout()
    plt.show()

    return uncertain_mapping_tuples, count_hub_recomp, len(tuples_loc_sim.keys())
# stop sim berechnung wenn maximum gefunden wurde?
# bag weise berechnung?

def delete_from_prio_dict(tuples, prio_dict, mapped_sim):
    uncertain_mapping_flag = False
    for sim,tuple_names in tuples:
        if sim not in prio_dict:
            ValueError("sim- key not in priority dict:" + str(sim))
        elif tuple_names not in prio_dict[sim]:
            continue
        # for the moment we just ignore, that the tuple was removed from the other side some iterations before
        # f.e. (t1,t3) was chosen before as mapping so (t1,t2) was removed in last iteration
        # now we pick (t4,t2) and would want to remove (t1,t2) again b
        # print("skipped value, bc it was removed from other side: " + str(tuple_names))
        else:
            prio_dict[sim].remove(tuple_names)
            # this is for logging, how often a mapping was done, where one of the terms had other tuples with the same
            # similarity
            if not uncertain_mapping_flag and sim >= mapped_sim:
                uncertain_mapping_flag = True
    return uncertain_mapping_flag


def find_crossproduct_mappings(hubs1, hubs2):
    return set(itertools.product(hubs1, hubs2))


# poss_mappings is a set of tuple
def add_mappings_to_pq(terms1,terms2, new_mapping_tuples, tuples_loc_sim, terms1_pq_mirror, terms2_pq_mirror, prio_dict,
                       processed_mapping_tuples, watch_exp_sim, similarity_metric):
    for term_name_tuple in new_mapping_tuples:
        term_name1, term_name2 = term_name_tuple
        term_obj1, term_obj2 = terms1[term_name1], terms2[term_name2]

        # this check is currently not necessary but later, when adding struc-sim we need it
        if term_name_tuple not in tuples_loc_sim:
            join = occurrence_overlap(term_obj1, term_obj2)
            common_occ, term1_record_ids, term2_record_ids = join
            sim = similarity_metric(term_obj1, term_obj2, common_occ)

            tuples_loc_sim[term_name_tuple] = (sim, common_occ)

            # add tuple to priority_queue
            if sim > 0:
                if sim not in prio_dict:
                    prio_dict[sim] = list([term_name_tuple])
                else:
                    prio_dict[sim].append(term_name_tuple)
                #if debug: print(sim, term_name_tuple)

                processed_mapping_tuples.add(term_name_tuple)

                # add term & tuple to prio_dict-mirror-1
                if term_name1 in terms1_pq_mirror:
                    terms1_pq_mirror[term_name1].append((sim,term_name_tuple))
                else:
                    terms1_pq_mirror[term_name1] = [(sim,term_name_tuple)]

                # add term & tuple to prio_dict-mirror-2
                if term_name2 in terms2_pq_mirror:
                    terms2_pq_mirror[term_name2].append((sim,term_name_tuple))
                else:
                    terms2_pq_mirror[term_name2] = [(sim,term_name_tuple)]
                watch_exp_sim.append(sim)

def update_existing_mappings(update_tuples, prio_dict,tuples_loc_sim,terms1_pq_mirror,terms2_pq_mirror):
    alpha = 0.15
    for tuple in update_tuples:
        term_name1, term_name2 = tuple
        if term_name1 in terms1_pq_mirror and term_name2 in terms2_pq_mirror:
            sim,rest = tuples_loc_sim[tuple]
            prio_dict[sim].remove(tuple)
            terms1_pq_mirror[term_name1].remove((sim,tuple))
            terms2_pq_mirror[term_name2].remove((sim,tuple))

            sim += sim * alpha
            if sim not in prio_dict:
                prio_dict[sim] = list([tuple])
            else:
                prio_dict[sim].append(tuple)
            tuples_loc_sim[tuple] = (sim,rest)
            terms1_pq_mirror[term_name1].append((sim, tuple))
            terms2_pq_mirror[term_name2].append((sim,tuple))

def occurrence_overlap(term_obj1, term_obj2):
    # intersection saves the key (file,col_nr): #common which is the minimum of occurrences for this key
    intersection = term_obj1.occurrence_c & term_obj2.occurrence_c
    term1_record_ids = []
    term2_record_ids = []
    # maybe it would be smarter to calculate this only after mapping has been accepted
    # on the other hand: when including the neighbour sim we need this info here
    # overlap consists of file, col_nr
    for overlap in intersection:
        term1_record_ids.append(term_obj1.occurrence[overlap])
        term2_record_ids.append(term_obj2.occurrence[overlap])
    return intersection, term1_record_ids, term2_record_ids


def find_hubs_std(free_term_names, terms_occ):
    degrees = []
    nodes = []
    for term in free_term_names:
        degrees.append(len(terms_occ[term]))
        nodes.append(term)
    mean = np.mean(degrees)
    std_dev = np.std(degrees)
    threshold = mean + std_dev
    # print("mean: "  + str(mean))
    # print("std_dev: " + str(std_dev))
    hubs = [nodes[i] for i in range(len(degrees)) if degrees[i] > threshold]
    # print("anzahl der hubs: " + str(len(hubs)))
    # print("anzahl der Terme: " + str(len(nodes)))
    return hubs


def find_hubs_quantile(free_term_names, terms):
    nodes = [terms[term_name].degree for term_name in free_term_names]
    #if debug: print(
    #    "node degree mean: " + str(round(np.mean(nodes), 2)) + " standard deviation: " + str(round(np.std(nodes), 2)))
    quantile = np.quantile(nodes, q=0.95)
    # returns termobjects
    return set(free_term_names[iter] for iter in range(len(free_term_names)) if nodes[iter] >= quantile)

def unpack_multi_columns(cols):
    # returns a list of ints
    return list(map(int,cols.split("-")))