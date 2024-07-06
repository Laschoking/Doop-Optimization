from collections import deque
import matplotlib.pyplot as plt
import numpy as np
from Python.Libraries.Mapping.Mapping import *
from sortedcontainers import SortedList


class Crossproduct_Mapping_Queue(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)
        self.mapping = dict()

    def compute_mapping(self,db1,db2,pa_non_mapping_terms):
        free_terms1 = SortedList(list(db1.terms.keys()))
        free_terms2 = SortedList(list(db2.terms.keys()))

        # block certain terms, that cannot be changed without computing wrong results
        for non_term in pa_non_mapping_terms:
            if non_term in free_terms1:
                # map term to itself
                self.mapping[non_term] = non_term
                free_terms1.discard(non_term)
                # if in terms2 then delete occurance there
                if non_term in free_terms2:
                    free_terms2.discard(non_term)

        print("Terme in Db1:" + str(len(db1.terms)))
        print("Terme in Db2:" + str(len(db2.terms)))
        print("Anzahl evaluierter Paare: " + str(len(db1.terms)* len(db2.terms)))
        l = []
        sim_plot = []
        mapping_sim_plot = []
        for term1,occ1 in db1.terms.items():
            for term2,occ2 in db2.terms.items():
                sim = self.similarity(term1,term2,occ1,occ2)
                l.append((sim,term1,term2))
                sim_plot.append(sim)

        g = sorted(l, key=lambda sim: sim[0])
        q = deque(g)

        while q:
            sim, term1, term2 = q.pop()
            if (term1 in free_terms1 and term2 in free_terms2):
                self.mapping[term1] = term2
                mapping_sim_plot.append(sim)
                free_terms1.discard(term1)
                free_terms2.discard(term2)
        plt.figure()
        fig, ax = plt.subplots(2,1
                               )
        ax[0].scatter(range(len(sim_plot)),np.array(sim_plot),s=1,label='ISUB Wkt. Verteilung')
        ax[1].scatter(range(len(mapping_sim_plot)),np.array(mapping_sim_plot),s=1,label='ISUB Mapping Verteilung')

        plt.show()

    def similarity(self,t1,t2,occ1,occ2):
        return 0