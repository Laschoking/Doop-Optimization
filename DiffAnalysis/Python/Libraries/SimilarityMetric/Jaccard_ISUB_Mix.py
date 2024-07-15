from Python.Libraries.SimilarityMetric.Jaccard_Min import *
from Python.Libraries.SimilarityMetric.ISUB_SequenceMatcher import *

def jaccard_isub_mix(term_obj1,term_obj2,occ_overlap):
    p = 0.5
    jaccard_sim = jaccard_min(term_obj1,term_obj2,occ_overlap)
    isub_sim = isub_sequence_matcher(term_obj1,term_obj2,occ_overlap)
    return p * jaccard_sim + (1 - p) * isub_sim

#def structural_similarity_jaccard(term_obj1,term_obj2,occ_overlap,all_tuple_sim):
