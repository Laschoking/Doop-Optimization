from collections import deque
import itertools
import queue
import numpy as np
from Python.Libraries.MappingStrategies.Mapping import *
import matplotlib.pyplot as plt
from sortedcontainers import SortedList,SortedDict

class Iterative_Anchor_Mapping(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)

    def compute_mapping(self, db1,db2,pa_non_mapping_terms):
        pq = SortedDict()
        free_terms1 = SortedList(list(db1.terms.keys()))
        free_terms2 = SortedList(list(db2.terms.keys()))

        # block certain terms, that cannot be changed without computing wrong results
        for block_term in pa_non_mapping_terms:
            if block_term in free_terms1:
                # map term to itself
                self.mapping[block_term] = block_term
                free_terms1.discard(block_term)
                # if in terms2 then delete occurance there
                if block_term in free_terms2:
                    free_terms2.discard(block_term)
                else:
                    # for counting, how many terms are mapped to synthetic values (that do not exist in DB2)
                    self.new_term_counter += 1


        pq_watch = SortedList()
        expanded_sim = []
        queue_len = []
        mapped_sim = []
        added_mapping = True

        queue_len.append(len(pq))
        while 1:
            # pop queue elements successively
            if pq:
                sim,data_q = pq.peekitem(index=-1)
                # removes first data-item
                term1, term2, join = data_q.popleft()
                if not data_q:
                    pq.popitem(-1)
                if term1 in free_terms1 and term2 in free_terms2:
                    self.mapping[term1] = term2
                    mapped_sim.append(sim)
                    free_terms1.discard(term1)
                    free_terms2.discard(term2)
                    added_mapping = True

                    # expand possible mappings:
                    # column is irrelevant since we want to match things
                    for file, col, t1_row, t2_row in join:
                        # this excludes the old column of term1 & term2
                        for ind in itertools.chain(range(col), range(col + 1,db1.files[file])):
                            new_t1 = db1.data_rows[file][t1_row][ind]
                            if new_t1 not in free_terms1:
                                continue
                            new_t2 = db2.data_rows[file][t2_row][ind]
                            if new_t2 not in free_terms2:
                                continue
                            if (new_t1,new_t2) not in pq_watch:
                                sim, join = self.similarity(new_t1, new_t2,db1.terms[new_t1], db2.terms[new_t2])
                                if sim > 0 :
                                    if sim not in pq:
                                        expanded_sim.append(sim)
                                        pq[sim] = deque([(new_t1, new_t2, join)])
                                    else:
                                        pq[sim].append((new_t1, new_t2, join))
                                pq_watch.add((new_t1,new_t2))
                    queue_len.append(len(pq))

            # add new hubs, if pq is empty
            elif len(free_terms1) > 0 and len(free_terms2) > 0 and added_mapping:
                added_mapping = False #idea is to only find new hubs if in last iteration at least 1 mapping was added
                hubs1 = self.find_hubs(free_terms1, db1.terms)
                hubs2 = self.find_hubs(free_terms2, db2.terms)
                for term1 in hubs1:
                    for term2 in hubs2:
                        # this function may be called iterative, so even though term1 and term2 are free
                        # the combination could be already inside the pq list
                        if (term1,term2) not in pq_watch:
                            sim, join = self.similarity(term1, term2,db1.terms[term1],db2.terms[term2])
                            if sim > -1:
                                if sim not in pq:
                                    pq[sim] = deque([(term1,term2,join)])
                                else:
                                    pq[sim].append((term1,term2,join))
                                pq_watch.add((term1, term2))
                                expanded_sim.append(sim)
            else:
                break
        #mapped_sim = mapped_sim[2800:]
        fig, ax = plt.subplots(3,1)
        ax[0].scatter(range(len(expanded_sim)),np.array(expanded_sim),s=1,label='Expanded Similarities')
        ax[1].scatter(range(len(mapped_sim)), np.array(mapped_sim), s=0.5, label='Mapped Similarities')
        ax[2].scatter(range(len(queue_len)),queue_len,s=1, label='Queue Size')
        plt.show()
        return


    def find_hubs(self, free_terms, terms_occ):
        degrees = []
        nodes = []
        for term in free_terms:
            degrees.append(len(terms_occ[term]))
            nodes.append(term)
        mean = np.mean(degrees)
        std_dev = np.std(degrees)
        threshold = mean + 1.5 * std_dev
        hubs = [nodes[i] for i in range(len(degrees)) if degrees[i] > threshold]
        #print("anzahl der hubs: " + str(len(hubs)))
        #print("anzahl der Terme: " + str(len(nodes)))
        return hubs

    # will be overritten
    def similarity(self,term1,term2,term1_occ,term2_occ):
        return 0

