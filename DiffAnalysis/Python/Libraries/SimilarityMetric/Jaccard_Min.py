import Python.Libraries.ExpansionStrategies.Iterative_Anchor_Expansion
def jaccard_min(term_obj1,term_obj2,occ_overlap):
    # compress the term-occurances
    # TODO Bei implementierung der Neighbourhood-Sim drauf achten, dass Termpaare die oft vorkommen auch besser Gewichtet werden
    # das sollten sie sowieso, da sie dann mehr Überlappung haben
    if occ_overlap.total() == 0:
        return 0
    local_sim = occ_overlap.total() ** 1.5 / min(term_obj1.occurrence_c.total(),term_obj2.occurrence_c.total())



    #for n


    # eventually integrate lexical similarity
    return local_sim

#def structural_similarity_jaccard(term_obj1,term_obj2,occ_overlap,all_tuple_sim):
