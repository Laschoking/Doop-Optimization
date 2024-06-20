import copy
import itertools
import queue
from collections import Counter
import numpy as np
from Python.Libraries.MappingStrategies.Mapping import *
import matplotlib.pyplot as plt
class Iterative_Anchor_Mapping(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)

    def compute_mapping(self, db1,db2):
        pq = queue.PriorityQueue()
        used1 = dict()
        used2 = dict()
        hubs1 = self.find_hubs(db1.terms)
        hubs2 = self.find_hubs(db2.terms)
        db1_data_rows_copy = copy.deepcopy(db1.data_rows)
        db2_data_rows_copy = copy.deepcopy(db2.data_rows)
        pq_watch = set()
        sim_plot = []
        for term1 in hubs1:
            for term2 in hubs2:
                sim, join = self.similarity(term1, db1.terms[term1], term2, db2.terms[term2])
                if sim != 0:
                    pq.put((sim, (term1, term2, join)))
                    pq_watch.add((term1,term2))
        while not pq.empty():
            sim, (term1, term2, join) = pq.get()
            if term1 not in used1 and term2 not in used2:
                self.mapping[term1] = term2
                sim_plot.append(sim)

                used1[term1] = None
                used2[term2] = None

                # delete occurances of term1 and term2
                # for file, col, row in db1.terms[term1]:
                for (file, col), row in db1.terms[term1].items():
                    db1_data_rows_copy[file][row][col] = None
                for (file, col), row in db2.terms[term2].items():
                    db2_data_rows_copy[file][row][col] = None

                # expand possible mappings:
                # column is irrelevant since we want to match things
                for file, col, t1_row, t2_row in join:
                    # this excludes the old column of term1 & term2
                    for ind in itertools.chain(range(col), range(col + 1,db1.files[file])):
                        new_t1 = db1_data_rows_copy[file][t1_row][ind]
                        new_t2 = db2_data_rows_copy[file][t2_row][ind]
                    # if one of the terms has been set to None,
                    # we know that the term has been mapped already
                        if new_t1 == None or new_t2 == None:
                            continue
                        sim, join = self.similarity(term1, db1.terms[new_t1], term2, db2.terms[new_t2])
                        t = (sim, (new_t1, new_t2, join))
                        if sim != 0 and (new_t1,new_t2) not in pq_watch:
                            pq.put(t)
                            pq_watch.add((new_t1,new_t2))
        print(len(self.mapping))
        #print(self.mapping)
        #a = np.sort(sim_plot)
        a = np.array(sim_plot)
        fig, ax = plt.subplots()
        ax.scatter(range(len(sim_plot)),a,s=1)
        plt.show()
        return


    def find_hubs(self, terms):
        degrees = []
        nodes = []
        for t, v in terms.items():
            degrees.append(len(v))
            nodes.append(t)
        mean = np.mean(degrees)
        std_dev = np.std(degrees)
        threshold = mean + 2 * std_dev
        hubs = [nodes[i] for i in range(len(degrees)) if degrees[i] > threshold]
        print("anzahl der hubs: " + str(len(hubs)))
        print("anzahl der Terme: " + str(len(nodes)))
        return hubs

# will be overritten
    def similarity(self,term1,term1_occ,term2,term2_occ):
        return 0