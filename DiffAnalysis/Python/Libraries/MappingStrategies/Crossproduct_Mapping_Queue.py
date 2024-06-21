from collections import deque
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import numpy as np
import sys
from Python.Libraries.MappingStrategies.Mapping import *

class Crossproduct_Mapping_Queue(Mapping):
    def __init__(self,paths,name):
        super().__init__(paths,name)
        self.mapping = dict()

    def compute_mapping(self,db1,db2):
        used1 = set()
        used2 = set()
        print("Terme in Db1:" + str(len(db1.terms)))
        print("Terme in Db1:" + str(len(db2.terms)))
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
            if (term1 not in used1 and term2 not in used2):
                self.mapping[term1] = term2
                mapping_sim_plot.append(sim)
                used1.add(term1)
                used2.add(term2)
        plt.figure()
        fig, ax = plt.subplots(2,1
                               )
        ax[0].scatter(range(len(sim_plot)),np.array(sim_plot),s=1,label='ISUB Wkt. Verteilung')
        ax[1].scatter(range(len(mapping_sim_plot)),np.array(mapping_sim_plot),s=1,label='ISUB Mapping Verteilung')

        plt.show()

    def similarity(self,t1,t2,sim):
        return 0