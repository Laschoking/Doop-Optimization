
def jaccard_term_overlap(term_obj1,term_obj2,occ_overlap):
    # compress the term-occurances
    structural_sim = occ_overlap.total() ** 2 / (term_obj1.occurrence_c.total() + term_obj2.occurrence_c.total())
    if structural_sim > 50:
        print(structural_sim,term_obj1.name,term_obj2.name)
    # eventually integrate lexical similarity
    return structural_sim