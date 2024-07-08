from collections import deque
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sortedcontainers import SortedList,SortedDict
import itertools





def iterative_anchor_expansion(mapping_obj, db1,db2,blocked_terms,similarity_metric):
    prio_dict = SortedDict()
    
    # those lists hold all terms, that are still mappable
    free_term_names1 = SortedList(db1.terms.keys())
    free_term_names2 = SortedList(db2.terms.keys())

    # those Dicts are a mirror version of prio_dict. for each term t, the tuple objects are saved, where t is involved
    # holds {term_name : [(tuple1,sim1),(tuple2,sim2) ...]}
    terms1_pq_mirror = SortedDict()
    terms2_pq_mirror = SortedDict()
    
    all_tuple_sim = SortedDict()
    processed_mapping_tuples = set()

    # block certain terms, that cannot be changed without computing wrong results
    for blocked_term in blocked_terms:
        if blocked_term in db1.terms:
            # map term to itself
            mapping_obj.mapping[blocked_term] = blocked_term
            free_term_names1.discard(blocked_term)
            # if in terms2 then delete occurrence there
            if blocked_term in free_term_names2:
                free_term_names2.discard(blocked_term)
            else:
                # for counting, how many terms are mapped to synthetic values (that do not exist in DB2)
                mapping_obj.new_term_counter += 1
    # counts len, after mapping pop, del obsolete tuples & adding new tuples from neighbourhoods
    watch_prio_len = []
    watch_exp_sim = []
    watch_mapped_sim = []

    count_hub_recomp = 0
    new_hubs_flag = True
    last_sim = 0
    # TODO auch eine Möglichkeit wäre es, alle Mappings eines Bags abzuarbeiten (falls viele sehr gut sind)

    while 1:
        if prio_dict and not new_hubs_flag: # pop last item = with the highest similarity
            sim,tuples = prio_dict.peekitem(index=-1)

            # data could be empty because of deletion of obsolete term-tuples
            if not tuples:
                prio_dict.popitem(-1)
                continue

            # removes first data-item
            term_name_tuple = tuples.pop()
            term_name1, term_name2 = term_name_tuple
            term_obj1, term_obj2 = db1.terms[term_name1], db2.terms[term_name2]

            # last tuple in similarity bin -> delete empty bin


            if term_name1 in free_term_names1 and term_name2 in free_term_names2:
                # if value is too bad - find new Hubs
                if sim < 0.5 * last_sim:
                    new_hubs_flag = True
                    last_sim = sim
                    count_hub_recomp += 1
                    continue

                sim,common_occ = all_tuple_sim[term_name_tuple]

                # add new mapping
                mapping_obj.mapping[term_name1] = term_name2

                # make terms "blocked"
                free_term_names1.discard(term_name1)
                free_term_names2.discard(term_name2)

                # remove tuple from mirror so that we have no key error
                terms1_pq_mirror[term_name1].remove((term_name_tuple,sim))
                terms2_pq_mirror[term_name2].remove((term_name_tuple,sim))
                    #terms2_pq_mirror[term_name2].discard(term_name_tuple))

                # delete all tuples from priority queue, that contain term_obj1 or term_obj2

                delete_from_prio_dict(terms1_pq_mirror[term_name1],prio_dict)
                delete_from_prio_dict(terms2_pq_mirror[term_name2],prio_dict)

                # remove term entry from mirror
                del terms1_pq_mirror[term_name1]
                del terms2_pq_mirror[term_name2]

                last_sim = sim
                watch_mapped_sim.append(sim)

                # expansion strategy:
                # current state: consider only terms, that occur in same colum of merged records
                for file_name, map_term_col in common_occ.keys():
                    db1_row_ids, db2_row_ids = term_obj1.occurrence[(file_name,map_term_col)], term_obj2.occurrence[(file_name,map_term_col)]
                    db1_file_obj = db1.files[file_name]
                    db2_file_obj = db2.files[file_name]

                    new_mapping_tuples = set()

                    # the mapped tuple (term_obj1, term_obj2) has the same key =  "file_name" & position "map_term_col"
                    # this could have been multiple times (db1_row_ids & db2_row_ids) for the same key
                    # i.e. term_obj1 "a" appears in several rows at the same spot  1:[a,b,c], 2:[a,d,f], so db1_row_ids hold all record-ids [1,2]
                    # -> iterate through all columns and retrieve possible mapping pairs (aka. neighbours of term1 & term2)
                    for col_ind in itertools.chain(range(map_term_col), range(map_term_col + 1,db1_file_obj.col_size)):
                        # iterate through all records of DB1: "filename", where term1 was at place "map_term_col"

                        # retrieve Term-objects that are neigbours of previously mapped terms
                        new_term_objs1 = [db1.terms[db1_file_obj.records[rec_ind][col_ind]] for rec_ind in db1_row_ids]
                        new_term_objs2 = [db2.terms[db2_file_obj.records[rec_ind][col_ind]] for rec_ind in db2_row_ids]

                        # insert crossproduct of poss. new mappings into set
                        new_mapping_tuples |= find_crossproduct_mappings(new_term_objs1,new_term_objs2)

                    # remove pairs, that are in prio_dict 
                    new_mapping_tuples -= processed_mapping_tuples

                    add_mappings_to_pq(new_mapping_tuples, all_tuple_sim, terms1_pq_mirror, terms2_pq_mirror, prio_dict,
                                       processed_mapping_tuples, watch_exp_sim, similarity_metric)

            watch_prio_len.append(sum(len(val) for val in prio_dict.values()))

                #queue_len.append(len(prio_dict))

        # add new hubs, if prio_dict is empty
        elif len(free_term_names1) > 0 and len(free_term_names2) > 0 and new_hubs_flag:
            new_hubs_flag = False #idea is to only find new hubs if in last iteration at least 1 mapping was added

            # detect new hubs (term-objects) based on all free-terms for each Database
            hubs1 = find_hubs_quantile(free_term_names1, db1.terms)
            hubs2 = find_hubs_quantile(free_term_names2, db2.terms)

            new_mapping_tuples = find_crossproduct_mappings(hubs1, hubs2)
            add_mappings_to_pq(new_mapping_tuples,all_tuple_sim,terms1_pq_mirror,terms2_pq_mirror, prio_dict,processed_mapping_tuples,watch_exp_sim, similarity_metric)

            #pq_watch.add((term_name1, term_name2))
            #watch_exp_sim.append(sim)
            watch_prio_len.append(sum(len(val) for val in prio_dict.values()))
        else:
            break
            
    # TODOL=: print strategy & make nice table or sth
    print("hub recompution: " + str(count_hub_recomp))
    print("number of calculated tuples: " + str(len(all_tuple_sim.keys())))
    print("number of maximal tuples: " + str(len(db1.terms) * len(db2.terms)))
    fig, ax = plt.subplots(4,1)
    ax[0].scatter(range(len(watch_prio_len)),watch_prio_len,s=1, label='Queue Size')
    ax[1].scatter(range(len(watch_exp_sim)),np.array(watch_exp_sim),s=1,label='Expanded Similarities')
    ax[2].scatter(range(len(watch_mapped_sim)), np.array(watch_mapped_sim), s=0.5, label='Mapped Similarities')
    ax[3].hist(watch_mapped_sim,100,label='Accepted Mapping Distribution')
    plt.show()
    return

