from collections import deque
import itertools
import numpy as np
from Python.Libraries.MappingStrategies.Mapping import *
import matplotlib.pyplot as plt
from sortedcontainers import SortedList,SortedDict

class Iterative_Anchor_Mapping(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)

    def compute_mapping(self, db1,db2,blocked_terms):
        pq = SortedDict()
        free_terms1 = SortedList(list(db1.terms.keys()))
        free_terms2 = SortedList(list(db2.terms.keys()))

        # block certain terms, that cannot be changed without computing wrong results
        # TODO floats etc. beachten
        for term_name,term_obj in db1.terms.items():
            if term_name in blocked_terms or term_obj.type == "int":
                # map term to itself
                self.mapping[term_name] = term_name
                free_terms1.discard(term_name)
                # if in terms2 then delete occurrence there
                if term_name in free_terms2:
                    free_terms2.discard(term_name)
                else:
                    # for counting, how many terms are mapped to synthetic values (that do not exist in DB2)
                    self.new_term_counter += 1


        pq_watch = SortedList()
        expanded_sim = []
        accepted_mapping_sim =[]
        queue_len = []
        mapped_sim = []
        new_hubs_flag = True
        last_sim = 0
        # auch eine Möglichkeit wäre es, alle Mappings eines Bags abzuarbeiten (falls viele sehr gut sind)
        queue_len.append(len(pq))
        while 1:
            if pq and not new_hubs_flag:
                sim,data_q = pq.peekitem(index=-1)

                # removes first data-item
                (term_name1, term_name2), join = data_q.popleft()
                # last term in similarity bin -> remove bin
                if not data_q:
                    pq.popitem(-1)

                if term_name1 in free_terms1 and term_name2 in free_terms2:
                    # if value is too bad - find new Hubs
                    if sim < 0.9 * last_sim:
                        new_hubs_flag = True
                        insert_sim_to_queue((term_name1, term_name2) ,sim, join, pq)
                        last_sim = sim
                        continue


                    # add new mapping
                    self.mapping[term_name1] = term_name2
                    mapped_sim.append(sim)
                    free_terms1.discard(term_name1)
                    free_terms2.discard(term_name2)
                    last_sim = sim
                    accepted_mapping_sim.append(sim)

                    # expansion strategy:
                    # current state: consider only terms, that occur in same colum of merged records
                    for file_name, col, db1_row_ids, db2_row_ids in join:
                        db1_file_obj = db1.files[file_name]
                        db2_file_obj = db2.files[file_name]

                        # iterate through each cell of the merged records
                        # this excludes the old column of term_name1 & term_name2
                        for ind in itertools.chain(range(col), range(col + 1,db1_file_obj.col_size)):
                            # db1_row_ids & db2_row_ids are lists, since the terms may occur multiple times in 1 file
                            for db1_row_id in db1_row_ids:
                                for db2_row_id in db2_row_ids:

                                    new_t1_name = db1_file_obj.records[db1_row_id][ind]
                                    if new_t1_name not in free_terms1:
                                        continue

                                    new_t2_name = db2_file_obj.records[db2_row_id][ind]
                                    if new_t2_name not in free_terms2:
                                        continue

                                    new_term_pair = (new_t1_name,new_t2_name)
                                    if (new_term_pair) not in pq_watch:
                                        # join = [(file_name, col_nr, [row_id1], [row_id2]),()]
                                        sim, join = self.similarity(new_t1_name, db1.terms[new_t1_name], new_t2_name, db2.terms[new_t2_name])
                                        insert_sim_to_queue(new_term_pair, sim, join, pq)

                                        pq_watch.add(new_term_pair)

                    queue_len.append(len(pq))

            # add new hubs, if pq is empty
            elif len(free_terms1) > 0 and len(free_terms2) > 0 and new_hubs_flag:
                new_hubs_flag = False #idea is to only find new hubs if in last iteration at least 1 mapping was added
                hubs1 = self.find_hubs_quantile(free_terms1, db1.terms)
                hubs2 = self.find_hubs_quantile(free_terms2, db2.terms)
                for term_name1, term_obj1 in hubs1:
                    for term_name2,term_obj2 in hubs2:
                        term_pair = (term_name1,term_name2)
                        # this function may be called iterative, so even though term1 and term2 are free
                        # the combination could be already inside the pq list
                        if term_pair not in pq_watch:
                            sim, join = self.similarity(term_name1,term_obj1,term_name2,term_obj2)
                            insert_sim_to_queue(term_pair,sim, join,pq)

                            pq_watch.add((term_name1, term_name2))
                            expanded_sim.append(sim)
            else:
                break
        fig, ax = plt.subplots(4,1)
        ax[0].scatter(range(len(expanded_sim)),np.array(expanded_sim),s=1,label='Expanded Similarities')
        ax[1].scatter(range(len(mapped_sim)), np.array(mapped_sim), s=0.5, label='Mapped Similarities')
        #queue length is not representable since it counts dicts, each holding a big amount of values (with same sim)
        ax[2].scatter(range(len(queue_len)),queue_len,s=1, label='Queue Size')
        ax[3].hist(accepted_mapping_sim,100,label='Accepted Mapping Distribution')
        plt.show()
        return


    def find_hubs_std(self, free_terms, terms_occ):
        degrees = []
        nodes = []
        for term in free_terms:
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

    def find_hubs_quantile(self, free_terms, terms):
        nodes = [terms[term_name].degree for term_name in free_terms]
        quantile = np.quantile(nodes,q=0.95)
        # TODO could be replaced by lambda function
        return [(free_terms[iter],terms[free_terms[iter]]) for iter in range(len(free_terms)) if nodes[iter] >= quantile ]

#        return [(term_name,term_obj) for term_name,term_obj in terms.items() if term_obj.degree >= quantile ]

    # will be overritten
    def similarity(self,term1,term2,term1_occ,term2_occ):
        return 0

def insert_sim_to_queue(term_pair,sim, join,pq):
    # insert minimal threshold here !
    if sim > 0:
        if sim not in pq:
            pq[sim] = deque([(term_pair ,join)])
        else:
            pq[sim].append((term_pair, join))
        #pq_watch.add(term_pair)
        #expanded_sim.append(sim)
