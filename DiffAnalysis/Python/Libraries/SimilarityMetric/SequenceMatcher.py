import difflib



def sequence_matcher(term_name1,term_name2,term_obj1,term_obj2,occ_overlap):
        # similarity was already calculated (just increase by one then)
        # based on the path to the first relation, determine path to second relation
    if term_obj1.type == "int" and term_obj2.type == "int" :
        max_int = max(int(term_name1), int(term_name2))
        if max_int > 0:
            return 1 - abs(int(term_name1) - int(term_name2)) / max_int
        else:
            return 1
    else:
        return difflib.SequenceMatcher(None, term_name1, term_name2).ratio()