def delete_from_prio_dict(tuples, prio_dict):
    for tuple_names,sim in tuples:
        if sim not in prio_dict:
            ValueError("sim- key not in priority dict:" + str(sim))
        elif tuple_names not in prio_dict[sim]:
            continue
            # for the moment we just ignore, that the tuple was removed from the other side some iterations before
            # f.e. (t1,t3) was chosen before as mapping so (t1,t2) was removed in last iteration
            # now we pick (t4,t2) and would want to remove (t1,t2) again b
            #print("skipped value, bc it was removed from other side: " + str(tuple_names))
        else:
            prio_dict[sim].remove(tuple_names)

def find_crossproduct_mappings(hubs1, hubs2):
    return set(itertools.product(hubs1, hubs2))

# poss_mappings is a set of tuple
def add_mappings_to_pq(new_mapping_tuples,all_tuple_sim,terms1_pq_mirror, terms2_pq_mirror, prio_dict,processed_mapping_tuples, watch_exp_sim,similarity_metric):
    for term_obj1, term_obj2 in new_mapping_tuples:
        term_name_tuple = term_obj1.name, term_obj2.name

        # this check is currently not necessary but later, when adding struc-sim we need it
        if term_name_tuple not in all_tuple_sim:
            join = occurrence_overlap(term_obj1, term_obj2)
            common_occ, term1_record_ids, term2_record_ids = join
            sim = similarity_metric(term_obj1, term_obj2, common_occ)

            all_tuple_sim[term_name_tuple] = (sim, common_occ)
            
            # add tuple to priority_queue
            if sim > 0:
                if sim not in prio_dict:
                    prio_dict[sim] = SortedList([term_name_tuple])
                else:
                    prio_dict[sim].add(term_name_tuple)

                processed_mapping_tuples.add(term_name_tuple)

                # add term & tuple to prio_dict-mirror-1
                if term_obj1.name in terms1_pq_mirror:
                    terms1_pq_mirror[term_obj1.name].append((term_name_tuple,sim))
                else:
                    terms1_pq_mirror[term_obj1.name] = [(term_name_tuple,sim)]

                # add term & tuple to prio_dict-mirror-2
                if term_obj2.name in terms2_pq_mirror:
                    terms2_pq_mirror[term_obj2.name].append((term_name_tuple,sim))
                else:
                    terms2_pq_mirror[term_obj2.name] = [(term_name_tuple,sim)]
                watch_exp_sim.append(sim)


def occurrence_overlap(term_obj1,term_obj2):
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
    return intersection,term1_record_ids,term2_record_ids


def find_hubs_std(free_term_names, terms_occ):
    degrees = []
    nodes = []
    for term in free_term_names:
        degrees.append(len(terms_occ[term]))
        nodes.append(term)
    mean = np.mean(degrees)
    std_dev = np.std(degrees)
    threshold = mean + std_dev
    #print("mean: "  + str(mean))
    #print("std_dev: " + str(std_dev))
    hubs = [nodes[i] for i in range(len(degrees)) if degrees[i] > threshold]
    #print("anzahl der hubs: " + str(len(hubs)))
    #print("anzahl der Terme: " + str(len(nodes)))
    return hubs

def find_hubs_quantile(free_term_names, terms):
    nodes = [terms[term_name].degree for term_name in free_term_names]
    quantile = np.quantile(nodes,q=0.95)
    # returns termobjects
    return [terms[free_term_names[iter]] for iter in range(len(free_term_names)) if nodes[iter] >= quantile]