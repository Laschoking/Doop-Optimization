
def term_equality(term_obj1, term_obj2, common_occ):
    if term_obj1.name == term_obj2.name:
        return 1
    else:
        return 0